from pathlib import Path
from urllib.parse import urljoin

from prettyconf import config

PROJECT_DIR = Path(__file__).resolve().parent

COPERNICUS_BASE_URL = config(
    'COPERNICUS_BASE_URL',
    default='https://emergency.copernicus.eu/mapping/list-of-components/',
)
COPERNICUS_COMPONENT_ID = config('COPERNICUS_COMPONENT_ID')
COPERNICUS_COMPONENT_URL = urljoin(COPERNICUS_BASE_URL, COPERNICUS_COMPONENT_ID)

CHECKED_MONITORING_IDS_KEY = config(
    'CHECKED_MONITORING_IDS_KEY', default='checked-monitoring-ids'
)
TARGET_MONITORING_ID_DISPLAY = config('TARGET_MONITORING_ID_DISPLAY', default='Monitoring')
TARGET_MAP_ID = config('TARGET_MAP_ID', cast=int)
TARGET_MAP_DISPLAY = f'RTP Map #{TARGET_MAP_ID:02d}'
TARGET_STATUS = config('TARGET_STATUS', default='Quality approved')

DOWNLOADS_DIR = PROJECT_DIR / config('DOWNLOADS_DIR', default='downloads')

NOTIFICATION_FROM_ADDR = config('NOTIFICATION_FROM_ADDR')
NOTIFICATION_TO_ADDRS = config('NOTIFICATION_TO_ADDRS', cast=config.list)
SMTP_SERVER = config('SMTP_SERVER')
SMTP_PORT = config('SMTP_PORT')
SMTP_USERNAME = config('SMTP_USERNAME')
SMTP_PASSWORD = config('SMTP_PASSWORD')

KEYVALUE_API_TOKEN = config('KEYVALUE_API_TOKEN')
KEYVALUE_API_URL = config(
    'KEYVALUE_API_URL', default='https://keyvalue.immanuel.co/api/KeyVal/'
)
KEYVALUE_API_SET_URL = urljoin(KEYVALUE_API_URL, 'UpdateValue/')
KEYVALUE_API_GET_URL = urljoin(KEYVALUE_API_URL, 'GetValue/')
KEYVALUE_API_NAMESPACE = config('KEYVALUE_API_NAMESPACE', default='copernicus')

LOGFILE = config('LOGFILE', default=PROJECT_DIR / (PROJECT_DIR.name + '.log'))
LOGFILE_SIZE = config('LOGFILE_SIZE', cast=float, default=1e6)
LOGFILE_BACKUP_COUNT = config('LOGFILE_BACKUP_COUNT', cast=int, default=3)

MAP_TIMESTAMP_TZ = config('MAP_TIMESTAMP_TZ', default='UTC')

CUSTOM_KEYVALUE_API_URL = config('CUSTOM_KEYVALUE_API_URL')
