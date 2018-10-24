import logging
from json import JSONDecodeError

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def web_hook():
    pass


def set_web_hook():
    if settings.LOCALTUNNEL_URL != '':
        pass


def delete_user():
    pass


def user_list():
    pass


def edit_user():
    pass


def password_recovery():
    pass


def auth_user():
    pass


def add_user():
    pass


def _make_requests(**kwargs):
    """
    The method returns result query to API Telegram

    :param kwargs: method, url, json
    :return: json
    """
    res = requests.request(**kwargs)
    print(res)

    if res.status_code != 200:
        try:
            res = res.json()
            print(res)
        except JSONDecodeError:
            _raise_error('Ответ пришел не в Json формате!')

        if 'errors' in res:
            _raise_error(res['errors'][0]['message'], kwargs)
            return res
        else:
            _raise_error('Нет доступа!')
    else:
        try:
            res = res.json()
        except JSONDecodeError:
            _raise_error('Ответ пришел не в Json формате!')

    return res


def _raise_error(message_error, params=None):
    logger.error('Error requests', exc_info=True, extra={
        'params': params,
        'error': message_error,
    })
