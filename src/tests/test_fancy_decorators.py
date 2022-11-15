"""Tests for `fancy_decorators` package."""
import pytest
import importlib

from function_decorators import typetest, log_metrics

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

def test_sample():
    assert 1 < 2

def test_typecheck():
    '''Testing typecheck decorator'''
    try:
        @typetest(a=int)
        def foo(a, b):
            return a, b
            
        assert foo(a=1, b=2) == (1, 2)
        
    except Exception as e:
        pytest.fail(e)
