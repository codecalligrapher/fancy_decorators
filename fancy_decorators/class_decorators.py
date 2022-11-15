instances = {}
def singleton(instance):
# On @ decoration
    def on_call(*args, **kwargs):
        # On instance creation
        if instance = not in instances:
            instances[instance] = instance(*args, **kwargs)
        return instances[instance]
    return on_call 