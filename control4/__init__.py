# -*- coding:utf-8 -*-
import logging

from .control4 import Control4

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = ['Control4']
