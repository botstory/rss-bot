FROM python:3.6

ENV PYTHONUNBUFFERED 1

# runtime dependencies
RUN apt-get install -y --no-install-recommends \
    libmagickwand-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

ADD . /usr/src/app
