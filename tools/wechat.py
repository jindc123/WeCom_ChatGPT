from tools.log import info_logger, error_logger
from tools.redis_client import RedisClient
from tools.get_config import getConfig
import requests

qh_sToken = getConfig("gpt.conf", 'qh_wechat', 'sToken')
qh_sEncodingAESKey = getConfig("gpt.conf", 'qh_wechat', 'sEncodingAESKey')
qh_sReceiveId = getConfig("gpt.conf", 'qh_wechat', 'sReceiveId')
qh_corpsecret = getConfig("gpt.conf", 'qh_wechat', 'corpsecret')
qh_agentid = getConfig("gpt.conf", 'qh_wechat', 'agentid')


class QHWechat:
    def __init__(self):
        self.corpid = qh_sReceiveId
        self.corpsecret = qh_corpsecret
        self.redis_client = RedisClient()
        self.access_token = self.get_access_token()

    def get_access_token(self):
        if not self.redis_client.get('Wechat_access_token' + self.corpid):
            try:
                url = f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.corpid}&corpsecret={self.corpsecret}'
                access_token = requests.get(url).json()
                self.redis_client.set('Wechat_access_token' + self.corpid, access_token['access_token'], int(access_token['expires_in']))
                return access_token['access_token']
            except Exception as e:
                error_logger.error(f'获取access_token失败：{e}')
        else:
            return self.redis_client.get('Wechat_access_token' + self.corpid)

    def send_message(self, tousers: list, content):
        try:
            url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.access_token}'
            data = {}
            data['touser'] = '|'.join(tousers)
            data['msgtype'] = 'text'
            data['agentid'] = int(qh_agentid)
            data['text'] = {
                "content": content
            }
            res = requests.post(url, json=data, timeout=10).json()
            if res['errcode'] == 0:
                info_logger.info(f'消息发送成功{res["msgid"]}')
                return 1
            else:
                error_logger.error(f'消息发送失败{res}')
                return
        except Exception as e:
            error_logger.error(f'消息发送失败{e}')
