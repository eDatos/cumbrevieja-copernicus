import shutil

import settings
from copernicus import notification, scrap, services, storage, utils

logger = utils.init_logger()

target_monitoring_id = storage.get_value(
    settings.TARGET_MONITORING_ID_KEY, default=1, cast=int
)

logger.info(f'Trying to retrieve Monitoring {target_monitoring_id}...')
if links := scrap.get_links(int(target_monitoring_id)):
    vectors_url, pdf_url = links
    vectors_file = scrap.download_vectors(vectors_url)
    pdf_file = scrap.download_pdf(pdf_url)
    map_timestamp = services.extract_map_timestamp(pdf_file)
    notification.notify(target_monitoring_id, map_timestamp, [vectors_file])
    shutil.rmtree(settings.DOWNLOADS_DIR)
else:
    logger.warning(
        f'Monitoring {target_monitoring_id} is not yet available '
        'or in a desired quality level'
    )
