"""Module providing several classes for handling grid objects"""

class __GridIterator__(object):

    def __init__(self, nx, ny, x, y):
        self.x = x-1
        self.y = y
        self.nx = nx
        self.ny = ny

    def __next__(self):
        if self.x == self.nx-1:
            self.x = 0
            self.y += 1
            if self.y > self.ny-1:
                raise StopIteration()
            else:
                return (self.x, self.y)
        else:
            self.x += 1
            return (self.x, self.y)

class BaseGrid(object):

    def __init__(self, nx, ny, periodicity=(False,False)):
        self.nx = nx
        self.ny = ny
        self.cells = [[None for y in range(ny)] for x in range(nx)]
        self.periodicity = periodicity

    def copy(self):
        grid = BaseGrid(self.nx, self.ny, self.periodicity)
        for x,y in self:
            grid[x,y] = self[x,y]
        return grid

    def __len__(self):
        """Returns the number of cells contained on the grid."""
        return self.nx * self.ny

    def __getitem__(self, key):
        x,y = key
        if self.periodicity[0]:
            x %= self.nx
        if self.periodicity[1]:
            y %= self.ny
        return self.cells[x][y]

    def __setitem__(self, key, value):
        self.cells[key[0]][key[1]] = value

    def __iter__(self, x=0, y=0):
        """Iterate over coordinates."""
        return __GridIterator__(self.nx, self.ny, x, y)

    def __repr__(self):
        return str(self.cells)

    def itercells(self):
        """Iterate over cell values"""
        for x,y in self:
            yield self[x,y]

    def fill(self, value):
        for x,y in self:
            self[x,y] = value
