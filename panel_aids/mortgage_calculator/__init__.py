"""examples in the panel ecosystem."""
__version__ = __import__("datetime").date.today().strftime("%Y.%m.%d")

with __import__("importnb").Notebook():
    from . import mortgage_calculator
    from .mortgage_calculator import *
