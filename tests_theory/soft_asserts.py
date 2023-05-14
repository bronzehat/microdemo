# -*- coding: utf-8 -*-
"""
This module shows soft asserts with the help of
pytest-check plugin.

Here we open russian version of Wiki page and
are redirected. Some checks will pass, some will
fail, some of them won't run because of fails
before them.
"""

import pytest_check as check
import logging
import requests

from urllib.parse import unquote


log = logging.getLogger()
log.setLevel(logging.DEBUG)

WIKI_URL = 'https://ru.wikipedia.org/wiki'
REDIRECT_PAGE = '/Заглавная_страница'


@check.check_func
def check_redirect(response):
    # This check should fail
    check.is_false(response.history, 'Request was redirected')
    if response.history:
        for resp in response.history:
            # This check should fail
            check.is_(
                resp.status_code, 200,
                'Unexpected status code for redirected source '
                f'{resp.url}')


@check.check_func
def check_response_url(response):
    #  This check should fail
    check.is_not_in(
        REDIRECT_PAGE, unquote(response.url),
        'Redirected page has unexpected name')


def test_wiki():
    response = requests.get(WIKI_URL)
    # This check should pass
    check.is_(response.status_code, 200)
    # This check should fail
    check_redirect(response)
    if not check.any_failures():
        # This check will not run because
        # there are failures before it
        check_response_url(response)
    else:
        log.debug('Did not check response url')
