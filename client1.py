import socket
import json
import time
import logging


# Configure the logger to get the logs
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
host_id = "13.52.218.34"
port = 8080

subscribed_job_categories = ["Development", "Business"]

#  HTTP request template
request_template = """GET /gs/subscribe HTTP/1.1\r\nHost: 13.52.218.34:8080\r\nContent-Type: application/json\r\nContent-Length: {content_length}\r\n\r\n{json_payload}"""

# Send the HTTP requests with different dynamic data
while True:
    for job_category in subscribed_job_categories:
        json_payload = json.dumps(job_category)

        content_length = len(json_payload)
        request = request_template.format(content_length=content_length, json_payload=json_payload)
        # Send the HTTP request
        sendRequest(host_id, port, request)
    # Sleep for 2 sec then send another request
    time.sleep(2)
# for job_data in job_posts:
    
#     json_payload = json.dumps(job_data) # Converting it to json format 

#     content_length = len(json_payload)

#     # Create an HTTP request with the required payload and content length for JSON.
#     request = request_template.format(content_length=content_length, json_payload=json_payload)

#     # Send the HTTP request
#     sendRequest(host_id, port, request)

#     # Sleep for 2 sec then send another request
#     time.sleep(2)
