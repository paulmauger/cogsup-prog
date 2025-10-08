from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK, K_SPACE, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_1, K_2
import math

""" Global settings """
exp = design.Experiment(name="Blindspot", background_colour=C_WHITE, foreground_colour=C_BLACK)
control.set_develop_mode()
control.initialize(exp)

FPS  = 60  
MSPF = 1000 / FPS 




""" Stimuli """
def make_circle(r, pos=(0,0)):
    c = stimuli.Circle(r, position=pos, anti_aliasing=10)
    c.preload()
    return c

key_names = {
    K_DOWN:"down",
    K_UP:"up",
    K_LEFT:"left",
    K_RIGHT:"right",
    K_1:"1",
    K_2:"2"
}

""" Experiment """
def run_trial(side="L"):
    exp.add_data_variable_names(["eye", "key", "radius", "xcord", "ycord"]) 
    eye = "left" if side == "L" else "right"
    
    text1 = stimuli.TextBox(f"Close your {eye} eye and fixate the cross. Move the circle until you find the blind spot.", size = (300, 100), position=(0,50))
    text2 = stimuli.TextBox("Use the arrows keys to move the circle and 1/2 to change its size. Press SPACE to start and stop.", size = (300, 100), position=(0,-50))
    
    text1.preload()
    text2.preload()

    text1.present(True, False)
    text2.present(False, True)

    exp.keyboard.wait(K_SPACE)

    pos_fix = [300, 0] if side == "L" else [-300, 0]
    fixation = stimuli.FixCross(size=(150, 150), line_width=10, position=pos_fix)
    fixation.preload()

    size = 75
    circle = make_circle(size)

    fixation.present(True, False)
    circle.present(False, True)

    posX, posY = 0, 0
    exp.screen.clear()

    while True: 

        key, _ = exp.keyboard.wait(keys = [K_DOWN, K_UP, K_LEFT, K_RIGHT, K_1, K_2, K_SPACE])

        if key == K_DOWN:
            posY -= 8
        elif key == K_UP:
            posY += 8
        elif key == K_LEFT: 
            posX -= 8 
        elif key == K_RIGHT: 
            posX += 8
        
        elif key == K_1: 
            size += 5
        elif key == K_2: 
            size -= 5

        elif key == K_SPACE:
            exp.data.add([side, "space", size, posX, posY])
            break

        exp.data.add([side, key_names[key], size, posX, posY])

        circle = make_circle(r=size, pos=(posX, posY))

        fixation.present(True, False)
        circle.present(False, True)








control.start(subject_id=1)

run_trial("R")
    
control.end()