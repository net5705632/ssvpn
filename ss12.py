import sys
import requests
import base64
import json
import pyaes
import binascii
from datetime import datetime

def decrypt_data(data, key, iv):
    try:
        aes = pyaes.AESModeOfOperationCBC(key, iv=iv)
        decrypted = b''.join(aes.decrypt(data[i:i+16]) for i in range(0, len(data), 16))
        return decrypted[:-decrypted[-1]]
    except Exception as e:
        print(f"Decryption error: {str(e)}", file=sys.stderr)
        sys.exit(1)

try:
    # 初始化请求参数
    api_url = 'http://api.skrapp.net/api/serverlist'
    headers = {
        'User-Agent': 'SkrKK/1.3.1 (iPhone; iOS 13.5; Scale/2.00)',
        'Cookie': 'PHPSESSID=fnffo1ivhvt0ouo6ebqn86a0d4'
    }
    payload = {'data': '4265a9c353cd8624fd2bc7b5d75d2f18b1b5e66ccd37e2dfa628bcb8f73db2f14ba98bc6a1d8d0d1c7ff1ef0823b11264d0addaba2bd6a30bdefe06f4ba994ed'}
    
    # 发送请求
    response = requests.post(api_url, headers=headers, data=payload)
    response.raise_for_status()  # 自动处理HTTP错误

    # 解密处理
    key = b'65151f8d966bf596'
    iv = b'88ca0f0ea1ecf975'
    decrypted_data = decrypt_data(binascii.unhexlify(response.text.strip()), key, iv)
    
    # 解析JSON
    servers = json.loads(decrypted_data)
    
    # 生成SS链接
    valid_links = []
    for server in servers.get('data', []):
        if all(k in server for k in ('password', 'ip', 'port')):
            ss_config = f"aes-256-cfb:{server['password']}@{server['ip']}:{server['port']}"
            base64_config = base64.b64encode(ss_config.encode()).decode()
            valid_links.append(f"ss://{base64_config}#{server.get('title', 'Untitled')}")
    
    # 输出有效链接
    if valid_links:
        print('\n'.join(valid_links))
    else:
        print("No valid servers found!", file=sys.stderr)
        sys.exit(1)

except Exception as e:
    print(f"Critical error: {str(e)}", file=sys.stderr)
    sys.exit(1)
