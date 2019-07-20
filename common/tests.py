import doctest

def run(verbosity=0):
    from . import trade
    result = doctest.testmod(trade, verbose=verbosity)
    return result.failed

if __name__ == '__main__':
    exit(run())

