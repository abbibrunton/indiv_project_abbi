FROM python:3.6.8
RUN apt-get update
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN pip3 install --upgrade pip
RUN apt install -y netcat
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
ENV FLASK_APP run.py
ENV FLASK_ENV production
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 5000
ENV FLASK_RUN_CERT cert.pem
ENV FLASK_RUN_KEY key.pem
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
COPY . .
ENTRYPOINT ["./init.sh"]
