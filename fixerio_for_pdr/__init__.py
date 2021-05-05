import os
from datetime import datetime

import pandas as pd

from pandas_datareader.base import _BaseReader
import pandas_datareader as pdr

__version__ = '0.1.0'

FIXERIO_BASE_URL = "http://data.fixer.io/api/"


class Fixer(_BaseReader):
    """
    Base class for all Finder.io queries

    Parameters
    ----------
    base_currency : str
        The base currency code
    symbols : {str, List[str]}
        String symbol of like of symbols
    start : string, int, date, datetime, Timestamp
        Starting UTC date. Parses many different kind of date
        representations (e.g., 'JAN-01-2010', '1/1/10', 'Jan, 1, 1980')
    end : string, int, date, datetime, Timestamp
        Ending UTC date. Parses many different kind of date
        representations (e.g., 'JAN-01-2010', '1/1/10', 'Jan, 1, 1980')
    retry_count : int, default 3
        Number of times to retry a query request.
    pause : float, default 0.1
        Time, in seconds, of the pause between retries.
    session : Session, default None
        requests.sessions.Session instance to be used
    api_key : {str, None}
        Fixer.io API access key
        If not provided the environment variable
        FIXERIO_API_KEY is read. The API key is *mandatory*.

    Notes
    -----
    See `<Fixer https://fixer.io/documentation>`
    """

    _format = "json"

    def __init__(
        self,
        base_currency=None,
        symbols=None,
        start=None,
        end=None,
        retry_count=3,
        pause=0.1,
        session=None,
        api_key=None,
    ):
        if start is None:
            # Force date to UTC today when start is None
            start = datetime.utcnow().date()
        super(Fixer, self).__init__(
            symbols=symbols,
            start=start,
            end=end,
            retry_count=retry_count,
            pause=pause,
            session=session,
        )

        self.base_currency = base_currency 
        if api_key is None:
            api_key = os.getenv("FIXERIO_API_KEY")
            print(api_key)
        if not api_key or not isinstance(api_key, str):
            raise ValueError(
                """The Fixer.io API key must be provided
                either as the api_key variable or as the
                environment varible FIXERIO_API_KEY"""
            )
        self.api_key = api_key

    @property
    def url(self):
        """API URL"""
        return FIXERIO_BASE_URL

    @property
    def params(self):
        return {"function": self.function, "access_key": self.api_key}

    @property
    def function(self):
        """FixerIO endpoint function"""
        raise NotImplementedError

    @property
    def data_key(self):
        """Key of data returned fron Fixer.io endpoint"""
        raise NotImplementedError

    def _read_lines(self, out):
        raise NotImplementedError


from .forex import FixerForexReader

# Monkey patch pandas datareader as it does appear to support plugin feed extensions
def get_exchange_rate_fixerio(*args, **kwargs):
    return FixerForexReader(*args, **kwargs).read()


pdr.get_exchange_rate_fixerio = get_exchange_rate_fixerio
