import shutil

import notification
import scrap
import services
import settings
import storage

target_monitoring_id = storage.get_value(
    settings.TARGET_MONITORING_ID_KEY, default=1, cast=int
)
if links := scrap.get_links(int(target_monitoring_id)):
    vectors_url, pdf_url = links
    vectors_file = scrap.download_vectors(vectors_url)
    pdf_file = scrap.download_pdf(pdf_url)
    map_timestamp = services.extract_map_timestamp(pdf_file)
    notification.notify(target_monitoring_id, map_timestamp, [vectors_file])
    shutil.rmtree(settings.DOWNLOADS_DIR)
