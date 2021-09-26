import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import settings


def notify(monitoring_id: int, map_timestamp: str, attachments: list[Path]):
    send_from = settings.NOTIFICATION_FROM_ADDR
    send_to = settings.NOTIFICATION_TO_ADDRS

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ','.join(send_to)
    msg['Subject'] = f'Actualización Copernicus - Cumbre Vieja [Monitoring {monitoring_id}]'

    content = map_timestamp
    msg.attach(MIMEText(content, 'html'))

    for attachment in attachments:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read_bytes())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={attachment.name}')
        msg.attach(part)

    s = smtplib.SMTP(settings.SMTP_SERVER, port=settings.SMTP_PORT)
    s.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
    s.sendmail(send_from, send_to, msg.as_string())
    s.quit()
