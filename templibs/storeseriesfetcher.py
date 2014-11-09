from datetime import datetime as dt


class StoreSeriesFetcher(object):
    """
    Responsible to fetch time series from store as distinct (timestamp, temperature) series
    """
    def __init__(self, store):
        self.store = store

    def fetch(self, samples=None):
        def _format(timestamp, temp):
            return dt.strptime(timestamp, '%Y-%m-%d %H:%M:%S'), float(temp)

        if samples is None:
            samples = self.store.depth

        last = self.store.last()
        s0 = []
        s1 = []
        for i in range(samples):
            (line, temp, timestamp) = self.store.get_one(last - i)
            if line is None:
                continue
            elif line == '0':
                s0.append(_format(timestamp, temp))
            else:
                s1.append(_format(timestamp, temp))
        return s0, s1
