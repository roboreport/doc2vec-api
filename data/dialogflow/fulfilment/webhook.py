# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import pymysql

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

# 어떤 URL이 우리가 작성한 함수를 실행시키는지 알려줌. HTTP POST request에만 응답할 것을 명시함 
@app.route('/', methods=['POST'])
def webhook():
    # incoming JSON data를 python dictionary 로 변환
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    # webhook 실행할 결과 (user definded fuction)
    res = makeWebhookResult(req)

    # python object 를 json 문자열로 변환 
    res = json.dumps(res, indent=4)
    # print(res)
    # return avleues to a proper HTTP response object & header 추가
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") == "sayHello":
        speech = "webhook test result ok"
    else:
        try:
            conn = pymysql.connect(host='localhost', user='tutorial', password='tutorial', db='tutorial', charset='utf8')
            apartmentname = req.get("result").get("parameters").get("apartmentname")
            with conn.cursor() as curs:
                curs.execute("""select avg(price) as aprice from tutorial where name=%s""", ( str(apartmentname)))
                print(curs.rowcount)
                print(curs._last_executed)
                rows = curs.fetchall()
                if curs.rowcount == 0:
                    speech = "최근 실거래가 정보가 없습니다"
                elif curs.rowcount == 1:
                    for row in rows:
                        aprice = row[0]
                    speech = "최근 " + apartmentname + "아파트 실거래가는 "+ str(int(aprice)) + "만원 입니다"
                else:
                    speech = "최근 실거래가 정보가 없습니다" 
        except pymysql.InternalError as error:
                code, message = error.args
                print(code)
                print( message)
        except Exception as e:
                print('Make WebHook Result Error:' + str(e))

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "dialogflow-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
