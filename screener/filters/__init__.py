import pkgutil


def load_workers():
    for loader, name, _ in pkgutil.walk_packages(__path__):
        try:
            loader.find_module(name).load_module(name)
        except Exception as e:
            print("Failed to load filter", name, e)


load_workers()
