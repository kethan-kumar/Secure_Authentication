FROM ubuntu:20.04


RUN apt-get update -y && \
    
	apt-get install -y python3-pip python3-dev

RUN pip3 install --upgrade pip

COPY ./requirements.txt /app/requirements.txt


WORKDIR /app


RUN pip install -r requirements.txt


EXPOSE 5000
COPY . /app


ENV FLASK_APP=app


ENV FLASK_RUN_PORT=5000
CMD [ "python3", "-m",  "flask", "run", "--host", "0.0.0.0" ]

