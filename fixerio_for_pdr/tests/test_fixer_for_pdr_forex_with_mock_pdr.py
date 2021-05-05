import os
from datetime import datetime, timedelta
import json

import pandas as pd
from pandas.testing import assert_index_equal
import pytest

import pandas_datareader as pdr
from pandas_datareader._utils import RemoteDataError
import fixerio_for_pdr

TEST_API_KEY = os.getenv("FIXERIO_API_KEY")


class MockResponse:
    def __init__(self, response={}):
        self.mock_response = response

    def json(self):
        """
        Mock json() method returns the init response like dict
        """
        return self.mock_response


class TestFixerForexMockAPI(object):
    """
    Test fixer forex class using mock api endpoint
    """

    @classmethod
    def setup_class(cls):
        pass

    def test_single_bad_currency_quote_symbol_raises_exception(self, monkeypatch):
        """
        GIVEN an invalid currency code
        WHEN the get_exchange_rate_fixerio method is called
        THEN the RemoteDataError exception must be raised
        """

        def mock_get_response(*args, **kwargs):
            return MockResponse(
                {
                    "success": False,
                    "error": {
                        "code": 202,
                        "type": "invalid_currency_codes",
                        "info": "You have provided one or more invalid Currency Codes. [Required format: currencies=EUR,USD,GBP,...]",
                    },
                }
            )

        monkeypatch.setattr(pdr.base._BaseReader, "_get_response", mock_get_response)
        with pytest.raises(RemoteDataError):
            df = pdr.get_exchange_rate_fixerio(symbols="XXX", api_key=TEST_API_KEY)

    def test_single_currency_quote_symbol_no_start_date(self, monkeypatch):
        """
        GIVEN a single currency code
        WHEN the get_exchange_rate_fixerio method is called
        THEN a dataframe with today's exchanges rate for the currency codes
        is returned
        """
        today = datetime.utcnow().date()

        def mock_get_response(*args, **kwargs):
            return MockResponse(
                {
                    "success": True,
                    "timestamp": 1620189484,
                    "historical": True,
                    "base": "EUR",
                    "date": today.strftime("%Y-%m-%d"),
                    "rates": {"AUD": 1.554834},
                }
            )

        monkeypatch.setattr(pdr.base._BaseReader, "_get_response", mock_get_response)

        df = pdr.get_exchange_rate_fixerio(symbols="AUD", api_key=TEST_API_KEY)
        assert isinstance(df, pd.DataFrame)
        assert len(df.index) == 1
        assert df.iloc[0][0] == today
        assert df.index == "AUD"

    def test_single_currency_quote_symbol_for_yesterday(self, monkeypatch):
        """
        GIVEN a single currency codes and a start date of today - 1 day
        WHEN the get_exchange_rate_fixerio method is called
        THEN a dataframe with yesterday (today - 1 day) exchange rate for the
        currency code is returned
        """
        yesterday = datetime.utcnow().date() - timedelta(days=1)

        def mock_get_response(*args, **kwargs):
            return MockResponse(
                {
                    "success": True,
                    "timestamp": 1620189484,
                    "historical": True,
                    "base": "EUR",
                    "date": yesterday.strftime("%Y-%m-%d"),
                    "rates": {"AUD": 1.554834},
                }
            )

        monkeypatch.setattr(pdr.base._BaseReader, "_get_response", mock_get_response)
        df = pdr.get_exchange_rate_fixerio(
            symbols="AUD", start=yesterday, api_key=TEST_API_KEY
        )
        assert isinstance(df, pd.DataFrame)
        assert len(df.index) == 1
        assert df.iloc[0][0] == yesterday
        assert df.index == "AUD"

    def test_multiple_bad_currency_quote_symbols_raises_exception(self, monkeypatch):
        """
        GIVEN a list of all invalid currency codes
        WHEN the get_exchange_rate_fixerio method is called
        THEN the RemoteDataError exception must be raised
        """

        def mock_get_response(*args, **kwargs):
            return MockResponse(
                {
                    "success": False,
                    "error": {
                        "code": 202,
                        "type": "invalid_currency_codes",
                        "info": "You have provided one or more invalid Currency Codes. [Required format: currencies=EUR,USD,GBP,...]",
                    },
                }
            )

        monkeypatch.setattr(pdr.base._BaseReader, "_get_response", mock_get_response)
        with pytest.raises(RemoteDataError):
            df = pdr.get_exchange_rate_fixerio(symbols=["XXX", "YYY", "ZZZ"])

    def test_multiple_good_and_bad_currency_quote_symbols(self, monkeypatch):
        """
        GIVEN a list of valid and invalid currency codes
        WHEN the get_exchange_rate_fixerio method is called
        THEN a dataframe with today's exchanges rates for the valid currency codes
        is returned
        """
        today = datetime.utcnow().date()

        def mock_get_response(*args, **kwargs):
            return MockResponse(
                {
                    "success": True,
                    "timestamp": 1620191404,
                    "historical": True,
                    "base": "EUR",
                    "date": today.strftime("%Y-%m-%d"),
                    "rates": {"AUD": 1.55551, "GBP": 0.864508, "SGD": 1.60588},
                }
            )

        monkeypatch.setattr(pdr.base._BaseReader, "_get_response", mock_get_response)
        df = pdr.get_exchange_rate_fixerio(
            symbols=["AUD", "XXX", "GBP", "SGD", "YYY"], api_key=TEST_API_KEY
        )
        assert isinstance(df, pd.DataFrame)
        assert len(df.index) == 3
        assert df.iloc[0][0] == today
        assert_index_equal(df.index, pd.Index(["AUD", "GBP", "SGD"]))

    def test_multiple_currency_quote_symbols_no_start_date(self, monkeypatch):
        """
        GIVEN a list of 4 valid currency codes
        WHEN the get_exchange_rate_fixerio method is called
        THEN a dataframe with today's exchanges rates for the currency codes
        is returned
        """
        today = datetime.utcnow().date()

        def mock_get_response(*args, **kwargs):
            return MockResponse(
                {
                    "success": True,
                    "timestamp": 1620191583,
                    "historical": True,
                    "base": "EUR",
                    "date": today.strftime("%Y-%m-%d"),
                    "rates": {
                        "AUD": 1.555819,
                        "USD": 1.20215,
                        "GBP": 0.864592,
                        "SGD": 1.606037,
                    },
                }
            )

        monkeypatch.setattr(pdr.base._BaseReader, "_get_response", mock_get_response)
        df = pdr.get_exchange_rate_fixerio(
            symbols=["AUD", "USD", "GBP", "SGD"], api_key=TEST_API_KEY
        )
        assert isinstance(df, pd.DataFrame)
        assert len(df.index) == 4
        assert df.iloc[0][0] == today
        assert_index_equal(df.index, pd.Index(["AUD", "GBP", "SGD", "USD"]))

    def test_multiple_currency_quote_symbols_for_today(self, monkeypatch):
        """
        GIVEN a list of 4 valid currency codes and a start date of today
        WHEN the get_exchange_rate_fixerio method is called
        THEN a dataframe with today's exchanges rates for the currency codes
        is returned
        """
        today = datetime.utcnow().date()

        def mock_get_response(*args, **kwargs):
            return MockResponse(
                {
                    "success": True,
                    "timestamp": 1620191583,
                    "historical": True,
                    "base": "EUR",
                    "date": today.strftime("%Y-%m-%d"),
                    "rates": {
                        "AUD": 1.555819,
                        "USD": 1.20215,
                        "GBP": 0.864592,
                        "SGD": 1.606037,
                    },
                }
            )

        monkeypatch.setattr(pdr.base._BaseReader, "_get_response", mock_get_response)
        df = pdr.get_exchange_rate_fixerio(
            symbols=["AUD", "USD", "GBP", "SGD"], start=today, api_key=TEST_API_KEY
        )
        assert isinstance(df, pd.DataFrame)
        assert len(df.index) == 4
        assert_index_equal(df.index, pd.Index(["AUD", "GBP", "SGD", "USD"]))

    def test_no_currency_quote_symbol_no_start_date(self, monkeypatch):
        """
        GIVEN no currency code or UTC start date
        WHEN the get_exchange_rate_fixerio method is called
        THEN a dataframe with today's exchanges rate for all
        currency codes is returned
        """
        today = datetime.utcnow().date()

        def mock_get_response(*args, **kwargs):
            return MockResponse(
                {
                    "success": True,
                    "timestamp": 1620192184,
                    "historical": True,
                    "base": "EUR",
                    "date": today.strftime("%Y-%m-%d"),
                    "rates": {
                        "AED": 4.414284,
                        "AFN": 94.091581,
                        "ALL": 123.155892,
                        "AMD": 625.227609,
                        "ANG": 2.155678,
                        "AOA": 786.316145,
                        "ARS": 112.632781,
                        "AUD": 1.555687,
                        "AWG": 2.164468,
                        "AZN": 2.038748,
                        "BAM": 1.955447,
                        "BBD": 2.424725,
                        "BDT": 101.831166,
                        "BGN": 1.955682,
                        "BHD": 0.45307,
                        "BIF": 2341.471648,
                        "BMD": 1.201815,
                        "BND": 1.603786,
                        "BOB": 8.280279,
                        "BRL": 6.543043,
                        "BSD": 1.200865,
                        "BTC": 2.1964123e-05,
                        "BTN": 88.690142,
                        "BWP": 13.081839,
                        "BYN": 3.084096,
                        "BYR": 23555.568909,
                        "BZD": 2.420626,
                        "CAD": 1.477307,
                        "CDF": 2404.830981,
                        "CHF": 1.09745,
                        "CLF": 0.030654,
                        "CLP": 845.852826,
                        "CNY": 7.780072,
                        "COP": 4602.349548,
                        "CRC": 740.045133,
                        "CUC": 1.201815,
                        "CUP": 31.848091,
                        "CVE": 110.243419,
                        "CZK": 25.848699,
                        "DJF": 213.78815,
                        "DKK": 7.436048,
                        "DOP": 68.283633,
                        "DZD": 160.736266,
                        "EGP": 18.833309,
                        "ERN": 18.029518,
                        "ETB": 51.0854,
                        "EUR": 1,
                        "FJD": 2.45221,
                        "FKP": 0.872968,
                        "GBP": 0.864531,
                        "GEL": 4.133954,
                        "GGP": 0.872968,
                        "GHS": 6.929244,
                        "GIP": 0.872968,
                        "GMD": 61.502873,
                        "GNF": 11871.576094,
                        "GTQ": 9.271602,
                        "GYD": 251.250817,
                        "HKD": 9.335649,
                        "HNL": 28.846353,
                        "HRK": 7.541381,
                        "HTG": 104.335576,
                        "HUF": 359.811218,
                        "IDR": 17340.744524,
                        "ILS": 3.921029,
                        "IMP": 0.872968,
                        "INR": 88.699336,
                        "IQD": 1752.127015,
                        "IRR": 50602.409328,
                        "ISK": 149.902709,
                        "JEP": 0.872968,
                        "JMD": 183.661048,
                        "JOD": 0.85205,
                        "JPY": 131.364346,
                        "KES": 128.952463,
                        "KGS": 101.903555,
                        "KHR": 4860.048627,
                        "KMF": 492.264131,
                        "KPW": 1081.633497,
                        "KRW": 1352.378159,
                        "KWD": 0.362251,
                        "KYD": 1.000704,
                        "KZT": 514.479289,
                        "LAK": 11300.587868,
                        "LBP": 1815.744561,
                        "LKR": 236.579289,
                        "LRD": 206.711899,
                        "LSL": 17.402344,
                        "LTL": 3.548646,
                        "LVL": 0.726966,
                        "LYD": 5.393644,
                        "MAD": 10.744497,
                        "MDL": 21.376216,
                        "MGA": 4562.386896,
                        "MKD": 61.587944,
                        "MMK": 1870.417359,
                        "MNT": 3425.956054,
                        "MOP": 9.608319,
                        "MRO": 429.047656,
                        "MUR": 48.733119,
                        "MVR": 18.447708,
                        "MWK": 952.922462,
                        "MXN": 24.286819,
                        "MYR": 4.947838,
                        "MZN": 69.212691,
                        "NAD": 17.402523,
                        "NGN": 457.287798,
                        "NIO": 41.94179,
                        "NOK": 9.998486,
                        "NPR": 141.895223,
                        "NZD": 1.677271,
                        "OMR": 0.462659,
                        "PAB": 1.200865,
                        "PEN": 4.583303,
                        "PGK": 4.216675,
                        "PHP": 57.699723,
                        "PKR": 183.379003,
                        "PLN": 4.555311,
                        "PYG": 7926.748309,
                        "QAR": 4.375811,
                        "RON": 4.92816,
                        "RSD": 117.601979,
                        "RUB": 89.797069,
                        "RWF": 1201.974709,
                        "SAR": 4.507288,
                        "SBD": 9.564819,
                        "SCR": 18.05187,
                        "SDG": 471.110841,
                        "SEK": 10.186065,
                        "SGD": 1.605829,
                        "SHP": 0.872968,
                        "SLL": 12300.574338,
                        "SOS": 701.859439,
                        "SRD": 17.010469,
                        "STD": 24912.583638,
                        "SVC": 10.507943,
                        "SYP": 1511.363049,
                        "SZL": 17.364601,
                        "THB": 37.520759,
                        "TJS": 13.69733,
                        "TMT": 4.21837,
                        "TND": 3.307998,
                        "TOP": 2.721871,
                        "TRY": 10.006568,
                        "TTD": 8.146505,
                        "TWD": 33.615363,
                        "TZS": 2787.008564,
                        "UAH": 33.403461,
                        "UGX": 4269.264276,
                        "USD": 1.201815,
                        "UYU": 52.621202,
                        "UZS": 12626.298355,
                        "VEF": 256984313118.49634,
                        "VND": 27713.84791,
                        "VUV": 131.64542,
                        "WST": 3.042667,
                        "XAF": 655.828619,
                        "XAG": 0.045491,
                        "XAU": 0.000676,
                        "XCD": 3.247965,
                        "XDR": 0.837636,
                        "XOF": 655.828619,
                        "XPF": 119.695994,
                        "YER": 300.964418,
                        "ZAR": 17.34477,
                        "ZMK": 10817.777865,
                        "ZMW": 26.840346,
                        "ZWL": 386.984581,
                    },
                }
            )

        monkeypatch.setattr(pdr.base._BaseReader, "_get_response", mock_get_response)
        df = pdr.get_exchange_rate_fixerio(api_key=TEST_API_KEY)
        assert isinstance(df, pd.DataFrame)
        assert len(df.index) == 168
        assert df.iloc[0][0] == today
