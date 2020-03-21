FROM python:3.8.1-alpine3.11
ENV PYTHONUNBUFFERED 1
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev
RUN mkdir /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install pipenv_to_requirements
COPY . /app/
RUN pipenv_to_requirements -f
RUN pip install -r requirements.txt 
RUN chmod +x entrypoint.sh
CMD ["sh", "entrypoint.sh"]