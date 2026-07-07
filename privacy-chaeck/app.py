from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ip_info')
def ip_info():
    # 获取客户端真实 IP（考虑代理转发）
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()

    # 查询 IP 地理位置信息（免费接口，每分钟45次请求）
    try:
        resp = requests.get(f'http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,org,query', timeout=3)
        data = resp.json()
        if data.get('status') == 'fail':
            data = {'ip': ip, 'error': '地理位置查询失败'}
    except Exception:
        data = {'ip': ip, 'error': '查询服务不可用'}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
