# -*-coding:utf-8-*-
# @Project  GPT
# @File     chat_gpt_server.py
# @Time     2023/03/20 9:09
# @Author   YangLiu
# @Email    willow918@163.com
# @Version  python3.7.1
from tools.chat_gpt import chat_gpt
from tools.log import error_logger, info_logger, warn_logger
from tools.e_wechat_msg_decode import WXBizMsgCrypt
from tools.get_config import getConfig
import xml.etree.cElementTree as ET
from tools.redis_client import RedisClient
from tools.wechat import QHWechat
from flask import Flask, request, jsonify

qh_sToken = getConfig("gpt.conf", 'qh_wechat', 'sToken')
qh_sEncodingAESKey = getConfig("gpt.conf", 'qh_wechat', 'sEncodingAESKey')
qh_sReceiveId = getConfig("gpt.conf", 'qh_wechat', 'sReceiveId')
qh_gpt_key = getConfig("gpt.conf", 'qh_wechat', 'gpt_key')

app = Flask(__name__)


@app.route('/qh_e_wechat_msg_verify', methods=["GET"])
def qh_e_wechat_msg_verify_get():
    try:

        msg_signature = request.args.get('msg_signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')
        e_wechat_msg_verify = WXBizMsgCrypt(qh_sToken, qh_sEncodingAESKey, qh_sReceiveId)

        res = e_wechat_msg_verify.VerifyURL(msg_signature, timestamp, nonce, echostr)
        info_logger.info(res)

        return res[1] if res[1] else f'校验回调失败{res[0]}'
    except Exception as e:
        error_logger.error(f'校验回调失败{e}')


@app.route('/qh_e_wechat_msg_verify', methods=["POST"])
def qh_e_wechat_msg_verify_post():
    try:
        sMsgSignature = request.args.get('msg_signature')
        sTimeStamp = request.args.get('timestamp')
        sNonce = request.args.get('nonce')
        print(f'data    {request.args}')
        print(f'body    {request.data}')
        body = request.data
        print(body)
        sPostData = body
        e_wechat_msg_verify = WXBizMsgCrypt(qh_sToken, qh_sEncodingAESKey, qh_sReceiveId)
        msg = e_wechat_msg_verify.DecryptMsg(sPostData.decode(), sMsgSignature, sTimeStamp, sNonce)[1]
        if not msg:
            info_logger.info('没有msg')
            return 'no msg'
        xml_tree = ET.fromstring(msg)
        Content = xml_tree.find('Content')
        if Content is None:
            # info_logger.info('没有content')
            return 'no Content'
        # ToUserName = xml_tree.find('ToUserName').text if xml_tree.find('ToUserName') is not None else ''
        FromUserName = xml_tree.find('FromUserName').text if xml_tree.find('FromUserName') is not None else ''
        if FromUserName is None:
            info_logger.info('没有FromUserName')
            return 'no FromUserName'
        CreateTime = xml_tree.find('CreateTime').text if xml_tree.find('CreateTime') is not None else ''
        if redis_client.get(FromUserName + CreateTime):
            return '会话已存在'
        if FromUserName and CreateTime:
            redis_client.set(FromUserName + CreateTime, '1', 60)
        answer = chat_gpt(redis_client, FromUserName, Content.text, gpt_key=qh_gpt_key)
        wechat = QHWechat()
        res = wechat.send_message([FromUserName], answer)
        if not res:
            wechat.send_message([FromUserName], answer)
        return '会话结束'
    except Exception as e:
        error_logger.error(f'接口发生错误{e}')
        return f'接口发生错误{e}'


if __name__ == '__main__':
    redis_client = RedisClient(db=0)
    app.run(host='0.0.0.0', threaded=True, debug=False, port=18080)
