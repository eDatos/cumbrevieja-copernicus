import json
import shutil
from operator import itemgetter

import logzero
import typer

import settings
from copernicus import notification, scrap, services, storage, utils

app = typer.Typer(add_completion=False)
logger = utils.init_logger()


@app.command()
def run(
    verbose: bool = typer.Option(
        False, '--verbose', '-v', show_default=False, help='Loglevel increased to debug'
    ),
    clean: bool = typer.Option(
        False,
        '--clean',
        '-x',
        show_default=False,
        help='Remove download folder after execution',
    ),
    notify: bool = typer.Option(
        False, '--notify', '-n', show_default=False, help='Notify vectors package via email'
    ),
    target_monitoring_id: int = typer.Option(
        -1,
        '--target-monit-id',
        '-m',
        help='Target monitoring id. If -1, all products will be checked',
    ),
    reset_checked_monitoring_ids: bool = typer.Option(
        False,
        '--reset-monit-ids',
        '-r',
        show_default=False,
        help='Reset checked monitoring ids',
    ),
):
    logger.setLevel(logzero.DEBUG if verbose else logzero.INFO)

    if reset_checked_monitoring_ids:
        storage.set_value(settings.CHECKED_MONITORING_IDS_KEY, json.dumps([]))

    checked_monitoring_ids = storage.get_value(
        settings.CHECKED_MONITORING_IDS_KEY, default=[], cast=json.loads
    )
    logger.debug(f'Checked monitoring ids: {checked_monitoring_ids}')

    for product, monitoring_id in sorted(scrap.get_products(), key=itemgetter(1)):
        if target_monitoring_id != -1 and monitoring_id != target_monitoring_id:
            continue
        logger.info(f'Processing Monitoring {monitoring_id}...')
        if settings.TARGET_STATUS in product.text:
            if (
                monitoring_id not in checked_monitoring_ids
                or monitoring_id == target_monitoring_id
            ):
                vectors_url, pdf_url = scrap.get_links(product)
                if vectors_url:
                    vectors_file = scrap.download_vectors(vectors_url, monitoring_id)
                else:
                    vectors_file = None
                if pdf_url:
                    pdf_file = scrap.download_pdf(pdf_url, monitoring_id)
                    map_timestamp = services.extract_map_timestamp(pdf_file)
                else:
                    map_timestamp = None
                if notify:
                    notification.notify(monitoring_id, map_timestamp, vectors_file)

                logger.debug(f'Adding #{monitoring_id} to checked monitoring ids...')
                checked_monitoring_ids.append(monitoring_id)
            else:
                logger.warning(
                    f'Monitoring {monitoring_id} is already checked. Discarding...'
                )
        else:
            logger.warning(
                f'Monitoring {monitoring_id} has not target status. Discarding...'
            )

    if clean:
        logger.debug('Cleaning downloads directory...')
        shutil.rmtree(settings.DOWNLOADS_DIR, ignore_errors=True)

    storage.set_value(
        settings.CHECKED_MONITORING_IDS_KEY, json.dumps(list(set(checked_monitoring_ids)))
    )


if __name__ == "__main__":
    app()
