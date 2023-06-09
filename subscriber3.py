import socket
import json
import time
import logging
from urllib.parse import urlencode
import re


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
    logging.info("SUBSCRIBER 3 subscribed to Job Category:Marketing")
    decoded_response = response.decode()

    start_index = decoded_response.find("[")
    end_index = decoded_response.rfind("]")
    json_payload = decoded_response[start_index:end_index+1]

    json_payload = json_payload.strip()
    message ='flask-server-2'
    message2 = 'No new Data'
    # striped_payload = remove_lines(json_payload)

    # logging.info(f'message: {message2}, payload: {json_payload}')
    # logging.info(f"payload")
    if message in json_payload or message2 in json_payload:
        logging.info("No new Data available")
    else:
         logging.info(f'New Data available: {json_payload}')
         logging.info("SUBSCRIBER 3 GOT THE NEW POSTINGS.")


    client_socket.close() # Close the socket connection

# Specify the host and port of the server
host_id = "13.52.218.34"
# host_id = "localhost"
port = 8080

subscribed_job_categories = ["MARKETING"]

base_url = "/gs/subscribe"

# Send the HTTP requests with different dynamic data
counter = 1
clientName = "subscriber-3"
while True:
    for job_category in subscribed_job_categories:
        query_params = {
            "clientName":clientName,
            "jobCategory": job_category,
            "sequence": counter
            
        }
        encoded_params = urlencode(query_params)
        url = f"{base_url}?{encoded_params}"
        request = f"GET {url} HTTP/1.1\r\nHost: {host_id}\r\n\r\n"

        # Send the HTTP request
        sendRequest(host_id, port, request)
        time.sleep(3)   
    
    

