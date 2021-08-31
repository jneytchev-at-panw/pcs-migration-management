from tqdm import tqdm
from loguru import logger
import time

def log_test(logger):
    for x in tqdm(range(10), desc='BEANS'):
        logger.debug("That's it, beautiful and simple logging!")
        logger.info("Iterating #{}", x)
        logger.error('ERROR')
        logger.warning('WARN')
        logger.success('SUCC')
        time.sleep(0.5)


if __name__ == '__main__':
    terminal_logging = True

    logger.remove()

    if terminal_logging:
        logger.level("BAR", no=4)
    else:
        logger.level("BAR", no=51)

    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True, level='BAR')
    logger.add('logs/{time:DD-MM-YYYY_HH:mm:ss}.log', level='TRACE')

    log_test(logger)