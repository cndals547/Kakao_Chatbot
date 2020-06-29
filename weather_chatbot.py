from flask import Flask, request, jsonify
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import urllib

ERROR_MESSAGE = '네트워크 접속에 문제가 발생하였습니다. 잠시 후 다시 시도해주세요.'

app = Flask(__name__)

@app.route('/weather', methods=['POST'])
def weather():

    req = request.get_json()

    location = req["action"]["detailParams"]["sys_location"]["value"]

    enc_loc = urllib.parse.quote(location + '+ 날씨')
    el = str(enc_loc)
    url = 'https://search.naver.com/search.naver'
    url = url + '?sm=top_hty&fbm=1&ie=utf8&query='
    url = url + el

    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = BeautifulSoup(html, 'html.parser')
    r1 = soup.find('li', class_='on now merge1')
    r2 = r1.find('dd', class_='weather_item _dotWrapper')
    r3 = r2.find('span').text
    r4 = soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text
    # .find('dd', class_='weather_item _dotWrapper').find('span').text

    rain_pct = int(r3)

    if len(location) <= 0:
        answer = ERROR_MESSAGE
    elif rain_pct < 30:
        answer = location + "의 온도는" + r4 + "도 이며" + "의 강수 확률은 " + r3 + "%입니다 맑은 하루 되세요^_^"
    else:
        answer = location + "의 온도는" + r4 + "도 이며" + "의 강수 확률은 " + r3 + "%입니다 우산 챙겨가세요!!"

    res = {
        "version": "1.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer
                    }
                }
            ]
        }
    }

    return jsonify(res)


# 메인 함수
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, threaded=True)