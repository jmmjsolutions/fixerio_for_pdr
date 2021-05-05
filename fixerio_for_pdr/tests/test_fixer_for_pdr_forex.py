import os
from datetime import datetime, timedelta

import pandas as pd
from pandas.testing import assert_index_equal
import pytest

import pandas_datareader as pdr
from pandas_datareader._utils import RemoteDataError
import fixerio_for_pdr

TEST_API_KEY = os.getenv("FIXERIO_API_KEY")


@pytest.mark.skipif(
    TEST_API_KEY is None,
    reason="The environment variable FIXERIO_API_KEY must be set with a valid Fixer API access key.",
)
class TestFixerForex(object):
    @classmethod
    def setup_class(cls):
        pass


    def test_single_bad_currency_quote_symbol_raises_exception(self):
        """
        GIVEN an invalid currency code
        WHEN the get_exchange_rate_fixerio method is called
        THEN the RemoteDataError exception must be raised
        """
        with pytest.raises(RemoteDataError):
            df = pdr.get_exchange_rate_fixerio(symbols="XXX", api_key=TEST_API_KEY)

    def test_single_currency_quote_symbol_no_start_date(self):
        """
        GIVEN a single currency code
        WHEN the get_exchange_rate_fixerio method is called
        THEN a dataframe with today's exchanges rate for the currency codes
        is returned
        """
        today = datetime.utcnow().date()
        df = pdr.get_exchange_rate_fixerio(symbols="AUD", api_key=TEST_API_KEY)
        assert isinstance(df, pd.DataFrame)
        assert len(df.index) == 1
        assert df.iloc[0][0] == today
        assert df.index == "AUD"

    def test_single_currency_quote_symbol_for_today(self):
        """
        GIVEN a single currency codes and a start date of today
        WHEN the get_exchange_rate_fixerio method is called
        THEN a dataframe with today's exchanges rate for the currency code
        is returned
        """
        today = datetime.utcnow().date()
        df = pdr.get_exchange_rate_fixerio(
            symbols="AUD", start=today, api_key=TEST_API_KEY
        )
        assert isinstance(df, pd.DataFrame)
        assert len(df.index) == 1
        assert df.iloc[0][0] == today
        assert df.index == "AUD"

    def test_single_currency_quote_symbol_for_yesterday(self):
        """
        GIVEN a single currency codes and a start date of today - 1 day
        WHEN the get_exchange_rate_fixerio method is called
        THEN a dataframe with yesterday (today - 1 day) exchange rate for the
        currency code is returned
        """
        yesterday = datetime.utcnow().date() - timedelta(days=1)
        df = pdr.get_exchange_rate_fixerio(
            symbols="AUD", start=yesterday, api_key=TEST_API_KEY
        )
        assert isinstance(df, pd.DataFrame)
        assert len(df.index) == 1
        assert df.iloc[0][0] == yesterday
        assert df.index == "AUD"

    def test_multiple_bad_currency_quote_symbols_raises_exception(self):
        """
        GIVEN a list of all invalid currency codes
        WHEN the get_exchange_rate_fixerio method is called
        THEN the RemoteDataError exception must be raised
        """
        with pytest.raises(RemoteDataError):
            df = pdr.get_exchange_rate_fixerio(symbols=["XXX", "YYY", "ZZZ"])

    def test_multiple_good_and_bad_currency_quote_symbols(self, api_key=TEST_API_KEY):
        """
        GIVEN a list of valid and invalid currency codes
        WHEN the get_exchange_rate_fixerio method is called
        THEN a dataframe with today's exchanges rates for the valid currency codes
        is returned
        """
        today = datetime.utcnow().date()
        df = pdr.get_exchange_rate_fixerio(
            symbols=["AUD", "XXX", "GBP", "SGD", "YYY"], api_key=TEST_API_KEY
        )
        assert isinstance(df, pd.DataFrame)
        assert len(df.index) == 3
        assert df.iloc[0][0] == today
        assert_index_equal(df.index, pd.Index(["AUD", "GBP", "SGD"]))

    def test_multiple_currency_quote_symbols_no_start_date(self):
        """
        GIVEN a list of 4 valid currency codes
        WHEN the get_exchange_rate_fixerio method is called
        THEN a dataframe with today's exchanges rates for the currency codes
        is returned
        """
        today = datetime.utcnow().date()
        df = pdr.get_exchange_rate_fixerio(
            symbols=["AUD", "USD", "GBP", "SGD"], api_key=TEST_API_KEY
        )
        assert isinstance(df, pd.DataFrame)
        assert len(df.index) == 4
        assert df.iloc[0][0] == today
        assert_index_equal(df.index, pd.Index(["AUD", "GBP", "SGD", "USD"]))

    def test_multiple_currency_quote_symbols_for_today(self):
        """
        GIVEN a list of 4 valid currency codes and a start date of today
        WHEN the get_exchange_rate_fixerio method is called
        THEN a dataframe with today's exchanges rates for the currency codes
        is returned
        """
        today = datetime.utcnow().date()
        df = pdr.get_exchange_rate_fixerio(
            symbols=["AUD", "USD", "GBP", "SGD"], start=today, api_key=TEST_API_KEY
        )
        assert isinstance(df, pd.DataFrame)
        assert len(df.index) == 4
        assert_index_equal(df.index, pd.Index(["AUD", "GBP", "SGD", "USD"]))

    def test_no_currency_quote_symbol_no_start_date(self):
        """
        GIVEN no currency code or UTC start date
        WHEN the get_exchange_rate_fixerio method is called
        THEN a dataframe with today's exchanges rate for all
        currency codes is returned
        """
        today = datetime.utcnow().date()
        df = pdr.get_exchange_rate_fixerio(api_key=TEST_API_KEY)
        assert isinstance(df, pd.DataFrame)
        assert len(df.index) == 168
        assert df.iloc[0][0] == today
