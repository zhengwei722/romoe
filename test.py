from flask import Flask, Response, stream_with_context
import time
import requests
app = Flask(__name__)

@app.route('/stream')
def stream():
    def generate():
        try:
            for i in range(10):
                time.sleep(1)  # 模拟耗时操作
                yield f'data: {i}\n'
        except Exception as e:
            yield f'An error occurred: {e}\n'

    return Response(stream_with_context(generate()), status=200, mimetype='text/event-stream')

@app.route('/stream1')
def stream_data():
    def generate():
        # 请求接口 A
        try:
            response = requests.get('http://127.0.0.1:5000/stream', stream=True)
            response.raise_for_status()  # 确保请求成功

            # 流式读取接口 A 的响应内容
            for chunk in response.iter_lines(decode_unicode=True):
                print(chunk)
                if chunk:  # 过滤掉 keep-alive 新行
                    yield chunk

        except requests.exceptions.RequestException as e:
            # 处理请求异常
            yield str(e)

    # 创建流式响应
    return Response(stream_with_context(generate()), status=200, mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)