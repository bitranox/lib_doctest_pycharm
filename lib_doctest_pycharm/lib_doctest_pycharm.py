import lib_log_utils
import logging
import sys
logger = logging.getLogger()


def setup_doctest_logger_for_pycharm(log_level: int = logging.INFO):
    """
    >>> logger.info('test')     # there is no output in pycharm by default
    >>> setup_doctest_logger_for_pycharm()
    >>> logger.info('test')     # now we have the output we want
    test

    """
    if is_pytest_running() or is_docrunner_running():
        lib_log_utils.setup_console_logger_simple()
        if not hasattr(logger, 'pycharm_doctest_logger_added'):
            logger_add_streamhandler_to_sys_stdout()
            logging.getLogger().setLevel(log_level)
            logger.pycharm_doctest_logger_added = True


def logger_add_streamhandler_to_sys_stdout():
    if not is_doctest_stdout_handler_added():
        console = logging.StreamHandler(stream=sys.stdout)
        console.name = 'doctest_console_handler'
        logging.getLogger().addHandler(console)


def is_doctest_stdout_handler_added() -> bool:
    """
    >>> setup_doctest_logger_for_pycharm()
    >>> is_doctest_stdout_handler_added()
    True
    """
    for handler in logger.handlers:
        if hasattr(handler, 'stream') and hasattr(handler, 'get_name'):
            if handler.stream == sys.stdout and handler.get_name() == 'doctest_console_handler':
                return True
    return False


def is_docrunner_running() -> bool:
    if 'docrunner.py' in sys.argv[0]:
        return True
    else:
        return False


def is_pytest_running():
    if 'pytest_runner.py' in sys.argv[0]:
        return True
    else:
        return False
