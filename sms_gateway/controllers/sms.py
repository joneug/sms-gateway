import json

import falcon

import sms_gateway.config as config
from .controller_utils import get_parameter


class SMS(object):

    def on_get(self, req, resp):
        sms_messages = []

        start = True
        status = config.SM.GetSMSStatus()
        remain = status['SIMUsed'] + status['PhoneUsed'] + status['TemplatesUsed']
        while remain > 0:
            if start:
                sms = config.SM.GetNextSMS(Start=True, Folder=0)
                start = False
            else:
                sms = config.SM.GetNextSMS(Location=sms[0]['Location'], Folder=0)

            remain -= len(sms)
            sms_messages.append({'number': sms[0]['Number'], 'text': sms[0]['Text']})

        resp.body = json.dumps(sms_messages)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        number = get_parameter(req, "number")
        # Remove spaces from number
        number = number.replace(" ", "")
        text = get_parameter(req, "text")
        config.SMS_QUEUE.put((number, text))

        resp.status = falcon.HTTP_202
