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

class AbstractorBox(Box):

    def __init__(self, x, y):
        self.app = False
        Box.__init__(self, x, y)
        self.aline = None

    def update(self, x, y):
        Box.update(self, x, y)
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
        if self.aline:
            self.aline.hover(state)

    def draw(self):
        self.batch.draw()
        if self.aline:
            self.aline.draw()

    def checkhover(self, x, y):
        if (x > self.x-16) and (x < self.x+16) and (y > self.y-16) and (y < self.y+16):
            self.hover(True)
        else:
            self.hover(False)

class ApplicatorBox(Box):

    def __init__(self, x, y):
        self.app = True
        Box.__init__(self, x, y)
        self.inline = None
        self.outline = None

    def update(self, x, y):
        Box.update(self, x, y)
        left = self.x-12
        right = self.x+12
        bottom = self.y-6
        top = self.y+6
        self.triangle = self.batch.add_indexed(3, pyglet.gl.GL_TRIANGLES, None, [0, 1, 2],
                ('v2i', (x, y-6, x+12, y+6, x-12, y+6)),
                ('c3f', (1.0,)*9)
                )
        self.leftattach = (x-6, y)
        self.topattach = (x, y+6)
        self.bottomattach = (x, y-6)
        self.rightattach = (0, 0)

    def hover(self, state=False):
        if state == True:
            self.triangle.colors = (1.0, 0.0, 0.0)*3
        else:
            self.triangle.colors = (1.0,)*9
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

    def checkhover(self, x, y):
        #a, b: two vectors going from the lower tip of the triangle to the right or left edge
        ax = -12.0#a = (-12, 12)
        ay = 12.0
        bx = 12.0#b = (12, 12)
        by = 12.0
        px = x-self.x#do some conversion to port the mouse coordinates into a coordinate system based on the tip of the triangle
        py = y-self.y+6.0
        r = (-py*bx/by+px)/(-ay*bx/by+ax)#calculate r and s values to represent the point by a and b
        s = (px-r*ax)/bx
        if r<1 and r>0 and s<1 and s>0 and (r+s)<1 and (r+s)>0:#standard point-in-triangle test
            self.hover(True)
        else:
            self.hover(False)

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
boxes = []

@window.event
def on_draw():
    window.clear()
    for box in boxes:
        box.draw()

@window.event
def on_mouse_motion(x, y, dx, dy):
    for box in boxes:
        box.checkhover(x, y)

@window.event
def on_mouse_press(x, y, button, modifier):
    if button == pyglet.window.mouse.LEFT:
        boxes.append(AbstractorBox(x, y))
    elif button == pyglet.window.mouse.RIGHT:
        boxes.append(ApplicatorBox(x, y))

@window.event
def on_mouse_drag(x, y, dx, dy, symbol, modifier):
    pass

pyglet.app.run()
