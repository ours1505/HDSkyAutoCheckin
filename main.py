import configparser
from urllib.parse import urlencode
from ddddocr import DdddOcr
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')


def checkin():
    # 实例化DdddOcr对象
    ocr = DdddOcr()
    config = configparser.ConfigParser(interpolation=None)
    config.read('config.ini', encoding='utf-8')
    ua = config['default']['UserAgent']
    headers = {'User-Agent': ua, 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', }
    logging.info(f"正在签到站点: hdsky")
    cookies = config.get('hdsky', 'cookie').split('; ')
    cookie_dict = {}
    for pair in cookies:
        key, value = pair.split('=', 1)
        cookie_dict[key] = value
    while True:
        payload = urlencode({'action': 'new'})
        response = requests.post(f'https://hdsky.me/image_code_ajax.php', headers=headers, data=payload,
                                 cookies=cookie_dict, verify=False)
        if response.status_code == 200 and response.json()['success']:
            code = response.json()['code']
            response = requests.get(f'https://hdsky.me/image.php?action=regimage&imagehash={code}', headers=headers,
                                    stream=True, verify=False)
            if response.status_code == 200:
                # 将响应内容保存为bytes对象
                image_bytes = response.content
                # 使用ocr对象识别图片中的验证码
                recognized_text = ocr.classification(image_bytes)
                logging.info(f'获取到验证码为：{recognized_text}')
                payload = {'action': 'showup', 'imagehash': code, 'imagestring': recognized_text}
                response = requests.post(f'https://hdsky.me/showup.php', headers=headers, data=payload,
                                         cookies=cookie_dict, verify=False)
                if response.json()['success']:
                    logging.info(f'站点hdsky.me签到成功')
                    break
                elif response.json()['message'] == 'date_unmatch':
                    logging.info('站点已经签到')
                    break
                else:
                    logging.info('验证码识别错误，重试')


if __name__ == '__main__':
    checkin()
