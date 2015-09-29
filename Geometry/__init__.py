'''
XXX missing doc string
'''

try:
    __import__('pkg_resources').declare_namespace(__name__)
except:
    from pkgutil import extend_path
    __path__ = extend_path(__path__,__name__)

from .Point import Point as Point

from .Line import Line as Line
from .Line import Segment as Segment
from .Line import Ray as Ray

from .Triangle import Triangle as Triangle

from .Rectangle import Rectangle as Rectangle

from .Graph import Graph 
from .Graph import Node
from .Graph import Edge

from .Constants import *
from .Exceptions import *

__all__ =  [ 'Point',
             'Line','Segment','Ray',
             'Triangle','Rectangle',
             'Graph','Node','Edge' ]



