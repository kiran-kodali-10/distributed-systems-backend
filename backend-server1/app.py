from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Flask!'



@app.route('/api/subscribe', methods=['GET'])
def subscribe():

    return "lol"


@app.route('/api/users', methods=['POST'])
def create_user():
    # data = request.json
    # Process the request data and create a new user
    # ...
    response = {'message': 'User created successfully'}
    return jsonify(response)

if __name__ == '__main__':
    app.run()
