# pull the official docker image

FROM python:3.11.1

# set work directory
WORKDIR app

# install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .