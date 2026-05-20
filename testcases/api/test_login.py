import pytest
from common.assert_util import assert_response
from common.config import config
from common.data_util import load_json_data
from common.request_util import RequestUtil

url=config["base_url"]
@pytest.mark.api
@pytest.mark.login
#测试用例参数化  --- 掌握基本测试写法
@pytest.mark.parametrize("case",
                         load_json_data("data/api_test_data.json"),
                         ids=[c["name"] for c in load_json_data("data/api_test_data.json")])
def test_register(case):
    res=RequestUtil.send_method(url,"POST",data=case["data"])
    print(res.json())

    assert_response(res,case["expected"])