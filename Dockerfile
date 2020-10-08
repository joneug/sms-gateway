FROM python:3.8.3-slim-buster

ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Berlin

WORKDIR /code/

COPY requirements.txt .
RUN apt-get update \
    && apt-get install -y --no-install-recommends usb-modeswitch usb-modeswitch-data gammu python-gammu libgammu-dev gcc linux-libc-dev libc6-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && echo $TZ > /etc/timezone \
    && apt-get purge -y --auto-remove gcc linux-libc-dev libc6-dev

COPY . .

RUN useradd --create-home user \
 && chown -R user /code \
 && adduser user dialout

USER user

ENTRYPOINT [ "python", "-m", "sms_gateway" ]
