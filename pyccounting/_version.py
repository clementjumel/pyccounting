from importlib import metadata

__version__: str = metadata.version(__package__)  # __version__ is like "x.y.z"
