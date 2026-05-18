#封装请求工具，不然的话每次都要写requests.post，把发请求变成一个统一的入口
import requests
from common.config import config
from common.logger import get_logger
logger=get_logger() #获取日志对象
class RequestUtil:

    base_url=config["base_url"]
    api_key=config["api_key"]

    @staticmethod
    def send_method(url,method,headers=None,data=None,json=None):
        timeout=config.get("timeout",10)
        default_headers={
            "x-api-key":RequestUtil.api_key
        }
        if headers:
            default_headers.update(headers)

        logger.info(f"请求方式：{method}")
        logger.info(f"请求url：{url}")
        logger.info(f"请求参数：{data}")
        logger.info(f"请求头：{default_headers}")
        method=method.upper()
        if method=="GET":
            res=requests.get(url,
                             headers=default_headers,
                             data=data,
                             json=json,
                             timeout=timeout)
        elif method=="POST":
            res=requests.post(url,
                              headers=default_headers,
                              data=data,
                              json=json,
                              timeout=timeout)
        logger.info(f"响应状态码：{res.status_code}")
        logger.info(f"响应内容：{res.text}")
        return res