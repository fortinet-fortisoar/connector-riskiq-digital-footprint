""" Copyright start
  Copyright (C) 2008 - 2021 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """

import base64

import requests

from connectors.core.connector import ConnectorError, get_logger
from .constants import *

logger = get_logger('riskiq-digital-footprint')


class RiskIQDigitalFootPrint(object):
    def __init__(self, config):
        self.server_url = config.get('server_url')
        if not self.server_url.startswith('https://'):
            self.server_url = 'https://' + self.server_url
        if not self.server_url.endswith('/'):
            self.server_url += '/'
        self.api_key = config.get('username')
        self.api_password = config.get('api_key')
        self.verify_ssl = config.get('verify_ssl')

    def make_api_call(self, endpoint=None, method='GET', data=None, params=None):
        try:
            url = self.server_url + endpoint
            b64_credential = base64.b64encode((self.api_key + ":" + self.api_password).encode('utf-8')).decode()
            headers = {'Authorization': "Basic " + b64_credential, 'Content-Type': 'application/json'}
            response = requests.request(method, url, params=params, data=data, headers=headers, verify=self.verify_ssl)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(response.text)
                raise ConnectorError({'status_code': response.status_code, 'message': response.reason})
        except requests.exceptions.SSLError:
            raise ConnectorError('SSL certificate validation failed')
        except requests.exceptions.ConnectTimeout:
            raise ConnectorError('The request timed out while trying to connect to the server')
        except requests.exceptions.ReadTimeout:
            raise ConnectorError('The server did not send any data in the allotted amount of time')
        except requests.exceptions.ConnectionError:
            raise ConnectorError('Invalid endpoint or credentials')
        except Exception as err:
            logger.exception(str(err))
            raise ConnectorError(str(err))


def add_assets(config, params):
    df = RiskIQDigitalFootPrint(config)
    data = params.get('request')
    params.pop('request')
    param_dict = {k: PARAM_MAP.get(v, v) for k, v in params.items() if
                  v is not None and v != '' and v != {} and v != []}
    endpoint = '/v1/globalinventory/assets/add'
    response = df.make_api_call(endpoint=endpoint, method='POST', data=data, params=param_dict)
    return response


def get_assets_by_type(config, params):
    df = RiskIQDigitalFootPrint(config)
    param_dict = {k: PARAM_MAP.get(v, v) for k, v in params.items() if
                  v is not None and v != '' and v != {} and v != []}
    endpoint = 'v1/globalinventory/assets/{type}'.format(type=param_dict.pop('type'))
    response = df.make_api_call(endpoint=endpoint, params=param_dict)
    return response


def get_assets_by_uuid(config, params):
    df = RiskIQDigitalFootPrint(config)
    param_dict = {k: PARAM_MAP.get(v, v) for k, v in params.items() if
                  v is not None and v != '' and v != {} and v != []}
    endpoint = 'v1/globalinventory/assets/id/{uuid}'.format(uuid=param_dict.pop('uuid'))
    response = df.make_api_call(endpoint=endpoint, params=param_dict)
    return response


def update_assets(config, params):
    df = RiskIQDigitalFootPrint(config)
    data = params.get('request')
    params.pop('request')
    param_dict = {k: PARAM_MAP.get(v, v) for k, v in params.items() if
                  v is not None and v != '' and v != {} and v != []}
    endpoint = '/v1/globalinventory/update'
    response = df.make_api_call(endpoint=endpoint, method='POST', data=data, params=param_dict)
    return response


def get_connected_asset(config, params):
    df = RiskIQDigitalFootPrint(config)
    param_dict = {k: PARAM_MAP.get(v, v) for k, v in params.items() if
                  v is not None and v != '' and v != {} and v != []}
    endpoint = 'v1/globalinventory/assets/{type}/connected'.format(type=param_dict.pop('type'))
    response = df.make_api_call(endpoint=endpoint, params=param_dict)
    return response


def get_task_status(config, params):
    df = RiskIQDigitalFootPrint(config)
    param_dict = {k: PARAM_MAP.get(v, v) for k, v in params.items() if
                  v is not None and v != '' and v != {} and v != []}
    endpoint = '/v1/globalinventory/task/{id}'.format(id=param_dict.pop('id'))
    response = df.make_api_call(endpoint=endpoint, params=param_dict)
    return response


def get_changed_asset(config, params):
    df = RiskIQDigitalFootPrint(config)
    param_dict = {k: PARAM_MAP.get(v, v) for k, v in params.items() if
                  v is not None and v != '' and v != {} and v != []}
    endpoint = 'v1/globalinventory/deltas'
    response = df.make_api_call(endpoint=endpoint, params=param_dict)
    return response


def get_changed_asset_summary(config, params):
    df = RiskIQDigitalFootPrint(config)
    param_dict = {k: PARAM_MAP.get(v, v) for k, v in params.items() if
                  v is not None and v != '' and v != {} and v != []}
    endpoint = 'v1/globalinventory/deltas/summary'
    response = df.make_api_call(endpoint=endpoint, params=param_dict)
    return response


def _check_health(config):
    try:
        df = RiskIQDigitalFootPrint(config)
        endpoint = 'v1/globalinventory/deltas'
        response = df.make_api_call(endpoint=endpoint, params={})
        if response:
            logger.info('connector available')
            return True
    except Exception as err:
        logger.exception(str(err))
        raise ConnectorError(str(err))


operations = {
    'add_assets': add_assets,
    'get_assets_by_type': get_assets_by_type,
    'get_assets_by_uuid': get_assets_by_uuid,
    'update_assets': update_assets,
    'get_connected_asset': get_connected_asset,
    'get_task_status': get_task_status,
    'get_changed_asset': get_changed_asset,
    'get_changed_asset_summary': get_changed_asset_summary
}
