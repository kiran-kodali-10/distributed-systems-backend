from flask import Flask, request, jsonify
import os
import requests
import logging


app = Flask(__name__)

app.name = "flask-server-1"

# Clear the Flask's default logger
app.logger.handlers.clear()
# Set the logging level
app.logger.setLevel(logging.DEBUG)

# Create a log handler for console output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a log formatter
formatter = logging.Formatter(' %(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the log handler to the application logger
app.logger.addHandler(console_handler)

all_job_categories = ["Development", "Marketing", "Sales", "Business"]
master_job_categories = ["Business", "Development"]

publisher_data = [
    {
        "job_category": "Development",
        "job_posts": [
            {
                "role_name": "",
                "job_description": "",
                "publisher_name": ""
            }
        ]
    }
]
subscriber_data = [
    {
        "subscriber_name": "Silvi",
        "subscribed_categories": ["Development", "Marketing"]
    }
]


@app.route('/')
def hello():
    print(app.name)
    # print(app.config['ARGUMENT'])
    response = requests.get("http://172.31.10.181:8080/api/subscribe")
    return 'Hello, Flask!'+response.text


@app.route('/api/subscribe_master', methods=['GET'])
def subscribed_data():
    data = request.json
    app.logger.info(f"{app.name} - Got request from {data['node']} ")


@app.route('/api/subscribe', methods=['GET'])
def subscribe():
    data = request.json
    subscriber_name = data["subscriber_name"]
    subscribed_category = data["subscribed_category"]
    subscriber_details = []
    # if subscribed_category in master_job_categories:
    #     response = requests.get("http://172.31.10.181:8080/api/subscribe")
    for subscriber in subscriber_data:
        if subscriber["subscriber_name"] in subscriber_name:
            subscriber_details.append(subscriber)
            if subscribed_category not in subscriber["subscribed_categories"]:
                subscriber["subscribed_categories"].append(subscribed_category)

    app.logger.info(
        f"{app.name} - {subscriber_name} has subscribed to the {subscribed_category} category.")
    return jsonify(subscriber_details)


# API to set whatever the pubslisher has published and return
'''
request object format:
{
    job_category: "",
    new_job_post: {
        "role_name": "",
        "job_description": "",
        "publisher_name": ""
    }
}
'''


@app.route('/api/setPublisherData',  methods=['POST'])
def set_published_data():
    temp = request.json
    if "data" in temp:
        # the request came from a node
        app.logger.info(f"{app.name} - Got request from {temp['node']} ")
    data = temp["data"]
    node_name = temp["node"]

    job_category = data["job_category"]
    target_dict = None
    new_job_post = data["new_job_post"]

    # Add data to the publisher
    if job_category not in all_job_categories:
        all_job_categories.append(job_category)

    for category_dict in publisher_data:
        if category_dict["job_category"] == job_category:
            target_dict = category_dict
            break
    if target_dict is not None:
        target_dict["job_posts"].append(new_job_post)

    # whoever has subscribed to that job category, update them with the new data
    response_data = []

    for subscriber_dict in subscriber_data:
        subscriber_name = subscriber_dict["subscriber_name"]
        subscribed_categories = subscriber_dict["subscribed_categories"]
        if job_category in subscribed_categories:
            app.logger.info(
                f"{app.name} - {subscriber_name} has subscribed to the {job_category} category.")
            response_data.append({
                "subscriber_name": subscriber_name,
                "job_posts": new_job_post
            })
        else:
            app.logger.info(
                f"{subscriber_name} has not subscribed to the {job_category} category.")

    return jsonify(response_data)


@app.route('/api/getSubscribedData', methods=['POST'])
def get_subscribed_data():
    data = request.json
    job_category = data["jobCategory"]

    # Process the request data and create a new user
    # ...
    response = {'message': 'User created successfully',
                'name': str(app.name), 'arg': str(app.config['ARGUMENT'])}
    return jsonify(response)


if __name__ == '__main__':
    app.run(port=8080, host="0.0.0.0", debug=True)
