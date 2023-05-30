from flask import Flask, request, jsonify
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


app.name = "flask-server-2"

# Set the configuration variable based on the environment variable
app.config['ARGUMENT'] = os.environ.get('server_name')

job_categories = ["Development", "Manager", "Business", "Designer"]

job_posts = [
    {
        "job_category": "Development",
        "job_posts": [
            {
                "Development-1": {
                    "role_name": "development role 1",
                    "description": " description of the role"
                }
            }
        ]
    },
    {
        "job_category": "Business"
    }
]


@app.route('/')
def hello():
    print(app.name)
    print(app.config['ARGUMENT'])
    return 'Hello, Flask!'


@app.route('/api/subscribe', methods=['GET'])
def subscribe():

    return "subscriber"


@app.route('/api/users', methods=['POST'])
def create_user():
    # data = request.json
    # Process the request data and create a new user
    # ...
    response = {'message': 'User created successfully', 'name':str(app.name), 'arg': str(app.config['ARGUMENT'])}
    return jsonify(response)


if __name__ == '__main__':
    print(app.config['ARGUMENT'])
    app.run(port=8080, debug=True)
