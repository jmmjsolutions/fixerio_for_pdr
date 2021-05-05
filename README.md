# fixerio_for_pdr
Fixer is a simple and lightweight API for current and historical foreign exchange (forex) rates. 
Free registration is required to get an API key. The free subscription is restricted to a base
currency of EUR.
 
The Pandas datareader (https://pandas-datareader.readthedocs.io/) is a pydata package that allows a pandas user to create a dataframe 
from various internet datasources, currently including: Yahoo! Finance. Google Finance.

This package allows the pandas_datareader to use the fixer api to request historical forex rates for a specific day and range of currencies.

## Installation

The package can be installed from [GitHub](https://github.com/jmmjsolutions/fixerio_for_pdr) using [pip](http://www.pip-installer.org)
    
    pip install git+https://github.com/jmmjsolutions/fixerio_for_pdr.git


... or download the source distribution from [GitHub](https://github.com/jmmjsolutions/fixerio_for_pdr/archive/master.zip), unarchive, and run

    python setup.py install

## Usage

The Fixer.io api access key either is read from the environment variable FIXERIO_API_KEY or passed via the api_key keyword argument. 
The API key is *mandatory*.
```py
  import pandas_datareader as pdr
  import fixerio_for_pdr

  df = pdr.get_exchange_rate_fixerio(symbols='AUD')

  print(df)
          Date    ExRate
AUD 2021-05-04  1.559358

```

## Requirements

Using the fixerio for panadas datareader requires the following packages:

* pandas>=1.2.4
* pandas_datareader>=0.9.0
* lxml
* requests>=2.25.0

Development and testing requires the following additional packages:

* pytest
* pytest-mock
* pytest-cov
* black