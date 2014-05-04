import pyglet

#Ladies and Gentlemen, I present to you:
##My first working lambda calculus interpreter. It passed its first test on Friday, March 2, 2014, at 23:53.

window = pyglet.window.Window(resizable=True)
pyglet.font.add_file('whitrabt.ttf')
textdisplay = pyglet.text.Label(text="", font_name="White Rabbit", font_size=24, x=window.width/2, y=window.height/2, width=window.width, anchor_x="center", anchor_y="center", multiline=True)

text = "--*m*n*f*x--mf--nfx*f*x-f-f-fx*g*y-g-gy"

application = False
def build_tree(text):
    """This function takes a lambda expression in the style seen above (polish notation, "-" is for applications, "*" for abstractions) and transforms it into a tree of nested lists and tuples. A list represents an application the first element on the second. A tuple represents an abstraction, where the first element is the variable to be bound (the star is left before) and the second element is the body. Both of course can be nested."""
    if text[0] == "-":#Application
        l = [None, None]
        l[0], text = build_tree(text[1:])#use build_tree recursively to allow nested stuff, return text so that the next function can continue where the nested one left off.
        l[1], text = build_tree(text[1:])
    elif text[0] == "*":#Abstraction
        l = [text[0:2], None]
        text = text[1:]#the variable has to be removed before proceeding
        l[1], text = build_tree(text[1:])#same as above
        l = (l[0], l[1])
    else:
        l = text[0]
    return l, text

def replace(old, new, l):
    """Recursively replaces. This is the function that's actually called for applications."""
    if type(l) == list:#Here both elements need to be checked
        if l[0] == old:#Replacement
            r1 = new
        elif type(l[0]) != str:#if it's either list or tuple
            r1 = replace(old, new, l[0])#recursive checking is needed
        else:
            r1 = l[0]#nothing changes
        if l[1] == old:#same as above
            r2 = new
        elif type(l[1]) != str:
            r2 = replace(old, new, l[1])
        else:
            r2 = l[1]
        return [r1, r2]#assemble the new list with replacements done and return
    elif type(l) == tuple:#Here only the second element needs to be checked. Also, if the Abstraction here defines the variable that's been looked for, stop looking in there (namespacing)
        if l[0] == "*"+old:#if the abstraction also defines the variable to replace (see above)
            r = l
        else:
            if l[1] == old:#the same stuff as above, just for one element
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
    """This function does the actual lambda calculus transformations recursively and then reassembles the transformed expression."""
    if type(tree) == list and type(tree[0]) == tuple:#This basically looks for any applications it can do directly. These applications are the ones where the function is already defined through abstraction. That's why it checks whether the first element of the list (for application) is an abstraction
        func = tree[0]#The whole function with parameter and body
        name = func[0][1]#Only the parameter
        func = func[1]#Only the body
        arg = tree[1]
        nfunc = replace(name, arg, func)#The replacement of all occurences of the parameter in the body with the argument
        return nfunc
    elif type(tree) == list:
        return [step(tree[0]), step(tree[1])]#recursive checking, again
    elif type(tree) == tuple:
        return (tree[0], step(tree[1]))
    else:
        return tree

def render(tree):
    """This function turns a tree into the text format explained at the beginning."""
    if type(tree) == list:
        return "-"+render(tree[0])+render(tree[1])
    elif type(tree) == tuple:
        return tree[0]+render(tree[1])
    else:
        return tree

def get_levels(tree, level=0):
    """The only thing this function does is returning the level (as in nested level) for every text character (as rendered by render) in a list"""
    if type(tree) == list:
        return [level]+get_levels(tree[0], level+1)+get_levels(tree[1], level+1)
    elif type(tree) == tuple:
        return [level, level]+get_levels(tree[1], level+1)
    else:
        return [level]

def draw_text(text, levels):
    """This function does the conversion of text and associated levels to a formatted block of text."""
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
