# -*- coding: utf-8 -*-
# @Date    : 2021-04-24 16:31:25
# @Author  : gwentmaster(gwentmaster@vivaldi.net)
# I regret in my life


import json
import logging
import logging.config
import os
import re
import time
from hashlib import md5
from typing import List, Optional

import httpx


def chicken_checkin() -> None:
    """几鸡签到
    """

    logger = logging.getLogger("chicken")

    client = httpx.Client()
    email = os.environ["CHICKEN_MAIL"]
    passwd = os.environ["CHICKEN_PASSWORD"]

    login_resp = client.post(
        "http://j01.space/signin",
        headers={"Content-Type": "application/json;charset=UTF-8"},
        content=json.dumps(
            {"email": email, "passwd": passwd},
            separators=(",", ":")
        )
    )
    logger.info(login_resp.json())

    checkin_resp = client.post(
        "http://j01.space/user/checkin"
    )
    logger.info(checkin_resp.json())


def lovezhuoyou_checkin() -> None:
    """爱桌游签到
    """

    logger = logging.getLogger("lovezhuoyou")

    url = "https://www.lovezhuoyou.com/wp-admin/admin-ajax.php"

    client = httpx.Client()
    username = os.environ["LOVEZHUOYOU_USER"]
    password = os.environ["LOVEZHUOYOU_PASSWORD"]

    login_resp = client.post(
        url,
        data={
            "action": "user_login",
            "username": username,
            "password": password
        }
    )
    logger.info(login_resp.json())

    checkin_resp = client.post(
        url,
        data={"action": "user_qiandao"}
    )
    logger.info(checkin_resp.json())


def vgtime_checkin() -> None:
    """游戏时光签到
    """

    logger = logging.getLogger("vgtime")

    client = httpx.Client()
    username = os.environ["VGTIME_USER"]
    password = os.environ["VGTIME_PASSWORD"]

    ua = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        + "(KHTML, like Gecko) Chrome/90.0.4430.95 Safari/537.36"
    )

    login_resp = client.post(
        "http://www.vgtime.com/handle/login.jhtml",
        headers={"User-Agent": ua},
        data={
            "username": username,
            "password": password,
            "remember": "1"
        }
    )
    logger.info(login_resp.json()["message"])

    checkin_resp = client.post(
        "http://www.vgtime.com/uc/writesign.jhtml",
        headers={"User-Agent": ua}
    )
    logger.info(checkin_resp.json()["message"])


def iyingdi_checkin() -> None:
    """旅法师营地签到
    """

    client = httpx.Client()

    username = os.environ["IYINGDI_USER"]
    password = os.environ["IYINGDI_PASSWORD"]
    timestamp = str(int(time.time()))
    key = "b8d5b38577b8bb382b0c783b474b95f9"

    sign_material = ""
    for k, v in {
        "password": password,
        "timestamp": timestamp,
        "type": "password",
        "username": username,
        "key": key
    }.items():
        sign_material += f"&{k}={v}"
    sign = md5(sign_material.encode()).hexdigest()

    login_resp = client.post(
        "https://api.iyingdi.com/web/user/login",
        headers={
            "Login-Token": "nologin",
            "Platform": "pc"
        },
        data={
            "username": username,
            "password": password,
            "timestamp": timestamp,
            "type": "password",
            "sign": sign
        }
    )

    cookies = {"yd_token": login_resp.json()["login_token"]}
    client.cookies.update({k: str(v) for k, v in cookies.items()})

    artical_resp = client.get("https://www.iyingdi.com/tz/tag/19")
    search = re.search(r"/tz/post/\d+", artical_resp.content.decode("utf-8"))
    if search:
        client.get(f"https://www.iyingdi.com{search.group(0)}")


if __name__ == "__main__":

    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "logging.Formatter",
                "fmt": (
                    "[%(asctime)s]-[%(name)s]-[%(levelname)s]: %(message)s\n"
                ),
                "datefmt": "%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout"
            }
        },
        "loggers": {
            "": {"handlers": ["default"], "level": "INFO"},
        }
    })

    errors = []  # type: List[Optional[Exception]]
    for func in [
        chicken_checkin, lovezhuoyou_checkin, vgtime_checkin, iyingdi_checkin
    ]:
        try:
            func()
        except Exception as e:
            errors.append(e)

    for er in errors:
        if isinstance(er, Exception):
            raise er
