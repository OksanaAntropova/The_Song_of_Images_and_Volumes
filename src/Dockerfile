# pull official base image
FROM python:3.10.2-slim-bullseye

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat

# install python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy project inside the container
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]