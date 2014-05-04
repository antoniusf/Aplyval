import pyglet

#Ladies and Gentlemen, I present to you:
##My first working lambda calculus interpreter. It passed its first test on Friday, March 2, 2014, at 23:53.

window = pyglet.window.Window(resizable=True)
pyglet.font.add_file('whitrabt.ttf')
textdisplay = pyglet.text.Label(text="", font_name="White Rabbit", font_size=24, x=window.width/2, y=window.height/2, width=window.width, anchor_x="center", anchor_y="center", multiline=True)

text = "--*m*n*f*x--mf--nfx*f*x-f-f-fx*g*y-g-gy"

application = False
def build_tree(text):
    if text[0] == "-":
        l = [None, None]
        l[0], text = build_tree(text[1:])
        l[1], text = build_tree(text[1:])
    elif text[0] == "*":
        l = [text[0:2], None]
        text = text[1:]
        l[1], text = build_tree(text[1:])
        l = (l[0], l[1])
    else:
        l = text[0]
    return l, text

def replace(old, new, l):
    """Recursively replaces."""
    if type(l) == list:
        if l[0] == old:
            r1 = new
        elif type(l[0]) != str:
            r1 = replace(old, new, l[0])
        else:
            r1 = l[0]
        if l[1] == old:
            r2 = new
        elif type(l[1]) != str:
            r2 = replace(old, new, l[1])
        else:
            r2 = l[1]
        return [r1, r2]
    elif type(l) == tuple:
        if l[0] == "*"+old:
            r = l
        else:
            if l[1] == old:
                r = (l[0], new)
            elif type(l[1]) != str:
                r = (l[0], replace(old, new, l[1]))
            else:
                r = l
        return r

def replace_element_by_index(new, indices, l):
    """This function is actually never used. Oh well."""
    index = indices[0]
    if len(indices) == 1 or type(l[index]) == str:
        if type(l) == list:
            return l[:index]+[new]+l[index+1:]
        elif type(l) == tuple:
            return l[:index]+(new,)+l[index+1:]
    else:
        if type(l) == list:
            return l[:index]+[replace_element_by_index(new, indices[1:], l[index])]+l[index+1:]
        elif type(l) == tuple:
            return l[:index]+(replace_element_by_index(new, indices[1:], l[index]),)+l[index+1:]

def step(tree):
    if type(tree) == list and type(tree[0]) == tuple:
        func = tree[0]
        name = func[0][1]
        func = func[1]
        arg = tree[1]
        nfunc = replace(name, arg, func)
        return nfunc
    elif type(tree) == list:
        return [step(tree[0]), step(tree[1])]
    elif type(tree) == tuple:
        return (tree[0], step(tree[1]))
    else:
        return tree

def render(tree):
    if type(tree) == list:
        return "-"+render(tree[0])+render(tree[1])
    elif type(tree) == tuple:
        return tree[0]+render(tree[1])
    else:
        return tree

def get_levels(tree, level=0):
    if type(tree) == list:
        return [level]+get_levels(tree[0], level+1)+get_levels(tree[1], level+1)
    elif type(tree) == tuple:
        return [level, level]+get_levels(tree[1], level+1)
    else:
        return [level]

def draw_text(text, levels):
    positions = []
    length = len(levels)
    xypos = []
    for x in range(len(levels)):
        y = levels[x]
        xypos.append((x, y))
    tlist = []
    for y in range(max(levels)+1):
        tlist.append([])
        for x in range(length):
            tlist[-1].append(" ")
        tlist[-1].append("\n")
    for i in range(len(text)):
        char = text[i]
        x, y = xypos[i]
        tlist[y][x] = char
    endtext = ""
    for l in tlist:
        endtext += "".join(l)
    return endtext

tree = build_tree(text)[0]
#print tree
#print render(tree)
#print get_levels(tree)
textdisplay.text = draw_text(render(tree), get_levels(tree))

@window.event
def on_draw():
    window.clear()
    textdisplay.draw()

@window.event
def on_key_press(symbol, modifiers):
    global tree
    if symbol == pyglet.window.key.ENTER:
        tree = step(tree)
        text = render(tree)
        levels = get_levels(tree)
        textdisplay.text = draw_text(render(tree), get_levels(tree))
        #print textdisplay.text

@window.event
def on_resize(width, height):
    textdisplay.x = window.width/2
    textdisplay.y = window.height/2
    textdisplay.width = window.width

pyglet.app.run()
