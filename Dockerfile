FROM python:3.12-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        make \
        gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
