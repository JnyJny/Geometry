'''
'''

import collections


def FloatProperty(name, default=0.0, readonly=False):
    '''
    '''
    private_name = '_' + name

    @property
    def prop(self):
        if not hasattr(self, private_name):
            setattr(self, private_name, default)
        return getattr(self, private_name)

    if not readonly:
        @prop.setter
        def prop(self, newValue):
            try:
                setattr(self, private_name, float(newValue))
                return
            except TypeError:
                pass

            if isinstance(newValue, collections.Mapping):
                try:
                    setattr(self, private_name, float(newValue[name]))
                except KeyError:
                    pass
                return

            if isinstance(newValue, collections.Iterable):
                try:
                    setattr(self, private_name, float(newValue[0]))
                    return
                except IndexError:
                    pass

            try:
                mapping = vars(newValue)
                setattr(self, private_name, float(mapping[name]))
                return
            except (TypeError, KeyError):
                pass

            if newValue is None:
                setattr(self, private_name, float(default))
                return

            raise ValueError(newValue)
    return prop


def FloatMultiProperty(keys, default=0.0, readonly_keys='', all_keys='xyzw'):
    '''
    '''

    if not any(set(keys).intersection(all_keys)):
        raise KeyError(keys)

    writable_keys = [k for k in keys if k not in readonly_keys]

    @property
    def prop(self):
        return list(self[key] for key in keys)

    @prop.setter
    def prop(self, newValues):

        if newValues is None:
            for key in writable_keys:
                setattr(self, key, default)
            return

        if isinstance(newValues, collections.Mapping):
            for key, value in newValues.items():
                if key in writable_keys:
                    setattr(self, key, value)
            return

        if isinstance(newValues, collections.Iterable):
            for key, value in zip(writable_keys, newValues):
                setattr(self, key, value)
            return

        try:
            mapping = vars(newValues)
            for key, value in mapping.items():
                if key in writable_keys:
                    setattr(self, key, value)
            return
        except TypeError:
            pass
        setattr(self, writable_keys[0], newValues)

    return prop
