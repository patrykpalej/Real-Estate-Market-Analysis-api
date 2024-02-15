FROM python:3.11.8-slim-bullseye

WORKDIR /usr/app/src/

COPY ./Pipfile /usr/app
COPY ./Pipfile.lock /usr/app

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --system --deploy

COPY ./src /usr/app/src/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
