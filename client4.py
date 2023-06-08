import socket
import json
import time
import logging
from urllib.parse import urlencode


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
    
    logging.info("SUBSCRIBER 1 subscribed to Job Category: Business, Sales.")
    decoded_response = response.decode()

    start_index = decoded_response.find("{")
    end_index = decoded_response.rfind("}")
    json_payload = decoded_response[start_index:end_index + 1]

    json_payload = json_payload.strip()
    print(f'payload: {json_payload}')

    json_data = json.loads(json_payload)
    data = json_data["message"]
    print(data)
    # for temp, value in decoded_response:
    #     print(temp,)
    # print(type(decoded_response))
    # print(response.decode())

    client_socket.close() # Close the socket connection

# Specify the host and port of the server
host_id = "54.67.32.100"
port = 8080

subscribed_job_categories = ["BUSINESS", "SALES"]

base_url = "/gs/subscribe"

# Send the HTTP requests with different dynamic data
# while True:
for job_category in subscribed_job_categories:
    query_params = {
        "jobCategory": job_category,
        
    }
    encoded_params = urlencode(query_params)
    url = f"{base_url}?{encoded_params}"
    request = f"GET {url} HTTP/1.1\r\nHost: {host_id}\r\n\r\n"

    # Send the HTTP request
    sendRequest(host_id, port, request)
# Sleep for 2 sec then send another request

logging.info("SUBSCRIBER 1 GOT THE BUSINESS POSTINGS.")
time.sleep(2)

