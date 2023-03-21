# WeCom_ChatGPT
企业微信集成ChatGPT聊天机器人，Python3+Flask+Redis

# 需要海外服务器或者设置代理

# 按照顺序完成以下流程
- 登录企业微信管理后台（管理员身份）
- 点击【应用管理】，【应用】，【创建应用】
- 创建完应用后，进入应用
- 【企业可信IP】-【配置】（自己服务器的公网ip）
- 【网页授权及JS-SDK】-【设置可信域名】（有官方指引）
- 克隆本项目到服务器（依赖redis，python368+）
- 安装requirements.txt
- 修改本项目中的gpt.conf配置文件
```
sToken  # 【企业微信管理后台】-【应用管理】-【自建应用】-【接收消息】-【设置API接收】-【Token】-【自定义即可】

sEncodingAESKey # 【企业微信管理后台】-【应用管理】-【自建应用】-【接收消息】-【设置API接收】-【EncodingAESKey】-【自定义即可】

sReceiveId  # 【企业微信管理后台】-【我的企业】-【企业信息】-【企业ID】

corpsecret # 【企业微信管理后台】-【应用管理】-【Secret】-【查看】

agentid # 【企业微信管理后台】-【应用管理】-【Secret】-【AgentId】

gpt_key # 【gpt的key】
```
- 按需修改【main.py】中的端口，并开放安全组
- 启动项目【python3 main.py】
- 【企业微信管理后台】-【应用管理】-【自建应用】-【接收消息】-【设置API接收】-【接收消息服务器配置】-【域名+/qh_e_wechat_msg_verify】
- 【保存】
- 【企业微信客户端】-【工作台】-【自建应用】，即可开启聊天之旅

