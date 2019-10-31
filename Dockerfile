FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install python3
RUN apt-get -y install python3-pip
RUN pip3 install -r requirements.txt
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV FLASK_RUN_CERT=cert.pem
ENV FLASK_RUN_KEY=key.pem
COPY . .
ENTRYPOINT ["/usr/local/bin/flask", "run"]
