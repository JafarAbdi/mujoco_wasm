import streamlit as st
import streamlit.components.v1 as components

# Define the path to the HTML file
html_file_path = "device_orientation.html"

# Load the HTML file as a string
with open(html_file_path, "r") as f:
    html_str = f.read()

# Create the custom component
def device_orientation_component():
    # Use the Streamlit components API to render the HTML
    orientation_data = components.html(html_str, height=100, key="device_orientation")

    # Return the orientation data received from the frontend
    return orientation_data

# Use the custom component in the Streamlit app
if __name__ == "__main__":
    st.title("Device Orientation Streamlit Component")

    # Call the custom component and get the data
    orientation_data = device_orientation_component()

    # If data is received, display it
    if orientation_data:
        st.write("Orientation data received:")
        st.json(orientation_data)