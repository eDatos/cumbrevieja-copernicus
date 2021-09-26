import shutil

import scrap
import services
import settings

if links := scrap.get_links():
    vectors_url, pdf_url = links
    scrap.download_vectors(vectors_url)
    pdf_file = scrap.download_pdf(pdf_url)
    map_timestamp = services.extract_map_timestamp(pdf_file)
    shutil.rmtree(settings.DOWNLOADS_DIR)
