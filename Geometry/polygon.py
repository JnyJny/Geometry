'''

'''

import math
from .exceptions import InfiniteLength
from .point2 import Point, PointCollection

class Polygon(PointCollection):

    @property
    def perimeter(self):
        '''
        Sum of the length of all sides.
        '''
        try:
            return self._perimeter
        except AttributeError:
            pass
    
        if self.closed:
            self._perimeter = sum([a.distance(b) for a,b in self.pairs])
            return self._perimeter
        raise InfiniteLength()

    @property
    def closed(self):
        '''
        Property :closed: is true if the point collection's last
        point is equal to the first point. 
        '''
        try:
            return self._closed
        except AttributeError:
            pass
        self._closed = True
        return self._closed
    
    @closed.setter
    def closed(self, value):
        self._closed = bool(value)
        
    @property
    def sides(self):
        '''
        A list of point pairs. 
        '''
        try:
            return self._pairs
        except AttributeError:
            pass
        keys = [k for k in self.keys()]
        if len(keys) <= 1:
            return []
        
        if len(keys) == 2:
            return [tuple(self.values()),]
        
        if self.closed:
            keys.append(keys.pop(0))
        else:
            keys.pop(0)
        self._pairs = [(self[x],self[y]) for x,y in zip(self.keys(),keys)]
        return self._pairs
    
