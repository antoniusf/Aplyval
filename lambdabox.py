import pyglet, math

class Vector:

    def __init__(self, *args):
        """Takes coordinates either as a tuple or separate"""
        self.set(args)

    def set(self, *args):
        """Takes coordinates either as a tuple or separate"""
        if len(args) == 1:
            arg = args[0]
            self.x = arg[0]
            self.y = arg[1]
        elif len(args) == 2:
            self.x = args[0]
            self.y = args[1]
        else:
            raise TypeError("Vector.__init__() takes either one or two arguments; "+len(args)+" given.")

    def coords(self):
        return self.x, self.y

    def __add__(self, other):
        if type(other) == type(self):
            print "Hello"
            t = Vector(self.x+other.x, self.y+other.y)
            return None
        else:
            raise TypeError

    def __sub__(self, other):
        if type(other) == type(self):
            return Vector(self.x-other.x, self.y-other.y)
        else:
            raise TypeError

    def __repr__(self):
        return "Vector ("+str(self.x)+", "+str(self.y)+")"

    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y

class Box:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lines = []#Lines this box is connected to
        self.triangleconstant = math.tan(math.pi/8)/(math.tan(math.pi/8)+1)
        self.calc_s1_s2(48)
        self.update(x, y)

    def calc_s1_s2(self, width):
        """s1 and s2 are lengths for calculating the corner coordinates from the center one"""
        self.s1 = width*self.triangleconstant
        self.s2 = width-self.s1

    def point_in_triangle(self, p, a, b, x, y):
        """p: position vector to a and b; a, b: vectors defining the triangle; x, y: coordinates of the point"""
        ax, ay = a.coords()
        ax = float(ax); ay = float(ay)
        bx, by = b.coords()
        bx = float(bx); by = float(by)
        px = x-p[0]#do some conversion to port the mouse coordinates into a coordinate system based on the tip of the triangle
        py = y-p[1]
        r = (-py*bx/by+px)/(-ay*bx/by+ax)#calculate r and s values to represent the point by a and b
        s = (px-r*ax)/bx
        if r<1 and r>0 and s<1 and s>0 and (r+s)<1 and (r+s)>0:#standard point-in-triangle test
            return True
        else:
            return False

    def update(self, x, y):
        self.x = x
        self.y = y
        self.batch = pyglet.graphics.Batch()

    def click(self, x, y):
        if self.checkhover(x, y) == True:
            set_drag(self)

class AbstractorBox(Box):

    def __init__(self, x, y):
        self.topline = None
        self.rightline = None
        self.bottomline = None
        Box.__init__(self, x, y)
        
    def get_vertices(self, centerx, centery):
        left = centerx-self.s2
        right = centerx+self.s1
        bottom = centery-self.s2
        top = centery+self.s1
        return Vector(right, bottom), Vector(right, top), Vector(left, top)

    def update(self, x, y):
        Box.update(self, x, y)
        self.a, self.b, self.c = a, b, c = self.get_vertices(x, y)
        self.triangle = self.batch.add(3, pyglet.gl.GL_TRIANGLES, None,
                ('v2f', (a.x, a.y, b.x, b.y, c.x, c.y)),
                ('c4f', (1.0,)*12)
                )
        self.left_triangle = self.batch.add(3, pyglet.gl.GL_TRIANGLES, None,
                ('v2f', (a.x, a.y, b.x, b.y, x, y)),
                ('c4f', (1.0, 1.0, 1.0, 0.0)*3)
                )
        self.bottom_triangle = self.batch.add(3, pyglet.gl.GL_TRIANGLES, None,
                ('v2f', (b.x, b.y, c.x, c.y, x, y)),
                ('c4f', (1.0, 1.0, 1.0, 0.0)*3)
                )
        self.right_triangle = self.batch.add(3, pyglet.gl.GL_TRIANGLES, None,
                ('v2f', (c.x, c.y, a.x, a.y, x, y)),
                ('c4f', (1.0, 1.0, 1.0, 0.0)*3)
                )
        self.leftattach = (x-12, y)
        self.topattach = (x, y+12)
        self.bottomattach = (x, y-12)
        self.rightattach = (0, 0)

    def hover(self, state=False):
        if state == True:
            self.triangle.colors = (1.0, 0.0, 0.0, 1.0)*3
        else:
            self.triangle.colors = (1.0,)*12

    def draw(self):
        self.batch.draw()

    def checkhover(self, x, y):
        hover = self.point_in_triangle(self.a, self.b-self.a, self.c-self.a, x, y)
        if hover:
            self.hover(True)
            lefthover = self.point_in_triangle(self.a, self.b-self.a, Vector(self.x, self.y)-self.a, x, y)
            bottomhover = self.point_in_triangle(self.b, self.c-self.b, Vector(self.x, self.y)-self.b, x, y)
            righthover = self.point_in_triangle(self.c, self.a-self.c, Vector(self.x, self.y)-self.c, x, y)
            if bottomhover:
                self.bottom_triangle.colors = (1.0, 1.0, 1.0, 0.5)*3
            else:
                self.bottom_triangle.colors = (1.0, 1.0, 1.0, 0.0)*3
            if lefthover:
                self.left_triangle.colors = (1.0, 1.0, 1.0, 0.5)*3
            else:
                self.left_triangle.colors = (1.0, 1.0, 1.0, 0.0)*3
            if righthover:
                self.right_triangle.colors = (1.0, 1.0, 1.0, 0.5)*3
            else:
                self.right_triangle.colors = (1.0, 1.0, 1.0, 0.0)*3
            return True
        else:
            self.hover(False)
            self.bottom_triangle.colors = (1.0, 1.0, 1.0, 0.0)*3
            self.left_triangle.colors = (1.0, 1.0, 1.0, 0.0)*3
            self.right_triangle.colors = (1.0, 1.0, 1.0, 0.0)*3
            return False

class ApplicatorBox(Box):

    def __init__(self, x, y):
        self.leftline = None
        self.rightline = None
        self.bottomline = None
        Box.__init__(self, x, y)
        
    def get_vertices(self, centerx, centery):
        left = centerx-self.s1
        right = centerx+self.s2
        bottom = centery-self.s1
        top = centery+self.s2
        return Vector(left, top), Vector(left, bottom), Vector(right, bottom)

    def update(self, x, y):
        Box.update(self, x, y)
        self.a, self.b, self.c = a, b, c = self.get_vertices(x, y)
        self.triangle = self.batch.add(3, pyglet.gl.GL_TRIANGLES, None,
                ('v2f', (a.x, a.y, b.x, b.y, c.x, c.y)),
                ('c4f', (1.0,)*12)
                )
        self.left_triangle = self.batch.add(3, pyglet.gl.GL_TRIANGLES, None,
                ('v2f', (a.x, a.y, b.x, b.y, x, y)),
                ('c4f', (1.0, 1.0, 1.0, 0.0)*3)
                )
        self.bottom_triangle = self.batch.add(3, pyglet.gl.GL_TRIANGLES, None,
                ('v2f', (b.x, b.y, c.x, c.y, x, y)),
                ('c4f', (1.0, 1.0, 1.0, 0.0)*3)
                )
        self.right_triangle = self.batch.add(3, pyglet.gl.GL_TRIANGLES, None,
                ('v2f', (c.x, c.y, a.x, a.y, x, y)),
                ('c4f', (1.0, 1.0, 1.0, 0.0)*3)
                )
        self.leftattach = (x-12, y)
        self.topattach = (x, y+12)
        self.bottomattach = (x, y-12)
        self.rightattach = (0, 0)

    def hover(self, state=False):
        if state == True:
            self.triangle.colors = (1.0, 0.0, 0.0, 1.0)*3
        else:
            self.triangle.colors = (1.0,)*12

    def draw(self):
        self.batch.draw()

    def checkhover(self, x, y):
        hover = self.point_in_triangle(self.a, self.b-self.a, self.c-self.a, x, y)
        if hover:
            self.hover(True)
            lefthover = self.point_in_triangle(self.a, self.b-self.a, Vector(self.x, self.y)-self.a, x, y)
            bottomhover = self.point_in_triangle(self.b, self.c-self.b, Vector(self.x, self.y)-self.b, x, y)
            righthover = self.point_in_triangle(self.c, self.a-self.c, Vector(self.x, self.y)-self.c, x, y)
            if bottomhover:
                self.bottom_triangle.colors = (1.0, 1.0, 1.0, 0.5)*3
            else:
                self.bottom_triangle.colors = (1.0, 1.0, 1.0, 0.0)*3
            if lefthover:
                self.left_triangle.colors = (1.0, 1.0, 1.0, 0.5)*3
            else:
                self.left_triangle.colors = (1.0, 1.0, 1.0, 0.0)*3
            if righthover:
                self.right_triangle.colors = (1.0, 1.0, 1.0, 0.5)*3
            else:
                self.right_triangle.colors = (1.0, 1.0, 1.0, 0.0)*3
            return True
        else:
            self.hover(False)
            self.bottom_triangle.colors = (1.0, 1.0, 1.0, 0.0)*3
            self.left_triangle.colors = (1.0, 1.0, 1.0, 0.0)*3
            self.right_triangle.colors = (1.0, 1.0, 1.0, 0.0)*3
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
pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
fpsdisplay = pyglet.clock.ClockDisplay()
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
    fpsdisplay.draw()

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
