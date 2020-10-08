# SMS Gateway API

This repository contains a Python web application providing an API for sending SMS. The SMS sending is based on [`python-gammu`](https://pypi.org/project/python-gammu/). Some concepts used for implementing this application are borrowed from [`vvanholl/smsgateway-gammu`](https://github.com/vvanholl/smsgateway-gammu).

## Usage

### PIP

First install `sms-gateway` using PIP:

```sh
$ pip install sms-gateway
```

Then run the application and provide the device name, the PIN and a token used to authenticate against the API. For further options see [Options](#options).

```sh
$ sms-gateway --device /dev/ttyUSB1 --pin 1234 --token ABCD1234
```

### Docker

You can also run the web app via Docker:

```sh
$ docker run --device=/dev/ttyUSB1:/dev/modem -p 8000:8000 joneug/sms-gateway --pin 1234 --token ABCD1234
```

Alternatively you can use docker-compose:

```yaml
version: '3'
services:
  sms-gateway:
    image: joneug/sms-gateway
    environment:
      - "SG_PIN=1234"
      - "SG_TOKEN=ABCD1234"
    devices:
      - /dev/ttyUSB1:/dev/modem
```

## Options

TODO
