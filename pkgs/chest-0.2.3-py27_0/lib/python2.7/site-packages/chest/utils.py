def raises(err, lamda):
    try:
        lamda()
        return False
    except err:
        return True


def raise_KeyError(key):
    raise KeyError("I asked for one of these %s" % key)
