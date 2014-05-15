import pyglet
from pyglet.gl import *

class Triangle:

    def __init__(self, a, b, c, color, batch):
        """Takes a, b and c as position vec2 vectors to the three vertices of the triangle and a color triple."""
        self.vertexlist = None
        self.color = color
        self.update(a, b, c)
        self.add_to_batch(batch)

    def update(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        if self.vertexlist:
            self.vertexlist.vertices = self.a.coords()+self.b.coords()+self.c.coords()

    def add_to_batch(self, batch):
        self.vertexlist = batch.add(3, GL_TRIANGLES, None,
                ('v2f', (self.a.coords()+self.b.coords()+self.c.coords())),
                ('c4f', (self.color+(1.0,))*3)
                )

    def highlight(self, state=False):
        if self.vertexlist:
            if state == True:
                self.vertexlist.colors = (0.5+self.color[0]*0.5, 0.5+self.color[1]*0.5, 0.5+self.color[2]*0.5, 1.0)*3
            elif state == False:
                self.vertexlist.colors = (self.color+(1.0,))*3
        else:
            raise AttributeError

    def collide_point(self, point):
        ax, ay = (self.a-self.c).coords()
        bx, by = (self.b-self.c).coords()
        p = self.c
        px = point.x-p[0]#do some conversion to port the mouse coordinates into a coordinate system based on the tip of the triangle
        py = point.y-p[1]
        r = (-py*bx/by+px)/(-ay*bx/by+ax)#calculate r and s values to represent the point by a and b
        s = (px-r*ax)/bx
        if r<1 and r>0 and s<1 and s>0 and (r+s)<1 and (r+s)>0:#standard point-in-triangle test
            return True
        else:
            return False

    def gethover(self, point):
        hover = self.collide_point(point)
        self.highlight(hover)
        return hover
