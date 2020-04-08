

def save_gif(frames, name='cool_gif.gif'):
    frames[0].save(name, format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0)
    return

