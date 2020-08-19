import os


def get_plugin_list():
    pluginsdir = os.path.join(os.getcwd(), 'src/plugins/')
    contents = os.scandir(pluginsdir)
    plugins = map(
        lambda direntry: direntry.name,
        filter(lambda direntry: direntry.is_dir() and direntry.name != '__pycache__', contents)
    )
    return plugins
