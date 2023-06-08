import socket
import json
import time
import logging


# Configure the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def sendRequest(host_id, port, request):
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket created

    client_socket.connect((host_id, port))  # Connect the client socket to the server with the specified host id and port no.

    client_socket.sendall(request.encode()) # Send the HTTP request to the server

    # Build the response
    response = b""
    while True:
        response_data = client_socket.recv(4096)
        if not response_data:
            break
        response += response_data

    # Logging info of the client entry
    logging.info("Client 1 is connected to the server.")
    print(response.decode())

    client_socket.close() # Close the socket connection

# Specify the host and port of the server
host_id = "localhost"
port = 8080

# data for payload
job_posts = [
    {
        "role_name": "development role 6",
        "job_description": " description of the role1",
        "Company_name": "Oracle"
    },
    {
        "role_name": "development role 7",
        "job_description": " description of the role2",
        "Company_name": "Apple"
    },
    {
        "role_name": "development role 8",
        "job_description": " description of the role 3",
        "Company_name": "Amazon"
    },
    {
        "role_name": "development role 9",
        "job_description": " description of the role 4",
        "Company_name": "KION"
    },
    {
        "role_name": "Marketing role 1",
        "job_description": " description of the role1",
        "Company_name": "Applied Materials"
    },
    {
        "role_name": "Marketing role 5",
        "job_description": " description of the role2",
        "Company_name": "KPMG"
    },
    {
        "role_name": "Marketing role 6",
        "job_description": " description of the role 3",
        "Company_name": "PWC"
    },
    {
        "role_name": "Marketing role 7",
        "job_description": " description of the role 4",
        "Company_name": "Deloitte"
    },
    # Add more data objects as needed
]

#  HTTP request template
request_template = """GET / HTTP/1.1\r\nHost: localhost\r\nContent-Type: application/json\r\nContent-Length: {content_length}\r\n\r\n{json_payload}"""

# Send the HTTP requests with different dynamic data
for job_data in job_posts:
    
    json_payload = json.dumps(job_data) # Converting it to json format 

    content_length = len(json_payload)

    # Create an HTTP request with the required payload and content length for JSON.
    request = request_template.format(content_length=content_length, json_payload=json_payload)

    # Send the HTTP request
    sendRequest(host_id, port, request)

    # Sleep for 2 sec then send another request
    time.sleep(2)
