from fastapi import FastAPI, Request
import smtplib
import os
from email.mime.text import MIMEText

app = FastAPI()

@app.post("/send-alert")
async def send_alert(request: Request):
    data = await request.json()
    nb = data.get("nb_feedbacks", "?")

    smtp_server = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    port = int(os.getenv("EMAIL_PORT", 587))
    sender = os.getenv("EMAIL_HOST_USER")
    password = os.getenv("EMAIL_HOST_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    print("=== [API MAIL DEBUG] ===")
    print(f"SMTP Server     : {smtp_server}")
    print(f"Port            : {port}")
    print(f"Sender          : {sender}")
    print(f"Receiver        : {receiver}")
    print(f"Password present: {bool(password)}")

    try:
        subject = f"[ALERTE] {nb} feedbacks négatifs reçus"
        body = f"{nb} tweets négatifs détectés en 5 min !"
        msg = MIMEText(body, _charset="utf-8")
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = receiver

        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())

        print("✅ Email envoyé avec succès.")
        return {"status": "success"}
    except Exception as e:
        print(f"❌ Erreur lors de l’envoi : {e}")
        return {"status": "fail", "error": str(e)}
