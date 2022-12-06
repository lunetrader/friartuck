""" Friartuck: Python Robinhood API Wrapper """

######
# Current Robinhood API Version
# 1.431.4
######

######
# Basic usage
#
# Configuration settings are in friartuck_config.py
# import friartuck
# ft = friartuck.FriarTuck([mfa_code=123456]) # optional MFA code
# ft.portfolio_info() # example API call
# ft.logout() # optional, will require new mfa code on next run
######

######
# What is stored on my computer for persistent authentication?
#
# Default location ~/.friartuck/session
# You can change location in friartuck_config.py
#
# Pickle file: auth persistence
# {"token_type": "Bearer",
# "access_token": "Bearer access token (long string)",
# "refresh_token": "UUID variant token",
# "expires_in": float,
# "expiration_epoch_timestamp": float}
######

import json
import os
import pickle
import sys
import time
import uuid

import requests

import friartuck_config

class FriarTuck:
    """FriarTuck object handles all authentication and API calls."""
    def __init__(self, mfa_code=None):
        # Robinhood Login credentials
        self._username = friartuck_config.ROBINHOOD_USERNAME
        self._password = friartuck_config.ROBINHOOD_PASSWORD
        self._mfa_code = mfa_code

        # Authorization timeout constraints
        self._session_duration_seconds = \
            friartuck_config.SESSION_DURATION_SECONDS
        self._session_revoke_tolerance = \
            friartuck_config.SESSION_REVOKE_TOLERANCE

        # Authorization persistence
        self._session_file = friartuck_config.SESSION_FILE

        # Robinhood account ID
        self._robinhood_account_number = None

        # Session data
        # Recovered from pickle file or set with new login
        self._session_data = {}

        # Session and session headers
        self._session = requests.session()
        self._session.headers = {
            "User-Agent":
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; "
                "rv:108.0) Gecko/20100101 Firefox/108.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://robinhood.com/",
            "Content-Type": "application/json",
            "X-Robinhood-API-Version": "1.431.4",
            "Origin": "https://robinhood.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "TE": "trailers"
        }

        # Attempt persistent login
        try:
            self._load_session()
            if self._validate_expiration_tolerance() is False:
                msg = "Expiring to soon. New login."
                print(msg)
                raise Exception(msg)
            self._set_authorization_header()
            self._set_account_number()
            return
        # Attempt new login
        except:
            self._delete_session_data()
            self._login_with_mfa()
            if self._validate_expiration_tolerance() is False:
                msg = """
                    Session expiration timeout and tolerance settings 
                    are too close or reversed. Please check configuration.
                    Aborting login and exiting.
                """
                print(msg)
                sys.exit()
            self._set_authorization_header()
            self._set_account_number()
            self._store_session_data()

    def _load_session(self):
        with open(self._session_file, 'rb') as file:
            self._session_data = pickle.load(file)

    def _validate_expiration_tolerance(self):
        if self._session_data['expiration_epoch_timestamp'] - time.time() \
            < self._session_revoke_tolerance:
            return False
        else:
            return True

    def _set_authorization_header(self):
        self._session.headers['Authorization'] = f"{self._session_data['token_type']} {self._session_data['access_token']}"

    def _set_account_number(self):
        url = "https://api.robinhood.com/accounts/"
        res = self._session.get(url)
        account_number = res.json()["results"][0]["account_number"]
        self._robinhood_account_number = account_number

    def _login_with_mfa(self):
        url = "https://api.robinhood.com/oauth2/token/"

        payload = {
            "device_token": f"{uuid.uuid4()}",
            "client_id": "c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS",
            "expires_in": self._session_duration_seconds,
            "grant_type": "password",
            "scope": "internal",
            "username": self._username,
            "password": self._password,
            "try_passkeys": False,
            "mfa_code": self._mfa_code,
	        "al_pk": "7F867EDC-C71B-467F-B0A1-8DCBA5D4D2E3",
	        "al_token": "r=us-east-1"
        }

        while True:
            json_payload = json.dumps(payload)
            res = self._session.post(url, data=json_payload).json()

            # Try MFA codes repeatedly
            if "detail" in res:
                if res["detail"] == "Please enter a valid code.":
                    mfa = input("Enter MFA code: ")
                    payload["mfa_code"] = int(mfa)
                    continue

            # Successful response has access_token and token_type
            if "access_token" in res:
                # Set new session data
                print(res)
                self._session_data['token_type'] = res['token_type']
                self._session_data['access_token'] = res['access_token']
                self._session_data['refresh_token'] = res['refresh_token']
                self._session_data['expires_in'] = int(res['expires_in'])
                self._session_data['expiration_epoch_timestamp'] = \
                    time.time() + float(self._session_data['expires_in'])
                print("Succesfully set new in memory session_data info.")
                print("Returning...")
                return

    def _store_session_data(self):
        with open(self._session_file, 'wb') as file:
            pickle.dump(self._session_data, file)

    def _delete_session_data(self):
        if os.path.exists(self._session_file):
            os.remove(self._session_file)

    def _print_session_file(self):
        if os.path.exists(self._session_file):
            with open(self._session_file, 'rb') as file:
                print(pickle.load(file))

    def logout(self):
        """Logout and delete session data."""
        url = "https://api.robinhood.com/oauth2/revoke_token/"

        payload = {
            "client_id": "c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS",
            "token": self._session_data["access_token"]
        }

        json_payload = json.dumps(payload)
        
        # HTTPS revoke token
        res = self._session.post(url, data=json_payload)

        # Remove persistent auth data
        self._delete_session_data()

    def open_option_orders(self):
        url = "https://api.robinhood.com/options/orders/?states=queued,new,confirmed,unconfirmed,partially_filled,pending_cancelled"

        res = self._session.get(url)
        return res.json()

    def account_info(self):
        url = "https://api.robinhood.com/accounts/"
        res = self._session.get(url)
        return res.json()

    def portfolio_info(self):
        url = "https://api.robinhood.com/portfolios/"
        res = self._session.get(url)
        return res.json()

    def day_trades(self):
        #url = f"https://api.robinhood.com/accounts/{0}/recent_day_trades/'.format(account))
        pass

    def get_option_instrument_data_by_id(self, instr_id):
        pass

    def get_latest_ticker_price(self, ticker):
        pass

    def get_open_option_positions(self):
        pass

    def get_option_market_data_by_id(self, option_id):
        pass

    def get_chains(self, ticker):
        pass

    def find_tradable_options(self, ticker, expirationDate=None, optionType=''):
        pass

    def get_chains(self, ticker):
        pass

    def cancel_option_order_by_id(self, id=None):
        pass

    def order_buy_option_limit(self, openclose, debitcredit, limit, ticker, qty, exp, strike, optionType=None, timeInForce='gtc', jsonify=True):
        pass

    def order_sell_option_limit(self, closeopen, creditdebit, limit, ticker, qty, exp, strike, optionType=None, timeInForce='gtc', jsonify=True):
        pass

    def cancel_all_option_orders(self):
        pass

