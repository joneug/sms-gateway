import argparse
import logging
import secrets
import threading
import time
from wsgiref.simple_server import make_server

import falcon
from falcon_auth import FalconAuthMiddleware, TokenAuthBackend

import sms_gateway.config as config
from .background_threads.sms_sender import send_sms
from .controllers.controller_utils import user_loader
from .controllers.sms import SMS

auth_backend = TokenAuthBackend(user_loader)
auth_middleware = FalconAuthMiddleware(auth_backend)

api = falcon.API(middleware=[auth_middleware])

sms = SMS()
api.add_route('/sms', sms)

parser = argparse.ArgumentParser()
parser.add_argument('--loglevel', type=str, help="Sets the log level.", default='INFO')
parser.add_argument('--pin', type=str, help="Sets the PIN used to unlock the modem.", default=None)
parser.add_argument('--port', type=int, help="Sets the port the web app is listening on.", default=8000)
parser.add_argument('--token', type=str, help="Sets the authentication token.", default=None)
parser.add_argument('--device', type=str, help="Sets the device to use with gammu.", default='/dev/modem')


def main():
    parse_options(parser.parse_args())
    unlock_modem()

    # Start background thread that sends SMS
    sms_sender = threading.Thread(name="SMSSender", target=send_sms)
    sms_sender.setDaemon(True)
    sms_sender.start()

    # Start web app
    with make_server('', config.PORT, api) as httpd:
        logging.info(f'Serving on port {config.PORT}...')
        httpd.serve_forever()


def parse_options(options):
    # Log level
    if config.LOGLEVEL is None:
        config.LOGLEVEL = options.loglevel
    config.LOGLEVEL = config.LOGLEVEL.upper()
    logging.basicConfig(level=config.LOGLEVEL, format='%(asctime)s [%(levelname)s] %(message)s')

    # PIN
    if config.PIN is None:
        config.PIN = options.pin
    if config.PIN is None or len(config.PIN) == 0:
        raise Exception('PIN is required to unlock the modem')

    # Port
    if config.PORT is None:
        config.PORT = options.port
    config.PORT = int(config.PORT)

    # Token
    if config.TOKEN is None:
        config.TOKEN = options.token
    if config.TOKEN is None or config.TOKEN == '':
        config.TOKEN = secrets.token_urlsafe(20)
        logging.warning(f"No token set - using auto-generated token '{config.TOKEN}' instead")

    # Device
    if config.DEVICE is None:
        config.DEVICE = options.device


def unlock_modem():
    # Initialize
    config.SM.SetConfig(0, {'Device': config.DEVICE, 'Connection': 'at'})
    config.SM.Init()

    # Unlock
    status = config.SM.GetSecurityStatus()
    if status is None:
        logging.info('Modem is already unlocked')
    elif config.SM.GetSecurityStatus() == 'PIN':
        logging.info('Unlocking modem...')
        config.SM.EnterSecurityCode('PIN', config.PIN)
        time.sleep(10)
    else:
        raise Exception(f"Unexpected security status '{status}'")


if __name__ == '__main__':
    main()
