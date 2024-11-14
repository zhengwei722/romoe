from flask import Flask, Response, json, jsonify
import time
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)


@app.route('/config', methods=['GET'])
def config():
    data = {
    "code": 200,
    "msg": "操作成功",
    # "data": {
    #     "baseInfo": {
    #         "contentSecurity": 0,
    #         "siteTitle": "Romoe",
    #         "siteLogo": "https://gpt.panday94.xyz/chat-master/files/default/2024/03/f8e0b55b-b785-461a-87c2-b56b1ccfc863.png",
    #         "proxyType": 2,
    #         "proxyServer": "https://api.openai-hk.com/",
    #         "proxyAddress": "",
    #         "domain": "https://gpt.panday94.xyz",
    #         "copyright": "Romoe",
    #         "descrip": "切换讯飞星火！星火！星火！可正常输出。ChatMASTER，基于AI大模型api实现的ChatGPT服务，支持ChatGPT(3.5、4.0)模型，同时也支持国内文心一言(支持Stable-Diffusion-XL作图)、通义千问、讯飞星火、智谱清言(ChatGLM)等主流模型，支出同步响应及流式响应，完美呈现打印机效果。",
    #         "keywords": [
    #             "通义千问",
    #             "ChatGPT",
    #             "文心一言",
    #             "智谱清言"
    #         ]
    #     },
    #     "extraInfo": None,
    #     "appInfo": {
    #         "isGPTLimit": 0,
    #         "isRedemption": 1,
    #         "isSms": 1,
    #         "isShare": 1,
    #         "shareNum": 5,
    #         "freeNum": 20,
    #         "h5Url": "https://gpt.panday94.xyz/h5",
    #         "homeNotice": "切换讯飞星火！星火！星火！可正常输出。确保合法合规使用，在运营过程中产生的一切问题后果自负，与作者无关。!"
    #     },
    #     "wxInfo": None,
    #     "mainAssistant": None,
    #     "assistants": []
    # }
}


    return jsonify(data)

@app.route('/test', methods=['GET','POST'])
def test():
    data = {
        "code": 200,
        "msg": "操作成功",
        # "data": {
        #     "baseInfo": {
        #         "contentSecurity": 0,
        #         "siteTitle": "Romoe",
        #         "siteLogo": "https://gpt.panday94.xyz/chat-master/files/default/2024/03/f8e0b55b-b785-461a-87c2-b56b1ccfc863.png",
        #         "proxyType": 2,
        #         "proxyServer": "https://api.openai-hk.com/",
        #         "proxyAddress": "",
        #         "domain": "https://gpt.panday94.xyz",
        #         "copyright": "Romoe",
        #         "descrip": "切换讯飞星火！星火！星火！可正常输出。ChatMASTER，基于AI大模型api实现的ChatGPT服务，支持ChatGPT(3.5、4.0)模型，同时也支持国内文心一言(支持Stable-Diffusion-XL作图)、通义千问、讯飞星火、智谱清言(ChatGLM)等主流模型，支出同步响应及流式响应，完美呈现打印机效果。",
        #         "keywords": [
        #             "通义千问",
        #             "ChatGPT",
        #             "文心一言",
        #             "智谱清言"
        #         ]
        #     },
        #     "extraInfo": None,
        #     "appInfo": {
        #         "isGPTLimit": 0,
        #         "isRedemption": 1,
        #         "isSms": 1,
        #         "isShare": 1,
        #         "shareNum": 5,
        #         "freeNum": 20,
        #         "h5Url": "https://gpt.panday94.xyz/h5",
        #         "homeNotice": "切换讯飞星火！星火！星火！可正常输出。确保合法合规使用，在运营过程中产生的一切问题后果自负，与作者无关。!"
        #     },
        #     "wxInfo": None,
        #     "mainAssistant": None,
        #     "assistants": []
        # }
    }


    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)



