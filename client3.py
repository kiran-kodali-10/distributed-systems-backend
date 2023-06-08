import socket
import json
import logging
import time

# Configure the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_custom_request(host, port, request):
    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, port))

    # Send the HTTP request
    client_socket.sendall(request.encode())

    # Receive and print the response
    response = b""
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        response += data

    # Log the client entry
    logging.info("Client - connected.")
    print(response.decode())

    # Close the socket
    client_socket.close()

# Specify the host and port of the server
host = "localhost"
port = 8080

# Specify the list of subscribed topics
subscribed_topics = ["Development", "Business"]

# Define the HTTP request template with the subscribed topic
request_template = """GET /topics/{topic} HTTP/1.1\r\nHost: {host}\r\n\r\n"""

# Continuously send requests to fetch and display data for each subscribed topic
while True:
    for topic in subscribed_topics:
        # Generate the HTTP request with the subscribed topic
        request = request_template.format(topic=topic, host=host)

        # Send the custom request
        send_custom_request(host, port, request)

    # Sleep for 2 seconds between requests for each topic
    time.sleep(2)
