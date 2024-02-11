import streamlit as st
from streamlit.server.server import Server
import streamlit.components.v1 as components
from device_orientation_component import device_orientation_component


# Function to handle orientation data
def handle_orientation(alpha, beta, gamma, verbose=False):
    # Update the orientation data in the session state
    st.session_state['orientation'] = {'alpha': alpha, 'beta': beta, 'gamma': gamma}
    st.write("Orientation data received")
    if verbose:
        log_orientation_data(alpha, beta, gamma)

def log_orientation_data(alpha, beta, gamma):
    # Log the orientation data
    st.write(f"Alpha: {alpha}°")
    st.write(f"Beta: {beta}°")
    st.write(f"Gamma: {gamma}°")

# Function to handle motion data
def handle_motion(acceleration, acceleration_including_gravity, rotation_rate, interval, verbose=False):
    # Process the motion data
    # For example, you could log it, save it, or perform calculations
    # log motion data
    st.write("Motion data received")
    st.session_state['motion'] = {
        'acceleration': acceleration,
        'acceleration_including_gravity': acceleration_including_gravity,
        'rotation_rate': rotation_rate,
        'interval': interval
    }
    if verbose:
        log_motion_data(acceleration, acceleration_including_gravity, rotation_rate, interval)

def log_motion_data(acceleration, acceleration_including_gravity, rotation_rate, interval):
    # Log the motion data
    st.write(f"Acceleration: {acceleration} m/s²")
    st.write(f"Acceleration including gravity: {acceleration_including_gravity} m/s²")
    st.write(f"Rotation rate: {rotation_rate}°/s")
    st.write(f"Data interval: {interval} ms")

# Function to start/stop the demo
def toggle_demo():
    ctx = st.session_state
    if ctx.get('is_running', False):
        # Stop the demo
        ctx['is_running'] = False
        ctx['button_label'] = "Start demo"
    else:
        # Start the demo
        ctx['is_running'] = True
        ctx['button_label'] = "Stop demo"

# Initialize session state
if 'orientation' not in st.session_state:
    st.session_state['orientation'] = {'alpha': 0, 'beta': 0, 'gamma': 0}

if 'motion' not in st.session_state:
    st.session_state['motion'] = {'acceleration': 0, 'acceleration_including_gravity': 0, 'rotation_rate': 0, 'interval': 0}


if 'is_running' not in st.session_state:
    st.session_state['is_running'] = False
    st.session_state['button_label'] = "Start demo"

# UI layout
st.title("JavaScript Sensor Access Demo")

if st.button(st.session_state['button_label']):
    toggle_demo()

# Display sensor data (placeholder values)
st.subheader("Orientation")
st.metric(label="X-axis (β)", value=f"{st.session_state['orientation']['beta']}°")
st.metric(label="Y-axis (γ)", value=f"{st.session_state['orientation']['gamma']}°")
st.metric(label="Z-axis (α)", value=f"{st.session_state['orientation']['alpha']}°")

# Display motion data
st.subheader("Motion")
st.metric(label="Acceleration", value=f"{st.session_state['motion']['acceleration']} m/s²")
st.metric(label="Acceleration including gravity", value=f"{st.session_state['motion']['acceleration_including_gravity']} m/s²")
st.metric(label="Rotation rate", value=f"{st.session_state['motion']['rotation_rate']}°/s")
st.metric(label="Data interval", value=f"{st.session_state['motion']['interval']} ms")


# add inputs and a button for motion data
components.html("""
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>MuJoCo Demo</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <meta name="application-name"   content="mujoco_wasm">
        <meta name="description"        content="MuJoCo Testbed">
        <meta name="keywords"           content="MuJoCo">
        <meta name="author"             content="zalo">
        <meta name="viewport"           content="width=device-width, initial-scale=1.0, maximum-scale=1.0, viewport-fit=cover, user-scalable=no, shrink-to-fit=0">
        <meta name="theme-color"        content="#ffffff">
        <link rel ="icon" type="image/x-icon" href="./examples/favicon.png">
    </head>

    <body style="margin:0px; background-color:rgb(255, 255, 255); overflow:hidden; position:fixed; min-height: 100%;
                 touch-action: none;
                 -webkit-touch-callout: none; /* iOS Safari */
                 -webkit-user-select: none; /* Safari */
                 -khtml-user-select: none; /* Konqueror HTML */
                 -moz-user-select: none; /* Old versions of Firefox */
                 -ms-user-select: none; /* Internet Explorer/Edge */
                 user-select: none; /* Non-prefixed version, currently supported by Chrome, Edge, Opera and Firefox */">
        <h1 hidden></h1> <!-- Puts the Lighthouse Score over 90 heheh-->

		<!-- Import maps polyfill -->
		<script async src="https://unpkg.com/es-module-shims@1.6.3/dist/es-module-shims.js"></script>

            
        <div id="motionData">
            <h2>Device Motion Data:</h2>
        
            <!-- Display values of acceleration along 
                X, Y, Z axes, and interval -->
            <p>Acceleration X: <span id="accelerationX">
            0</span>
            </p>
            <p>Acceleration Y: <span id="accelerationY">
            0</span>
            </p>
            <p>Acceleration Z: <span id="accelerationZ">
            0</span>
            </p>
            <p>Interval: <span id="interval">
            0</span> ms
            </p>
        </div>

        
        <script type="text/javascript">
            function requestOrientationPermission(){
                DeviceOrientationEvent.requestPermission()
                .then(response => {
                    if (response == 'granted') {    
                        const alpha = event.alpha;
                        const beta = event.beta;
                        const gamma = event.gamma;

                        // Prepare the data to send
                        const orientationData = { alpha, beta, gamma };

                        // Send the data to the server
                        fetch('http://10.0.0.12:3000/orientation', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(orientationData),
                        })
                        .then(response => response.json())
                        .then(data => console.log('Success:', data))
                        .catch((error) => console.error('Error:', error));
                    } else {
                        console.log("Device orientation not supported");
                        // send a message to the server that the device orientation is not supported
                        fetch('http://10.0.0.12:3000/orientation', 
                        { method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                          body: JSON.stringify({error: "Device orientation not supported"}),
                        })
                        .then(response => response.json())
                        .then(data => console.log('Success:', data))
                        .catch((error) => console.error('Error:', error));
                    }
                        // if (response == 'granted') {
                        //     console.log("we are in business!");
                        //     window.addEventListener('deviceorientation', (e) => {
                        //         console.log(e.alpha, e.beta, e.gamma)
                        //         // do something with e
                        //     })
                        // } else {
                        //     console.log("Device orientation not supported");
                        // }
                    })
                .catch(console.error)
            }
        </script>
        
        <button onclick='requestOrientationPermission();'>Request orientation permission</button>


        <!-- Allows three.js Examples to work without building -->
        <script type="importmap">
            { "imports": { "three": "./node_modules/three/build/three.module.js", "three/addons/": "./node_modules/three/examples/jsm/"} }
        </script>

        <!-- <script type="module" src="./examples/server.js"></script> -->
        <!-- <script type="module">
            import app from './examples/server.js';
            window.addEventListener('load', () => {
                app.listen(3000, () => console.log('Server is running on http://10.0.0.12:3000'));
            });
        </script> -->

        <!-- <div id="appbody" style="position: absolute;">
            <!--<div id="error"></div>
            <script type="module" src="./examples/Debug.js"></script>-->
            <!-- <script type="module" src="./examples/main.js"></script> -->
        <!-- </div> -->
    </body>
</html>
""")

# Run the Streamlit app by typing `streamlit run streamlit_app.py` in the terminal