import json
import os
import pickle
import sys
import time
import uuid

import requests

import friartuck_config

class FriarTuck:
    def __init__(self, mfa_code=None):
        # Robinhood Login credentials
        self._username = friartuck_config.ROBINHOOD_USERNAME
        self._password = friartuck_config.ROBINHOOD_PASSWORD
        self._mfa_code = mfa_code

        # Authorization timeout constraints
        self._session_expiration_seconds = friartuck_config.SESSION_EXPIRATION_SECONDS
        self._session_expiration_tolerance = friartuck_config.SESSION_EXPIRATION_TOLERANCE

        # Authorization persistence
        self._session_file = friartuck_config.SESSION_FILE

        # HTTPS Session
        # pickle file documentation
        # {"token_type": strint, 
        # "access_token": string, 
        # "expiration_epoch": float,
        # "refresh_token": string, 
        # "expiration_epoch_timestamp": float}
        self._session_data = {}
        self._session = requests.session()
        self._session.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0",
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

        # Load persistent auth and verify that it's not close to timeout
        try:
            # Load existing auth token
            self._load_session()

            # Throw error if existing session is expiring within expiration tolerance (expiring soon)
            if (self._session_data['expiration_epoch_timestamp'] - time.time()) < self._session_expiration_tolerance:
                print("Session is expiring within time constraints. Must refresh auth token.")
                raise Exception("Session is expiring within time constraints. Must refresh auth token.")

            # Set authorization headers to persisent auth data
            self._set_authorization_headers()

            # Verify valid access_token server-side
            self.get_portfolio_info()
            print("Persistent access successful.")
            return
        except:
            print("Persistent access failed. Must refresh login.")
            pass

        # Login with new MFA code
        if not self._login_with_mfa():
            print("Error loggin in with mfa code. Please report bug.")
        else:
            pass

        # Store new session data
        self._store_session_data()

        # Set auth headers with new auth token
        self._set_authorization_headers()
        self.get_portfolio_info()
        print("New login auth succesful. New headers set.")

    def _load_session(self):
        # Load pickle file
        with open(self._session_file, 'rb') as file:
            self._session_data = pickle.load(file)

    def _set_authorization_headers(self):
        self._session.headers['Authorization'] = f"{self._session_data['token_type']} {self._session_data['access_token']}"
        
    def _login_with_mfa(self):
        url = "https://api.robinhood.com/oauth2/token/"

        payload = {
            "device_token": f"{uuid.uuid4()}",
            "client_id": "c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS",
            "expires_in": self._session_expiration_seconds,
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

            try:
                if res["detail"]:
                    if res["detail"] == "Please enter a valid code.":
                        mfa = input("Enter MFA code: ")
                        payload["mfa_code"] = int(mfa)
                        continue
                    else:
                        print("Login mfa error. Code is malfunctioning. Please make a bug report. Exiting.")
                        sys.exit()
            except:
                pass

            if res["access_token"] and res["token_type"]:
                self._session_data['token_type'] = res['token_type']
                self._session_data['access_token'] = res['access_token']
                self._session_data['refresh_token'] = res['refresh_token']
                self._session_data['expires_in'] = int(res['expires_in'])
                self._session_data['expiration_epoch_timestamp'] = time.time() + float(self._session_data['expires_in'])
                print("Succesfully set new session_data info.")
                return True

    def _store_session_data(self):
        with open(self._session_file, 'wb') as file:
            pickle.dump(self._session_data, file)

    def logout(self):
        url = "https://api.robinhood.com/oauth2/revoke_token/"

        payload = {
            "client_id": "c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS",
            "token": self._session_data["access_token"]
        }

        json_payload = json.dumps(payload)
        
        # HTTPS revoke token
        res = self._session.post(url, data=json_payload)

        # Remove persistent auth data
        os.remove(self._session_file)

    def get_open_option_orders(self):
        url = "https://api.robinhood.com/options/orders/?states=queued,new,confirmed,unconfirmed,partially_filled,pending_cancelled"

        res = self._session.get(url)
        return res.json()

    def get_portfolio_info(self):
        url = "https://api.robinhood.com/accounts/"

        res = self._session.get(url)
        return res.json()

    def load_portfolio_profile(self):
        pass

    def load_account_profile(self):
        pass

    def get_day_trades(self):
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

