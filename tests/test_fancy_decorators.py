#!/usr/bin/env python

"""Tests for `fancy_decorators` package."""

import pytest

from fancy_decorators import log_metrics

def test_metrics():
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

    from pandas import MultiIndex, DataFrame
    conf = {
        'a': [1]
    }

    keys = conf.keys()
    values = conf.values()
    midx = MultiIndex.from_product(list(values), names=list(keys))
    metrics = DataFrame(index=midx)

    @log_metrics(conf, metrics)
    def fn():
        print(1)
