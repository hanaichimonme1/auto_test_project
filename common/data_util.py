import json
from pathlib import Path


def load_json_data(file_path):
    """
    读取 JSON 测试数据。
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"测试数据文件不存在: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_login_cases(cases):
    """
    校验登录用例数据格式。
    """
    required_fields = ["case_name", "username", "password", "expected_message"]

    for index, case in enumerate(cases, start=1):
        for field in required_fields:
            if field not in case:
                case_name = case.get("case_name", "未命名用例")
                raise ValueError(
                    f"第 {index} 条测试数据缺少字段: {field}，用例名: {case_name}"
                )