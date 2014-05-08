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

    def click(self, x, y):
        if self.checkhover(x, y) == True:
            set_drag(self)

class AbstractorBox(Box):

    def __init__(self, x, y):
        self.app = False
        Box.__init__(self, x, y)
        self.aline = None

    def update(self, x, y):
        Box.update(self, x, y)
        bottom = self.y-24
        left = self.x-32
        top = self.y+24
        right = self.x+32
        self.square = self.batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, None, [0, 1, 2, 2, 0, 3],
                ('v2i', (left, bottom, right, bottom, right, top, left, top)),
                ('c3f', (1.0,)*12)
                )
        self.s = self.batch.add_indexed(4, pyglet.gl.GL_TRIANGLES, None, [0, 1, 2, 2, 0, 3],
                ('v2i', (right, self.y-8, right+9, self.y-8, right+9, self.y+8, right, self.y+8)),
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
        if (x > self.x-32) and (x < self.x+32) and (y > self.y-32) and (y < self.y+32):
            self.hover(True)
            return True
        else:
            self.hover(False)
            return False

class ApplicatorBox(Box):

    def __init__(self, x, y):
        self.app = True
        self.inline = None
        self.outline = None
        Box.__init__(self, x, y)

    def update(self, x, y):
        Box.update(self, x, y)
        left = self.x-24
        right = self.x+24
        bottom = self.y-12
        top = self.y+12
        self.triangle = self.batch.add_indexed(3, pyglet.gl.GL_TRIANGLES, None, [0, 1, 2],
                ('v2i', (x, y-12, x+24, y+12, x-24, y+12)),
                ('c3f', (1.0,)*9)
                )
        self.leftattach = (x-12, y)
        self.topattach = (x, y+12)
        self.bottomattach = (x, y-12)
        self.rightattach = (0, 0)
        if self.inline:
            self.inline.update_start(self.topattach[0], self.topattach[1])
        elif self.outline:
            self.outline.update_start(self.bottomattach[0], self.bottomattach[1])

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
        ax = -24.0#a = (-12, 12)
        ay = 24.0
        bx = 24.0#b = (12, 12)
        by = 24.0
        px = x-self.x#do some conversion to port the mouse coordinates into a coordinate system based on the tip of the triangle
        py = y-self.y+12.0
        r = (-py*bx/by+px)/(-ay*bx/by+ax)#calculate r and s values to represent the point by a and b
        s = (px-r*ax)/bx
        if r<1 and r>0 and s<1 and s>0 and (r+s)<1 and (r+s)>0:#standard point-in-triangle test
            self.hover(True)
            return True
        else:
            self.hover(False)
            return False

class Line:

    def __init__(self, start, end):
        self.sx, self.sy = start
        self.ex, self.ey = end
        self.endbox = None

    def update_start(self, x, y):
        self.sx = x
        self.sy = y

    def update_end(self, x, y):
        self.ex = x
        self.ey = y

    def draw(self):
        if self.endbox:
            self.endbox.draw()
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                ('v2i', (self.sx, self.sy, self.ex, self.ey)),
                ('c3f', (1.0,)*6)
                )

    def hover(self, state=False):
        if self.endbox:
            self.endbox.hover(state)

window = pyglet.window.Window()
boxes = []
drag = None
dragline = False

def set_drag(box):
    global drag
    drag = box

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
    global dragline
    global drag
    for box in boxes:
        box.click(x, y)
    if drag:
        if button == pyglet.window.mouse.LEFT:
            dragline = False
        elif button == pyglet.window.mouse.RIGHT:
            if modifier & pyglet.window.key.MOD_SHIFT:
                line = Line(drag.rightattach, (x, y))
                drag.aline = line
            elif modifier & pyglet.window.key.MOD_CTRL:
                line = Line(drag.bottomattach, (x, y))
                drag.outline = line
            else:
                line = Line(drag.topattach, (x, y))
                drag.inline = line
            drag = line
            dragline = True
    elif drag == None:
        if button == pyglet.window.mouse.LEFT:
            boxes.append(AbstractorBox(x, y))
        elif button == pyglet.window.mouse.RIGHT:
            boxes.append(ApplicatorBox(x, y))

@window.event
def on_mouse_release(x, y, button, modifier):
    global drag
    drag = None

@window.event
def on_mouse_drag(x, y, dx, dy, symbol, modifier):
    global drag
    if drag:
        if dragline == True:
            drag.update_end(x, y)
        else:
            drag.update(x, y)

@window.event
def on_key_press(symbol, modifiers):
    print drag

pyglet.app.run()
