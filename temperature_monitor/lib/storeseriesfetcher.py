from datetime import datetime as dt


class StoreSeriesFetcher(object):
    """
    Responsible to fetch time series from store as distinct (timestamp, temperature) series
    """
    def __init__(self, store):
        self.store = store

    @staticmethod
    def _format(timestamp, temperature):
            return dt.strptime(timestamp, '%Y-%m-%d %H:%M:%S'), float(temperature)

    def fetch(self, samples=None):
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
                s0.append(self._format(timestamp, temp))
            elif line == '1':
                s1.append(self._format(timestamp, temp))
            else:
                raise Exception("Unknown line %s" % line)
        return s0, s1
