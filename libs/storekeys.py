class KeyMixin(object):
    """Utility class to generate and maintain keys used to get/set values in the store
    """
    KEY_TEMPLATES = ['line', 'temp', 'time']
    keys = {}

    @staticmethod
    def _make_key(key, i):
        return '%s_%i' % (key, i)

    def make_keys(self, i):
        for key in self.KEY_TEMPLATES:
            self.keys[key] = self._make_key(key, i)

    def get_key(self, key):
        return self.keys.get(key)

    def get_keys(self):
        return [self.get_key(key) for key in self.KEY_TEMPLATES]

    def get_value(self, data, key):
        return data.get(self.get_key(key))