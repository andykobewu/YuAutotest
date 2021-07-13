import pytest
from selenium import webdriver
from common.reader_yml import readerYml

# @pytest.fixture(scope='package',autouse=True)
driver_path=readerYml().get_path()
url_path=readerYml().get_url()
