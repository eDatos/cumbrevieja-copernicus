from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from logzero import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import services
import settings
import storage


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
            vectors_url, pdf_url = None, None
            if a := vfield.span.a:
                title = a.text
                if (
                    target_monitoring_display in title
                    and settings.TARGET_MAP_DISPLAY in title
                ):
                    logger.debug(f'Matched view {title}')
                    if settings.TARGET_STATUS in row.text.upper():
                        logger.debug(f'{settings.TARGET_STATUS} found!')
                        vectors = row.find(
                            class_='views-field-field-component-file-vectors'
                        )
                        if a := vectors.div.a:
                            vectors_url = urljoin(settings.COPERNICUS_BASE_URL, a['href'])
                            logger.debug(f'Vectors url: {vectors_url}')
                        pdf = row.find(class_='views-field-field-component-file-200dpi-pdf')
                        if a := pdf.div.a:
                            pdf_url = urljoin(settings.COPERNICUS_BASE_URL, a['href'])
                            logger.debug(f'PDF url: {pdf_url}')
                        if vectors_url is not None and pdf_url is not None:
                            logger.info('Updating key-value online storage...')
                            storage.set_value(
                                settings.TARGET_MONITORING_ID_KEY, target_monitoring_id + 1
                            )
                            return vectors_url, pdf_url


def download_vectors(vectors_url: str, output_filename: str = None):
    logger.debug('Initializing webdriver with Selenium...')
    options = Options()
    options.headless = True
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.dir', str(settings.DOWNLOADS_DIR))
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip')
    driver = webdriver.Firefox(options=options, firefox_profile=profile)

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

    if output_filename is None:
        output_filename = settings.COPERNICUS_COMPONENT_ID + '.zip'

    logger.info('Renaming downloaded vectors file to {output_filename} ...')
    output_file = settings.DOWNLOADS_DIR / output_filename
    return services.rename_newest_file(output_file)


def download_pdf(pdf_url: str, output_filename: str = None):
    logger.info('Downloading {pdf_url} ...')
    response = requests.get(pdf_url, allow_redirects=True)
    if output_filename is None:
        output_filename = settings.COPERNICUS_COMPONENT_ID + '.pdf'
    output_file = settings.DOWNLOADS_DIR / output_filename
    output_file.write_bytes(response.content)
    return output_file
