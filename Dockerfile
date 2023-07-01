FROM python:3.9-alpine3.13
LABEL maintainer="john arroyo"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# First command creates a virtual environment in image to store our dependencies (safeguards against any conflicting dependencies that may come in the base image)
# Second command upgrades pip in the virtual environment we just created
# Third command installs the requirements.txt file inside the image
# Fourth command removes the tmp directory
# Fifth command adds a new user inside our image (reason for this is its best practice not to use root user) (doesnt create a password or home directory for the user)
ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# This command updates the environment variable inside the image (Here we update the system PATH environment variable)
ENV PATH="/py/bin:$PATH"

USER django-user