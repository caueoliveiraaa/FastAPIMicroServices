FROM python:3.12.1-slim-bullseye

WORKDIR /app

COPY ./order_api /app

RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt \
    && python security/unit_test.py

ENTRYPOINT [ "python", "main.py" ]
