FROM python:alpine3.17
WORKDIR /usr/pythonplay
COPY ./requirements.txt /usr/pythonplay/requirements.txt
COPY ./docker-entrypoint.sh /usr/pythonplay/docker-entrypoint.sh
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . /usr/pythonplay