import falcon

import sms_gateway.config as config


def user_loader(token):
    if token == config.TOKEN:
        return 'user'
    else:
        return None


def get_parameter(req, param):
    param_value = req.get_param(param)
    if param_value is None or param_value == "":
        raise falcon.HTTPBadRequest(
            'Missing parameter',
            f"The parameter '{param}' has to be specified."
        )

    return param_value
