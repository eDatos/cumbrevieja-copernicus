import os
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


def extract_artifact_url(artifact_id: str, row: PageElement):
    try:
        artifact = row.find(class_=f'views-field-field-component-file-{artifact_id}')
        artifact_url = urljoin(settings.COPERNICUS_BASE_URL, artifact.div.a['href'])
    except AttributeError:
        logger.error(f'{artifact_id} link is not present')
        artifact_url = None
    else:
        logger.debug(f'{artifact_id} url: {artifact_url}')
    return artifact_url


def get_links(target_monitoring_id: int):
    target_monitoring_display = settings.TARGET_MONITORING_DISPLAY.format(
        target_monitoring_id=target_monitoring_id
    )
    logger.info(f'Scrapping {settings.COPERNICUS_COMPONENT_URL} ...')
    response = requests.get(settings.COPERNICUS_COMPONENT_URL)
    logger.debug('Parsing response with Beautiful Soup...')
    soup = BeautifulSoup(response.text, features='html.parser')
    for row in soup.find_all(class_='views-row'):
        for vfield in row.find_all(class_='views-field views-field-title'):
            if a := vfield.span.a:
                title = a.text
                if (
                    target_monitoring_display in title
                    and settings.TARGET_MAP_DISPLAY in title
                ):
                    logger.debug(f'Matched view {title}')
                    if settings.TARGET_STATUS in row.text.upper():
                        # Target monitoring id found and quality level achievied
                        logger.debug(f'{settings.TARGET_STATUS} found!')
                        vectors_url = extract_artifact_url('vectors', row)
                        pdf_url = extract_artifact_url('200dpi-pdf', row)
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


def download_vectors(vectors_url: str, target_monitoring_id: int):
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

    logger.debug('Downloading vectors...')
    submit = form.find_element_by_id('edit-submit')
    submit.click()

    driver.quit()

    output_filename = f'{settings.COPERNICUS_COMPONENT_ID}-M{target_monitoring_id}.zip'
    logger.info(f'Renaming downloaded vectors file to {output_filename} ...')
    output_file = settings.DOWNLOADS_DIR / output_filename
    return services.rename_newest_file(output_file)


def download_pdf(pdf_url: str, target_monitoring_id: int):
    logger.info(f'Downloading {pdf_url} ...')
    response = requests.get(pdf_url, allow_redirects=True)
    output_filename = f'{settings.COPERNICUS_COMPONENT_ID}-M{target_monitoring_id}.pdf'
    output_file = settings.DOWNLOADS_DIR / output_filename
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_bytes(response.content)
    return output_file
