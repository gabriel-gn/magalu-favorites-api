FROM python:3.6

RUN mkdir src
COPY ./src ./src
COPY setup/requirements.txt .

ENV PYTHONPATH=:/src
RUN python3 -m venv venv
RUN /venv/bin/python -m pip install -r requirements.txt
RUN touch src/__init__.py