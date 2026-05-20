def assert_response(res,expected_status,**expected_fields):
    """
        通用接口响应断言。
        用法：assert_response(res, 200, success=True, message="登录成功")
        """
    assert res.status_code == expected_status,(
        f"期望状态码{expected_status}，实际状态码{res.status_code}，响应{res.text}"
    )
    res_json=res.json()
    for key,value in expected_fields.items():
        assert key in res_json,(
            f"缺少字段{key}，响应{res.text}"
        )
        assert res_json[key] == value,(
            f"字段{key}期望值{value}，实际值{res_json[key]}"
        )