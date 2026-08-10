# -*- coding: utf-8 -*-
import os, sys, webbrowser, time, socket

# 切换到脚本所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 端口检测
def port_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) != 0

port = 5050
if not port_free(port):
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    tk.messagebox.showwarning("端口被占用", "5050 端口已被占用，\u8bf7\u5148\u5173\u95ed\u539f\u6709\u8fdb\u7a0b\u3002")
    sys.exit(0)

# 启动 Flask（静默，无控制台）
from wsgiref import simple_server
from kaoyan_web import make_app

app = make_app()
server = simple_server.make_server('0.0.0.0', port, app)

# 自动打开浏览器
time.sleep(0.5)
webbrowser.open(f'http://127.0.0.1:{port}')

server.serve_forever()
