"""This is a test program."""

# coding:utf-8
#!/usr/bin/env python

import requests
import json
import yaml
import time
import hmac
import hashlib
import urllib
import base64
import myutils

class krakenfAPI():
    """
    docstring
    """

    def __init__(self):
        self.base_url = "https://api.kraken.com"
        with open('config.yml', 'r') as yml:
            self.config = yaml.load(yml)


    def get_ticker(self):
        """
        docstring
        """
        params = {'pair': 'XXBTZJPY'}
        response = requests.get(self.base_url + "/0/public/Ticker", params=params)

        if response.status_code != 200:
            raise Exception('return status code is {}'.format(response.status_code))
        ticker = json.loads(response.text)
        bid = float(ticker["result"]["XXBTZJPY"]["b"][0])
        ask = float(ticker["result"]["XXBTZJPY"]["a"][0])

        print "kraken_ask :" + str(ask)
        print "kraken_bid :" + str(bid)

        return ask, bid

    def ask(self, rate, amount):
        """
        Uncertain
        """
        nonce = myutils.nonce()
        url_path = "/0/private/AddOrder"

        data = {
            'pair': 'XXBTZJPY',
            'type': 'buy',
            'ordertype': 'market',
            'volume:': amount
        }
        '''
        data = {
            'pair': 'XXBTZJPY',
            'type': 'buy',
            'ordertype': 'limit',
            'price': rate,
            'volume:': amount
        }
        '''

        data["nonce"] = nonce

        signature = self._signature(nonce=nonce, url_path=url_path, data=data)
        #message  = url_path + hashlib.sha256(str(nonce) +  urllib.urlencode(data)).digest()
        #signature = hmac.new(base64.b64decode(self.config["kraken"]["API_SECRET"]), message, hashlib.sha512)

        headers = {
            'API-Key': self.config["kraken"]["ACCESS_KEY"],
            'ACCESS-SIGNATURE': signature,
            'ACCESS-NONCE': nonce
        }

        #response = requests.post(self.base_url + url_path, headers=headers, data=data)
        response = myutils.post(self.base_url + url_path, headers, data)

        return response


    def bid(self, rate, amount):
        """
        Uncertain
        """
        nonce = myutils.nonce()
        url_path = "/0/private/AddOrder"
        
        data = {
            'pair': 'XXBTZJPY',
            'type': 'sell',
            'ordertype': 'market',
            'volume:': amount
        }
        '''
        data = {
            'pair': 'XXBTZJPY',
            'type': 'sell',
            'ordertype': 'limit',
            'price': rate,
            'volume:': amount
        }
        '''

        data["nonce"] = nonce

        signature = self._signature(nonce=nonce, url_path=url_path, data=data)
        #message  = url_path + hashlib.sha256(str(nonce) +  urllib.urlencode(data)).digest()
        #signature = hmac.new(base64.b64decode(self.config["kraken"]["API_SECRET"]), message, hashlib.sha512)

        headers = {
            'API-Key': self.config["kraken"]["ACCESS_KEY"],
            'ACCESS-SIGNATURE': signature,
            'ACCESS-NONCE': nonce
        }

        #response = requests.get(self.base_url + url_path, headers=headers, data=data)
        response = myutils.post(self.base_url + url_path, headers, data)

        return response

    def get_barance(self):
        """
        Uncertain
        """
        nonce = myutils.nonce()
        url_path = "/0/private/Balance"

        data = {}
        data["nonce"] = nonce

        signature = self._signature(nonce=nonce, url_path=url_path, data=data)
        #message  = url_path + hashlib.sha256(str(nonce) +  urllib.urlencode(data)).digest()
        #signature = hmac.new(base64.b64decode(self.config["kraken"]["API_SECRET"]), message, hashlib.sha512)

        headers = {
            'API-Key': self.config["kraken"]["ACCESS_KEY"],
            'API-Sign': base64.b64encode(signature.digest())
        }

        #response = requests.post(self.base_url + url_path, headers=headers, data=data)
        response = myutils.post(self.base_url + url_path, headers, data)
        
        ticker = json.loads(response.text)
        print ticker
        #jpy = ticker["jpy"]
        #btc = ticker["btc"]

        #print "coincheck_amount jpy :" + str(jpy)
        #print "coincheck_amount btc :" + str(btc)

        #return jpy, btc

    def _signature(self, nonce=None, url_path=None, data=None):
        """
        docstring
        """
        _message  = url_path + hashlib.sha256(str(nonce) +  urllib.urlencode(data)).digest()
        _signature = hmac.new(base64.b64decode(self.config["kraken"]["API_SECRET"]), _message, hashlib.sha512)

        return _signature

    def get_incomplete_orders(self):
        """
        Uncertain
        """
        nonce = myutils.nonce()
        url_path = "/0/private/OpenOrders"

        data = {}
        data["nonce"] = nonce

        signature = self._signature(nonce=nonce, url_path=url_path, data=data)
        #message  = url_path + hashlib.sha256(str(nonce) +  urllib.urlencode(data)).digest()
        #signature = hmac.new(base64.b64decode(self.config["kraken"]["API_SECRET"]), message, hashlib.sha512)

        headers = {
            'API-Key': self.config["kraken"]["ACCESS_KEY"],
            'API-Sign': base64.b64encode(signature.digest())
        }

        #response = requests.post(self.base_url + url_path, headers=headers, data=data)
        response = myutils.post(self.base_url + url_path, headers, data)

        return response
        
    def cancel_all_order(self,ids):
        """
        Uncertain
        """

        response = {}
        for id in ids:
            nonce = myutils.nonce()
            url_path = "/0/private/CancelOrder"

            data = {"txid": id}
            data["nonce"] = nonce

            signature = self._signature(nonce=nonce, url_path=url_path, data=data)
            #message  = url_path + hashlib.sha256(str(nonce) +  urllib.urlencode(data)).digest()
            #signature = hmac.new(base64.b64decode(self.config["kraken"]["API_SECRET"]), message, hashlib.sha512)

            headers = {
                'API-Key': self.config["kraken"]["ACCESS_KEY"],
                'API-Sign': base64.b64encode(signature.digest())
            }

            #response = requests.post(self.base_url + url_path, headers=headers, data=data)
            response[id] = myutils.post(self.base_url + url_path, headers, data)

        return response


if __name__ == '__main__':
    api = krakenfAPI()
    api.get_ticker()
    api.get_barance()
    #pass
