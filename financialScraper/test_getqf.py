import pytest
from getqf import *

def test_get_data():
	stocklist = ['XOM']

	datalist = get_data(stocklist)
	