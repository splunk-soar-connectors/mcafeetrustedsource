import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult

import sys
import requests
import json

from bs4 import BeautifulSoup
from mcafeets_consts import *


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


def setup():
    headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5)',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9,de;q=0.8'
              }

    base_url = 'http://www.trustedsource.org/sources/index.pl'
    r = requests.get(base_url, headers=headers)

    bs = BeautifulSoup(r.content, "html.parser")
    form = bs.find("form", { "class": "contactForm" })
    token1 = form.find("input", {'name': 'e'}).get('value')
    token2 = form.find("input", {'name': 'c'}).get('value')

    headers['Referer'] = base_url
    return headers, token1, token2


def lookup(headers, token1, token2, url):
    payload = {'e': (None, token1),
               'c': (None, token2),
               'action': (None, 'checksingle'),
               'product': (None, '01-ts'),
               'url': (None, url)}

    r = requests.post('https://www.trustedsource.org/en/feedback/url', headers=headers, files=payload)

    bs = BeautifulSoup(r.content, "html.parser")

    table = bs.find("table", { "class": "result-table" })
    td = table.find_all('td')
    categorized = td[len(td) - 3].text
    category = td[len(td) - 2].text[2:]
    risk = td[len(td) - 1].text

    return categorized, category, risk


class McAfeeTs(BaseConnector):

    def __init__(self):

        super(McAfeeTs, self).__init__()
        self._state = None
        self._base_url = None

    def initialize(self):

        self._state = self.load_state()
        return phantom.APP_SUCCESS

    def _handle_test_connectivity(self, param):

        action_result = self.add_action_result(ActionResult(dict(param)))

        self.save_progress("Testing the McAfee TrustedSource connectivity")

        base_url = 'http://www.trustedsource.org/sources/index.pl'
        r = requests.get(base_url)

        if r.status_code == 200:
            return self.set_status_save_progress(phantom.APP_SUCCESS, TS_SUCC_CONNECTIVITY_TEST)

        else:
            return action_result.set_status(phantom.APP_ERROR, TS_ERR_CONNECTION)

    def _handle_lookup_url(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        lookup_url = param[TS_LOOKUP_URL]

        try:
            headers, token1, token2 = setup()
            categorized, category, risk = lookup(headers, token1, token2, lookup_url)

            if risk == 'Unverified':
                score = 0
            elif risk == 'Minimal Risk':
                score = 1
            elif risk == 'Medium Risk':
                score = 2
            elif risk == 'High Risk':
                score = 3
            else:
                return action_result.set_status(phantom.APP_ERROR, "Invalid URL")

            result = {
                        'status': categorized,
                        'category': category,
                        'risk': risk,
                        'score': score
                     }

            action_result.add_data(result)
            action_result.set_status(phantom.APP_SUCCESS, TS_SUCC_QUERY)

        except Exception as e:
            action_result.set_status(phantom.APP_ERROR, TS_ERR_CONNECTION + str(e))
            return action_result.get_status()

        return action_result.get_status()

    def handle_action(self, param):

        ret_val = phantom.APP_SUCCESS

        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)
        elif action_id == 'lookup_url':
            ret_val = self._handle_lookup_url(param)

        return ret_val


if __name__ == '__main__':

    import pudb
    pudb.set_trace()

    if (len(sys.argv) < 2):
        print "No JSON specified as input"
        exit(0)

    with open(sys.argv[1]) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = McAfeeTs()
        connector.print_progress_message = True
        ret_val = connector._handle_action(json.dumps(in_json), None)
        print (json.dumps(json.loads(ret_val), indent=4))

    exit(0)
