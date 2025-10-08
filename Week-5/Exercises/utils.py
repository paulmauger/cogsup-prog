import math
from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK

FPS  = 60  
MSPF = 1000 / FPS 

def to_frames(t): 
    return math.ceil(t / MSPF) 

def to_time(num_frames): 
    return num_frames * MSPF 

def load(stims): 
    for stim in stims: 
        stim.preload()

def timed_draw(exp, stims):
    t0 = exp.clock.time 
    exp.screen.clear()
    for stim in stims:
        stim.present(clear=False, update=False)
    exp.screen.update()
    elapsed = exp.clock.time - t0 
    return elapsed

def present_for(exp, stims, num_frames):
    if num_frames == 0: 
        return
    dt = timed_draw(exp, stims) 
    if dt > 0:
        t = to_time(num_frames) 
        exp.clock.wait(t - dt) 