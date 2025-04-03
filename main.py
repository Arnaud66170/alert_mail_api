from fastapi import FastAPI, Request
import smtplib
import os

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
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender, password)
            subject = f"[ALERTE] {nb} feedbacks négatifs reçus"
            body = f"{nb} tweets négatifs détectés en 5 min !"
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(sender, receiver, message)
        return {"status": "success"}
    except Exception as e:
        return {"status": "fail", "error": str(e)}
