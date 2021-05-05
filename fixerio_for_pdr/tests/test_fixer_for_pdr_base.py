import os
from datetime import datetime, timedelta

import pandas as pd
import pytest

from fixerio_for_pdr import Fixer

TEST_API_KEY = "af3f0000fffefddc5d48f5879c0fefe"  # Not a real key

TEST_ENV_API_KEY = os.getenv("FIXERIO_API_KEY")


class TestFixerBase(object):
    @classmethod
    def setup_class(cls):
        pass

    @pytest.mark.skipif(
        TEST_ENV_API_KEY is not None,
        reason="The environment variable FIXERIO_API_KEY is set, so Fixer would use it as the api key.",
    )
    def test_fixer_raises_exception_on_missing_api_key(self):
        """
        GIVEN the fixerio api key is not set in the environment or passed as a parameter
        WHEN creating a Fixer instance
        THEN the ValueError exception must be raised
        """
        with pytest.raises(ValueError):
            fixer = Fixer()

    def test_fixer_uses_api_key_from_env(self):
        """
        GIVEN the fixerio api key is set in the environment variable FIXERIO_API_KEY
        WHEN creating a Fixer instance
        THEN a Fixer instance will be created
        """
        os.environ["FIXERIO_API_KEY"] = TEST_API_KEY
        fixer = Fixer()
        assert fixer.api_key == TEST_API_KEY

    def test_fixer_uses_api_key_variable(self):
        """
        GIVEN the fixerio api key passed as a keyword argument
        WHEN creating a Fixer instance
        THEN a Fixer instance will be created
        """
        fixer = Fixer(api_key=TEST_API_KEY)
        assert fixer.api_key == TEST_API_KEY

    def test_fixer_sets_base_url(self):
        """
        GIVEN the fixerio api key passed as a keyword argument
        WHEN creating a Fixer instance
        THEN a Fixer instance url property equals the fixer.io data api url
        """
        fixer = Fixer()
        assert fixer.url == "http://data.fixer.io/api/"

    def test_fixer_sets_start_date_to_today(self):
        """
        GIVEN no start date
        WHEN creating a Fixer instance
        THEN the Fixer instance start date property equals UTC today
        """
        fixer = Fixer()
        assert fixer.start == datetime.utcnow().date()

    def test_fixer_sets_start_date_to_start_parameter(self):
        """
        GIVEN a start date
        WHEN creating a Fixer instance
        THEN the Fixer instance start date property equals the supplied start date
        """
        start_date = datetime.utcnow().date() - timedelta(days=5)
        fixer = Fixer(start=start_date)
        assert fixer.start == start_date
