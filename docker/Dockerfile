FROM python:3.8.5-slim-buster

## Install Poetry
RUN pip install poetry==1.1.4
RUN poetry config virtualenvs.create false

# Create project
WORKDIR /workspace
COPY ./src/ .
RUN poetry install -vvv

CMD /usr/local/bin/shell.sh ; sleep infinity
