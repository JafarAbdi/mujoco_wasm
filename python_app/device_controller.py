import requests
import json

# The URL of the JavaScript server endpoint that will receive the joint configurations
js_server_url = 'http://localhost:3000/set_joints'

def send_joint_configurations(joint_configurations):
    # Convert the joint configurations to JSON
    data = json.dumps(joint_configurations)
    # Send a POST request with the joint configurations as JSON
    response = requests.post(js_server_url, data=data, headers={'Content-Type': 'application/json'})
    # Check if the request was successful
    if response.status_code == 200:
        print('Joint configurations sent successfully.')
    else:
        print(f'Failed to send joint configurations. Status code: {response.status_code}')

# Example joint configurations
joint_configurations = {
    'joint_angles': [0.5, 1.2, -0.3, 2.1]
}

# Send the joint configurations to the JavaScript server
send_joint_configurations(joint_configurations)