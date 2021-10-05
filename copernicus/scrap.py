import os
import re
from datetime import datetime
from urllib.parse import urljoin

import requests
import settings
from bs4 import BeautifulSoup
from bs4.element import PageElement
from logzero import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from copernicus import services


def _extract_artifact_url(artifact_id: str, row: PageElement):
    try:
        artifact = row.find(class_=f'views-field-field-component-file-{artifact_id}')
        artifact_url = urljoin(settings.COPERNICUS_BASE_URL, artifact.div.a['href'])
    except AttributeError:
        logger.error(f'{artifact_id} link is not present')
        artifact_url = None
    else:
        logger.debug(f'{artifact_id} url: {artifact_url}')
    return artifact_url


def get_products() -> list[PageElement]:
    logger.info('Getting products with target map id...')
    logger.debug(f'Scrapping {settings.COPERNICUS_COMPONENT_URL} ...')
    response = requests.get(settings.COPERNICUS_COMPONENT_URL)
    logger.debug('Parsing response with Beautiful Soup...')
    soup = BeautifulSoup(response.text, features='html.parser')
    for row in soup.find_all(class_='views-row'):
        if settings.TARGET_MAP_DISPLAY in row.text:
            title = row.find(class_='views-field-title').span.a.text
            if s := re.search(rf'{settings.TARGET_MONITORING_ID_DISPLAY} *(\d+)', title):
                monitoring_id = int(s.groups()[0])
                yield row, monitoring_id


def get_links(product: PageElement):
    vectors_url = _extract_artifact_url('vectors', product)
    pdf_url = _extract_artifact_url('200dpi-pdf', product)
    return vectors_url, pdf_url


def init_webdriver():
    options = Options()
    options.headless = True
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.dir', str(settings.DOWNLOADS_DIR))
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip')
    return webdriver.Firefox(
        options=options, firefox_profile=profile, service_log_path=os.devnull
    )


def download_vectors(vectors_url: str, target_monitoring_id: int, map_timestamp: datetime):
    logger.debug('Initializing webdriver with Selenium...')
    driver = init_webdriver()

    logger.info(f'Loading {vectors_url} ...')
    driver.get(vectors_url)
    form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'emsmapping-disclaimer-download-form'))
    )

    logger.debug('Accepting terms...')
    label = form.find_element_by_tag_name('label')
    label.click()

    logger.debug('Clicking submit button...')
    submit = form.find_element_by_id('edit-submit')
    submit.click()

    driver.quit()

    output_filename = services.build_vectors_filename(target_monitoring_id, map_timestamp)
    logger.debug(f'Renaming downloaded vectors file to {output_filename} ...')
    output_file = settings.DOWNLOADS_DIR / output_filename
    return services.rename_newest_file(output_file)


def download_pdf(pdf_url: str, target_monitoring_id: int):
    logger.info(f'Downloading {pdf_url} ...')
    response = requests.get(pdf_url, allow_redirects=True)
    output_filename = f'{settings.COPERNICUS_COMPONENT_ID}-M{target_monitoring_id}.pdf'
    logger.debug(f'Renaming downloaded pdf file to {output_filename} ...')
    output_file = settings.DOWNLOADS_DIR / output_filename
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_bytes(response.content)
    return output_file
