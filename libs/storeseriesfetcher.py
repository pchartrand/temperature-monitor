from datetime import datetime as dt


class StoreSeriesFetcher(object):
    def __init__(self, store):
        self.store = store

    def fetch(self):
        def _format(timestamp, temp):
            return (dt.strptime(timestamp, '%Y-%m-%d %H:%M:%S'), float(temp))

        last = self.store.last()
        s0 = []
        s1 = []
        for i in range(self.store.depth):
            (line, temp, timestamp) = self.store.get_one(last - i)
            if line is None:
                continue
            elif line == '0':
                s0.append(_format(timestamp, temp))
            else:
                s1.append(_format(timestamp, temp))
        return s0, s1
