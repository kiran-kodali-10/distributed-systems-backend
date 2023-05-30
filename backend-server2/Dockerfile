FROM python:3.9-slim

WORKDIR /flask-server2

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "sh", "-c", "export server_name=flask-server2 && python -m flask run --host=0.0.0.0 --port=8080 "]

# CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0","--port","8080"]
# CMD [ "python", "app.py", "flask-server2"]
EXPOSE 8080


