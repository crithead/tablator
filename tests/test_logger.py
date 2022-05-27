# PyTest for tablator.logger

import tablator.logger as logger

def test_debug_on(capsys):
    logger.set(True, False)     # enable debug
    logger.debug('this is a message')
    logger.set(False, False)    # disable
    out, err = capsys.readouterr()
    #with capsys.disabled():
    #    print('out', out, sep='\n')
    assert out.startswith('--- this is a message')


def test_debug_off(capsys):
    logger.set(False, False)    # disable both
    logger.debug('this is a message')
    out, err = capsys.readouterr()
    assert out == ''


def test_set_nothing():
    logger.set(False, False)
    assert logger._debug_on is False
    assert logger._trace_on is False


def test_set_debug():
    logger.set(True, False)
    assert logger._debug_on is True
    assert logger._trace_on is False


def test_set_trace():
    logger.set(False, True)
    assert logger._debug_on is False
    assert logger._trace_on is True


def test_set_both():
    logger.set(True, True)
    assert logger._debug_on is True
    assert logger._trace_on is True


def test_trace_on(capsys):
    logger.set(False, True)     # enable trace
    logger.trace('this is a message')
    logger.set(False, False)    # disable trace
    out, err = capsys.readouterr()
    assert out.startswith('=== this is a message')


def test_trace_off(capsys):
    logger.set(False, False)    # disable both
    logger.debug('this is a message')
    out, err = capsys.readouterr()
    assert out == ''

