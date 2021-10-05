import smtplib
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import settings
from logzero import logger


def notify(monitoring_id: int, map_timestamp: datetime, vectors_file: Path):
    logger.info('Initializing notification handler...')
    send_from = settings.NOTIFICATION_FROM_ADDR
    send_to = settings.NOTIFICATION_TO_ADDRS

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ','.join(send_to)
    msg['Subject'] = f'Actualización Copernicus - Cumbre Vieja [Monitoring {monitoring_id}]'

    buf = []
    if map_timestamp is None:
        buf.append('La marca temporal no está disponible en la web')
    else:
        buf.append(map_timestamp.strftime('%d/%m/%Y %H%M %Z'))
    if vectors_file is None:
        buf.append('El paquete de vectores no está disponible en la web')
    else:
        logger.debug('Adding attachment...')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(vectors_file.read_bytes())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={vectors_file.name}')
        msg.attach(part)
    content = '<br>'.join(buf)
    msg.attach(MIMEText(content, 'html'))

    logger.info('Sending message with attached files...')
    s = smtplib.SMTP(settings.SMTP_SERVER, port=settings.SMTP_PORT)
    s.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
    s.sendmail(send_from, send_to, msg.as_string())
    s.quit()
