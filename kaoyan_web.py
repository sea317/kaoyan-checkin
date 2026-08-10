# -*- coding: utf-8 -*-
"""
考研打卡 Web 服务（手机优先版）
kaoyan_web.py
"""
from flask import Flask, jsonify, request, send_from_directory
from kaoyan_core import (
    get_full_state, update_today, delete_today,
    SUBJECTS, APP_DIR
)
import os, sys

# 确保工作目录正确
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

def make_app():
    app = Flask(__name__, template_folder=SCRIPT_DIR)

    @app.route("/")
    def index():
        return send_from_directory(SCRIPT_DIR, "打卡页面.html")

    @app.route("/api/state")
    def api_state():
        return jsonify(get_full_state())

    @app.route("/api/checkin", methods=["POST"])
    def api_checkin():
        data = request.get_json() or {}
        subjects = data.get("subjects", {})
        note = data.get("note", "")
        state = update_today(subjects, note)
        return jsonify({"ok": True, "state": state})

    @app.route("/api/delete", methods=["POST"])
    def api_delete():
        state = delete_today()
        return jsonify({"ok": True, "state": state})

    return app

def run_web(port=5050):
    app = make_app()
    print("\u542f\u52a8\u4e2d... http://127.0.0.1:{}\u3002\u624b\u673a\u8bf7\u7528\u5c40\u57df\u7f51\u8bbf\u95ee\u3002".format(port))
    print("\u6309 Ctrl+C \u7ed8\u505c\u6b62")
    # 绑定 0.0.0.0 = 所有网卡（手机/电脑同局域网都能访问）
    app.run(host="0.0.0.0", port=port, debug=False)

if __name__ == "__main__":
    port = 5050
    if len(sys.argv) > 1 and sys.argv[1] == "--port":
        port = int(sys.argv[2])
    run_web(port)
