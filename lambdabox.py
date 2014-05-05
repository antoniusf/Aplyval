import pyglet

class Box:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lines = []#Lines this box is connected to
        self.update(x, y)

    def update(self, x, y):
        self.x = x
        self.y = y
        self.batch = pyglet.graphics.Batch()
        if self.app == True:
            left = self.x-12
            right = self.x+12
            bottom = self.y-6
            top = self.y+6
            self.s = self.batch.add_indexed(3, pyglet.gl.GL_TRIANGLES, None, [0, 1, 2],
                    ('v2i', (x, y-6, x+12, y+6, x-12, y+6)),
                    ('c3f', (1.0,)*9)
                    )
            self.leftattach = (x-6, y)
            self.topattach = (x, y+6)
            self.bottomattach = (x, y-6)
            self.rightattach = (0, 0)
        else:
            bottom = self.y-12
            left = self.x-16
            top = self.y+12
            right = self.x+16
            self.square = self.batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, None, [0, 1, 2, 2, 0, 3],
                    ('v2i', (left, bottom, right, bottom, right, top, left, top)),
                    ('c3f', (1.0,)*12)
                    )
            self.s = self.batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, None, [0, 1, 2, 2, 0, 3],
                    ('v2i', (right, self.y-4, right+3, self.y-4, right+3, self.y+4, right, self.y+4)),
                    ('c3f', (1.0,)*12)
                    )
            self.topattach = (x, top)
            self.leftattach = (left, y)
            self.rightattach = (right, y)
            self.bottomattach = (x, bottom)

    def hover(self, state=False):
        if state == True:
            self.square.colors = (1.0, 0.0, 0.0)*4
        else:
            self.square.colors = (1.0,)*12

    def checkhover(self, x, y):
        if (x > self.x-16) and (x < self.x+16) and (y > self.y-16) and (y < self.y+16):
            self.hover(True)
        else:
            self.hover(False)

class AbstractorBox(Box):

    def __init__(self, x, y):
        self.app = False
        Box.__init__(self, x, y)
        self.aline = None

    def update(self, x, y):
        Box.update(self, x, y)

    def hover(self, state=False):
        Box.hover(self, state)
        if self.aline:
            self.aline.hover(state)

    def draw(self):
        self.batch.draw()
        if self.aline:
            self.aline.draw()


class ApplicatorBox(Box):

    def __init__(self, x, y):
        self.app = True
        Box.__init__(self, x, y)
        self.inline = None
        self.outline = None

    def update(self, x, y):
        Box.update(self, x, y)

    def hover(self, state=False):
        Box.hover(self, state)
        if self.inline:
            self.inline.hover(state)
        if self.outline:
            self.outline.hover(state)

    def draw(self):
        self.batch.draw()
        if self.inline:
            self.inline.draw()
        if self.outline:
            self.outline.draw()

class Line:

    def __init__(self, start, end, endbox):
        self.sx, self.sy = start
        self.ex, self.ey = end
        self.endbox = endbox

    def draw(self):
        self.endbox.draw()
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                ('v2i', (self.sx, self.sy, self.ex, self.ey)),
                ('c3f', (1.0,)*6)
                )

    def hover(self, state=False):
        self.endbox.hover(state)

window = pyglet.window.Window()
b1 = AbstractorBox(50, 50)
b2 = AbstractorBox(100, 150)
a1 = ApplicatorBox(200, 200)
l1 = Line(b1.rightattach, b2.leftattach, b2)
l2 = Line(b2.rightattach, a1.bottomattach, a1)
l3 = Line(b1.topattach, a1.leftattach, a1)
l4 = Line(b2.topattach, a1.rightattach, a1)
b1.aline = l1
b2.aline = l2
drag = b2

@window.event
def on_draw():
    window.clear()
    b1.draw()
    l3.draw()
    l4.draw()

@window.event
def on_mouse_motion(x, y, dx, dy):
    b1.checkhover(x, y)
    b2.checkhover(x, y)
    a1.checkhover(x, y)

@window.event
def on_mouse_press(symbol, modifier, x, y):
    pass

@window.event
def on_mouse_drag(x, y, dx, dy, symbol, modifier):
    if drag:
        drag.update(x, y)

pyglet.app.run()
