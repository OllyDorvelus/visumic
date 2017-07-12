__author__ = 'OllyD'
# from .base import *
# from .local import *
from .base import *
from .production import *

try:
    from .local import *
except:
    pass