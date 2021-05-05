import pandas as pd
from pandas_datareader._utils import RemoteDataError
from . import Fixer, FIXERIO_BASE_URL


class FixerForexReader(Fixer):
    """
    Returns DataFrame of the Fixer.io Foreign Exchange Rates
    data.

    Parameters
    ----------
    base_currency : str
        The base currency code
    symbols : str, array-like object (list, tuple, Series)
        A single currency code or list of the currency codes.
    start : string, int, date, datetime, Timestamp
        Starting UTC date. Parses many different kind of date
        representations (e.g., 'JAN-01-2010', '1/1/10', 'Jan, 1, 1980')
    end : string, int, date, datetime, Timestamp
        Ending UTC date. Parses many different kind of date
        representations (e.g., 'JAN-01-2010', '1/1/10', 'Jan, 1, 1980')
    retry_count : int, default 3
        Number of times to retry query request.
    pause : int, default 0.1
        Time, in seconds, to pause between consecutive queries of chunks. If
        single value given for symbol, represents the pause between retries.
    session : Session, default None
        requests.sessions.Session instance to be used
    api_key : str, optional
        Fixer.io API key . If not provided, the environment variable
        FIXERIO_API_KEY is read. The API key is *mandatory*.
    """

    def __init__(
        self,
        base_currency=None, # Currently not supported in Fixer.io free plan, will API force EUR as base
        symbols=None,
        start=None,
        end=None,  # Currently not supported in Fixer.io free plan
        retry_count=3,
        pause=0.1,
        session=None,
        api_key=None,
    ):
        super(FixerForexReader, self).__init__(
            base_currency=base_currency,
            symbols=symbols,
            start=start,
            end=end,
            retry_count=retry_count,
            pause=pause,
            session=session,
            api_key=api_key,
        )
        self.optional_params = {}
        if isinstance(symbols, str):
            self.symbols = [symbols]
        else:
            self.symbols = symbols

    @property
    def url(self):
        """API URL"""
        return FIXERIO_BASE_URL + self.function

    @property
    def function(self):
        """
        """
        return self.start.strftime('%Y-%m-%d')


    @property
    def data_key(self):
        """
        Set the key to extract the rates date from the API json response.
        """
        return "rates"

    @property
    def params(self):
        """
        Set parameters used for the API query string
        """
        params = {"access_key": self.api_key}
        if self.base_currency:
            params['base'] = self.base_currency
        if self.symbols:
            params['symbols'] = ",".join(self.symbols)
        params.update(self.optional_params)
        return params

    def _read_lines(self, out):
        """
        Create dataframe from rates data returned by API call.
        """
        try:
            df = pd.DataFrame.from_dict(out[self.data_key], orient="index", columns=['ExRate'])
        except KeyError:
            raise RemoteDataError()
        df.insert(0, "Date", self.start)
        df.sort_index(ascending=True, inplace=True)
        return df
