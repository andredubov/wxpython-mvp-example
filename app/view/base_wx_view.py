from wx import Frame
from abc import ABCMeta

class WxABCMeta(ABCMeta, type(Frame)):
    pass

class WxViewMixin(metaclass=WxABCMeta):
    """Базовый миксин для всех wxPython представлений"""
    pass