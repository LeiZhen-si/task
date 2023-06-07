# base image
FROM python:3.9.4-slim

# docker build -t flask-test:0.0.1 .
# docker run -it -v ~/Documents/sync_folder:/usr/src/app/sync_folder --net=host -p 5001:5000 --name flask-test flask-test:0.0.1

# install netcat
RUN apt-get update && \
    apt-get -y install netcat && \
    apt-get clean

# set working directory
WORKDIR /usr/src/app
RUN mkdir /usr/src/app/sync_folder
RUN mkdir /usr/src/app/sync_folder/tasks

# add and install requirements
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# add app
COPY . /usr/src/app

# run server
CMD ["python","app.py"]
