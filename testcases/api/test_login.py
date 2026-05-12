import pytest
import json

from pydantic_core.core_schema import json_or_python_schema

from common.assert_util import assert_response
from common.config import config
from common.request_util import RequestUtil

API_KEY = config["api_key"]
url=config["base_url"]
headers = {
        "x-api-key": API_KEY
    }
def load_test_data(path):
    with open(path,"r",encoding="utf-8") as f:
        return json.load(f)
@pytest.mark.api
@pytest.mark.login
#测试用例参数化  --- 掌握基本测试写法
@pytest.mark.parametrize("case",load_test_data("data/api_test_data.json"))
def test_register(case):
    res=RequestUtil.send_method(url,"POST",headers=headers,data=case["data"])
    print(res.json())

    assert_response(res,case["expected"])