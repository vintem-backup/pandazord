FROM python:3.8.1-alpine3.11
ENV PYTHONUNBUFFERED 1
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev linux-headers
RUN mkdir /code
COPY requirements.txt /code/
WORKDIR /code
RUN pip install --upgrade pip
RUN pip install -r requirements.txt 
COPY . /code/
RUN chmod +x entrypoint.sh
CMD ["sh", "entrypoint.sh"]