from common.request_util import RequestUtil
import pytest
@pytest.mark.api
@pytest.mark.login
def test_get_user(get_token):
    url = "https://reqres.in/api/users/2"
    headers={
        "Authorization":f"Bearer {get_token}"
    }

    res=RequestUtil.send_method(url,"GET",headers=headers)

    print(res.json())
    assert res.status_code == 200
    assert "data" in res.json()