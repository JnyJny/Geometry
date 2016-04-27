"""support for geometric computation


"""

try:
    __import__('pkg_resources').declare_namespace(__name__)
except:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)

__author__ = '\n'.join(["Erik O'Shaughnessy",
                        'erik.oshaughnessy@gmail.com',
                        'https://github.com/JnyJny/Geometry'])

__version__ = "0.0.23"

from .point2 import Point, PointCollection
from .ellipse import Ellipse, Circle
from .line import Line, Segment, Ray
from .triangle import Triangle
from .rectangle import Rectangle
from .graph import Node, Edge, Graph
from .constants import *
from .exceptions import *
from .polygon import Polygon

__all__ = ['Point','PointCollection',
           'Polygon',
           'Ellipse', 'Circle',
           'Line', 'Segment', 'Ray',
           'Triangle', 'Rectangle',
           'Graph', 'Node', 'Edge',
           'ZeroSlope', 'InfiniteSlope', 'CollinearPoints',
           'InfiniteLength', 'ParallelLines', 'CollinearLines',
           'epsilon',
           '__author__', '__version__']
