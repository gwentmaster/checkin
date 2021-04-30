# -*- coding: utf-8 -*-
# @Date    : 2021-04-24 16:31:25
# @Author  : gwentmaster(gwentmaster@vivaldi.net)
# I regret in my life


import json
import logging
import os
import traceback

import httpx


def chicken_checkin() -> None:
    """几鸡签到
    """

    logger = logging.getLogger("chicken")

    client = httpx.Client()
    email = os.environ["CHICKEN_MAIL"]
    passwd = os.environ["CHICKEN_PASSWORD"]

    login_resp = None
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


if __name__ == "__main__":

    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)

    for func in (chicken_checkin, ):
        try:
            func()
        except Exception as e:
            logger.info(traceback.format_exc())
            raise e
