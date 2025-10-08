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

""" Experiment """
def run_trial(side="L"):

    pos_fix = [300, 0] if side == "L" else [-300, 0]
    fixation = stimuli.FixCross(size=(150, 150), line_width=10, position=pos_fix)
    fixation.preload()

    radius = 75
    circle = make_circle(radius)

    fixation.present(True, False)
    circle.present(False, True)

    posX, posY = 0, 0
    size = 1
    exp.screen.clear()

    while True: 

        key, _ = exp.keyboard.wait(keys = [K_DOWN, K_UP, K_LEFT, K_RIGHT, K_1, K_2, K_SPACE])

        if key == K_DOWN:
            posY -= 5
        elif key == K_UP:
            posY += 5
        elif key == K_LEFT: 
            posX -= 5 
        elif key == K_RIGHT: 
            posX += 5
        
        elif key == K_1: 
            size = 1
        elif key == K_2: 
            size = 2

        elif key == K_SPACE: 
            break

        circle = make_circle(r=size*75, pos=(posX, posY))

        circle.present(False, False)
        fixation.present(False, False)

        exp.screen.update()
        exp.screen.clear()

        if exp.keyboard.check(K_SPACE):
            break
        





        

control.start(subject_id=1)

run_trial("R")
    
control.end()