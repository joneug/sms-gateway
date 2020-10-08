import logging
import traceback

import sms_gateway.config as config


def send_sms():
    while True:
        data = config.SMS_QUEUE.get()
        try:
            sms_message = {
                'Number': data[0],
                'Text': data[1],
                'SMSC': {'Location': 1}
            }
            config.SM.SendSMS(sms_message)
            logging.info(f'Successfully sent SMS message to {data[0]}')
        except Exception:
            logging.error(f"Error while sending SMS message '{data[1]}' to {data[0]}\n{traceback.format_exc()}")
