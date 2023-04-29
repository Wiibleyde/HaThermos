import datetime
import glob
import logging
import os
import tarfile
import time

DATA_DIR = os.environ.get('DATA_DIR', '/app/data')
MINECRAFT_DIR = os.environ.get('MINECRAFT_DIR', '/app/minecraft')
BACKUP_DIR = os.environ.get('BACKUP_DIR', '/app/backup')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def make_backup():
    now = datetime.datetime.now()
    date_time = now.strftime('%Y%m%d%H%M%S')
    output_file = os.path.join(BACKUP_DIR, f'{date_time}.tar.gz')
    files_to_backup = glob.glob(os.path.join(DATA_DIR, '*'))
    files_to_backup.extend(glob.glob(os.path.join(MINECRAFT_DIR, '*')))
    logger.info('Creating backup...')
    with tarfile.open(output_file, 'w:gz') as tar:
        for file in files_to_backup:
            logger.info(f'Adding {file} to backup...')
            tar.add(file)
    logger.info(f'Backup created: {output_file}')

def delete_old_backups():
    logger.info('Deleting old backups...')
    files = glob.glob(os.path.join(BACKUP_DIR, '*.tar.gz'))
    files.sort()
    for file in files[:-5]:
        logger.info(f'Deleting {file}...')
        os.remove(file)

if __name__ == '__main__':
    while True:
        try:
            delete_old_backups()
            make_backup()
        except Exception as e:
            logger.exception('Backup failed', exc_info=e)
        logger.info('Sleeping for 1 hour...')
        time.sleep(3600)
