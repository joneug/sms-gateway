import multiprocessing
import os

import gammu

# Variables
LOGLEVEL = os.environ.get('SG_LOGLEVEL')
PORT = os.environ.get('SG_PORT')
PIN = os.environ.get('SG_PIN')
TOKEN = os.environ.get('SG_TOKEN')
DEVICE = os.environ.get('SG_DEVICE')
WHITELIST = os.environ.get('SG_WHITELIST')

# SMS Queue
SMS_QUEUE = multiprocessing.Queue()

# Gammu State Machine
SM = gammu.StateMachine()
