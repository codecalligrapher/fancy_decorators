def singleton(cls):
    '''Class-based singleton enforcement'''
    instance = None
    def on_call(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance
    return on_call
