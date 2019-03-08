#-*-coding:utf-8-*-

import requests
import json

class YunPian(object):
    def __init__(self,api_key):
        self.api_key=api_key
        self.single_send_url='https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self,code,mobile):
        parmas={
            'apikey':self.api_key,
            'mobile':mobile,
            'text':'【周帆1】您的验证码是{code}。如非本人操作，请忽略本短信'.format(code=code)
        }
        #text必须要跟云片后台的模板内容 保持一致，不然发送不出去！
        r=requests.post(self.single_send_url,data=parmas)
        return json.loads(r.text)

if __name__=='__main__':
    yun_pian=YunPian('76908d1d8a87c999a9e2cdedd0cd274d')
    yun_pian.send_sms('1234','15961168273')