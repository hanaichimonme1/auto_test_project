#断言封装
def assert_response(res,expected_status):
    assert res.status_code==expected_status

    res_json=res.json()
    if res.status_code==200:
        assert "token" in res_json
    else:
        assert "error" in res_json