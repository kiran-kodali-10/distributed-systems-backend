from flask import Flask, request, jsonify
import requests
import logging
import DSM

app = Flask(__name__)

app.name = "flask-server-1"

# Clear the Flask's default logger
app.logger.handlers.clear()
# Set the logging level
app.logger.setLevel(logging.DEBUG)

# Create a log handler for console output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

time_out=4

# Create a log formatter
formatter = logging.Formatter(' %(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the log handler to the application logger
app.logger.addHandler(console_handler)

all_job_categories = ["DEVELOPMENT", "MARKETING", "SALES", "BUSINESS"]
handle_categories = ["BUSINESS", "SALES"]

new_jobs_queue = []

master_node_2 = "http://172.31.5.101:8080"


@app.route('/')
def hello():
    print(app.name)
    response = app.name
    # response = requests.get(master_node_2)
    return 'Hello, Flask!'+str(app.name) + " "+str(response)


@app.route('/api/publish', methods=['POST'])
def post_published_data():
    data = request.get_json()

    new_jobs_queue.append(data)

    if data["jobCategory"] not in handle_categories:
        response = requests.post(master_node_2+"/api/publish", json=data)
        return response

    DSM.JOB_POSTS.append(data)
    # print(DSM.JOB_POSTS)

    response = jsonify({'message': 'Job posted successfullly',
                        'name': str(app.name)})
    response.status_code = 200

    return response

def validate_sequence(sequence,clientName):
    if sequence == str(time_out):
        app.logger.info(f'{clientName} died, please restart')

@app.route('/gs/subscribe', methods=['GET'])
def send_data_for_subscriber():
    data = request.args
    jobCategory = data["jobCategory"]
    sequence = data["sequence"]
    clientName = data['clientName']
    validate_sequence(sequence, clientName)
    response = []
    if jobCategory in handle_categories:
        if len(new_jobs_queue) == 0:
            return jsonify([{"message": "No new Data"}])
        for new_job in new_jobs_queue:
            # print(
            #     f'job-category: {jobCategory} and new job cate: {new_job["jobCategory"]}')
            if jobCategory.lower() == new_job["jobCategory"].lower():
                response.append(new_job)
        response.append({"message": str(app.name)})
        return jsonify(response)
    else:
        response_data = requests.get(
            master_node_2+"/gs/subscribe", 
            params={"companyName": jobCategory, 
                    "sequence": data["sequence"],
                    "clientName": data["clientName"]
                    })
        return jsonify(response_data.json())


@app.route('/api/publish', methods=['GET'])
def get_subscribe_data():
    # send the job posts of that subscriber.
    data = request.args
    companyName = data["companyName"]
    response = []
    # print(data)
    for jobPost in DSM.JOB_POSTS:
        companyName = jobPost["companyName"]
        if companyName.lower() == companyName.lower():
            response.append(jobPost)
    return jsonify(response)



@app.route('/api/subscribe', methods=['POST'])
def post_subscribed_data():
    data = request.get_json()
    subscriberName = data["subscriberName"]
    jobCategory = data["jobCategory"]
    existing_subscriber = False

    if jobCategory in handle_categories:

        for subscriber in DSM.SUBSCRIBER_DATA:
            if subscriber["subscriberName"].lower() == subscriberName.lower():
                subscriber["subscribed"].append(jobCategory)
                existing_subscriber = True
                break

        if not existing_subscriber:
            DSM.SUBSCRIBER_DATA.append({
                "subscriberName": data["subscriberName"],
                "subscribed": [data["jobCategory"]]
            })

        response = jsonify({
            "message": "Subscribed Successfully ",
            "name": str(app.name)

        })
        response.status_code = 200
        return response
    else:
        # send the request
        response = requests.post(url=master_node_2+"/api/subscribe", json=data)
        return response


@app.route('/api/subscribe', methods=['GET'])
def get_subscribed_data():
    response = []
    count = 0
    # return the list of objects with subscriber name and the list of job posts
    for subscriber in DSM.SUBSCRIBER_DATA:
        subscriberName = subscriber["subscriberName"]
        subscribed = subscriber["subscribed"]
        append_object = {
            "subscriberName": subscriberName,
            "jobPosts": []
        }
        print(count+1)

        for jobPost in DSM.JOB_POSTS:
            for subscribedCategory in subscribed:
                print(f"JOB POST: {jobPost}")
                if jobPost["jobCategory"].lower() in subscribedCategory.lower():
                    append_object["jobPosts"].append(jobPost)
        response.append(append_object)

    return jsonify(response)


@app.route('/api/unsubscribe', methods=['DELETE'])
def unsubscribe():
    data = request.get_json()
    jobCategory = data["jobCategory"]
    subscriberName = data["subscriberName"]

    for subscriber in DSM.SUBSCRIBER_DATA:
        if subscriber["subscriberName"].lower() == subscriberName.lower() and jobCategory in subscriber["subscribed"]:
            subscriber["subscribed"].remove(jobCategory.upper())
            break
    
    return jsonify({
        'message': "unsubscribed successfully",
        'name': str(app.name)
    })


# @app.errorhandler(Exception)
def server_error(error):
    app.logger.error(error)
    response = jsonify({
        'error': 'Internal Server error',
        'message': 'An unexpected error occurred on the server.'
    })
    response.status_code = 500
    return response


if __name__ == '__main__':
    app.run(port=8080, host="0.0.0.0", debug=True)
