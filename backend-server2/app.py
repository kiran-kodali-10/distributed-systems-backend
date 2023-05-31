from flask import Flask, request, jsonify
import os
from config import Config
import requests

app = Flask(__name__)
app.config.from_object(Config)


app.name = "flask-server-2"

# Set the configuration variable based on the environment variable
app.config['ARGUMENT'] = os.environ.get('server_name')

job_categories = ["Development", "Marketing", "Sales", "Business"]
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
    print(app.config['ARGUMENT'])
    response = requests.get("http://172.31.10.181:8080/api/subscribe")
    return 'Hello, Flask!'+response.text


@app.route('/api/subscribe', methods=['GET'])
def subscribe():

    return "subscriber"


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
    data = request.json
    job_category = data["job_category"]
    target_dict = None
    new_job_post = data["new_job_post"]

    # Add data to the publisher
    if job_category not in job_categories:
        job_categories.append(job_category)

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
            print(f"{subscriber_name} has subscribed to the {job_category} category.")
            response_data.append({
                "subscriber_name": subscriber_name,
                "job_posts": new_job_post
            })
        else:
            print(f"{subscriber_name} has not subscribed to the {job_category} category.")
    
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
    print(app.config['ARGUMENT'])
    app.run(port=8080, debug=True, host="0.0.0.0")
