"""
Logging configuration and convenience functions.
"""

_debug_on = False
_trace_on = False


def debug(*args):
    """
    Print debug messages, if enabled
    """
    if _debug_on:
        print('---', *args)


def set(d=False, t=False):
    """
    Enable logging types (debug, trace)
    """
    assert(type(d) is bool)
    assert(type(t) is bool)
    global _debug_on, _trace_on
    _debug_on = d
    _trace_on = t


def trace(*args):
    """
    Print trace messages, if enabled
    """
    if _trace_on:
        print('===', *args)
