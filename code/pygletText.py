import pyglet
snellen = pyglet.font.load('Snellen', 124)
text = pyglet.font.Text(snellen, '43210')
#label = pyglet.text.Label('01234', font_name='Snellen', font_size=14)
window = pyglet.window.Window()

@window.event
def on_draw():
    window.clear()
    text.draw()
    #label.draw()

pyglet.clock.schedule(lambda dt: None)
pyglet.app.run()

