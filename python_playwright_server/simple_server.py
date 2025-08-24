import json
import time
from playwright.sync_api import sync_playwright
from flask import Flask, jsonify, request

app = Flask(__name__)

playwright = sync_playwright().start()
browser = playwright.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
            ])

def generate_cookies(url, html, user_agent=None):
    default_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    if user_agent:
        default_user_agent = user_agent
    context = browser.new_context(
        user_agent=default_user_agent,
    )
    page = context.new_page()

    def handle_request(route, request):
        print('hererer ', request.url, url)
        if url in request.url:
            # 返回自定义的 HTML 内容
            route.fulfill(status=200, content_type='text/html', body=html)
        else:
            route.abort()

    page.route("**/*", handler=handle_request)
    page.goto(url)
    # time.sleep(1)
    cookies = context.cookies()
    result = {}
    for item in cookies:
        result[item['name']] = item['value']
    # 关闭页面
    page.close()
    return result


@app.route("/get-cookies", methods=["POST"])
def get_cookies():
    data = request.json
    url = data.get('url', '')
    html = data.get('html', '')
    user_agent = data.get('user_agent', '')
    cookies = generate_cookies(url, html, user_agent=user_agent)
    result = {}
    result['cookies'] = cookies
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=False, processes=1, port=3000, debug=False)
