import shutil

import logzero
import typer

import settings
from copernicus import notification, scrap, services, storage, utils

app = typer.Typer(add_completion=False)
logger = utils.init_logger()


@app.command()
def notify(
    target_monitoring_id: int = typer.Option(
        0,
        '--monitoring-id',
        '-m',
        help='Target monitoring id. If 0, a key-value online storage is used instead!',
    ),
    verbose: bool = typer.Option(False, '--verbose', '-vv', show_default=False),
    clean: bool = typer.Option(False, '--clean', '-x', show_default=False),
):
    logger.setLevel(logzero.DEBUG if verbose else logzero.INFO)

    if update_monitoring_id := not target_monitoring_id:
        logger.debug('Getting target monitoring id from key-value online storage...')
        target_monitoring_id = storage.get_value(
            settings.TARGET_MONITORING_ID_KEY, default=1, cast=int
        )
    logger.info(f'Trying to retrieve Monitoring {target_monitoring_id}...')

    if links := scrap.get_links(target_monitoring_id, update_monitoring_id):
        vectors_url, pdf_url = links
        if vectors_url:
            vectors_file = scrap.download_vectors(vectors_url, target_monitoring_id)
        else:
            vectors_file = None
        if pdf_url:
            pdf_file = scrap.download_pdf(pdf_url, target_monitoring_id)
            map_timestamp = services.extract_map_timestamp(pdf_file)
        else:
            map_timestamp = None
        notification.notify(target_monitoring_id, map_timestamp, vectors_file)
        if clean:
            logger.debug('Cleaning downloads directory...')
            shutil.rmtree(settings.DOWNLOADS_DIR)
    else:
        logger.warning(
            f'Monitoring {target_monitoring_id} is not yet available '
            'or in a desired quality level'
        )


if __name__ == "__main__":
    app()
