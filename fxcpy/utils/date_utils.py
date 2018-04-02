from datetime import datetime, timedelta

def ole_zero():
    return datetime(1899,12,30)

def to_ole(pydate):
    if isinstance(pydate, datetime):
        delta = pydate - ole_zero()
        return float(delta.days) + (float(delta.seconds) / 86400)
    else:
        return pydate

def fm_ole(oletime):
    if isinstance(oletime, float):
        return ole_zero() + timedelta(days=float(oletime))
    else:
        return oletime
