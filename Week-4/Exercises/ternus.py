from expyriment import design, control, stimuli
from expyriment.misc.constants import K_SPACE


def load(stims : list[stimuli._stimulus]) -> None:
    for stim in stims: 
        stim.preload()


def draw(stims : list[stimuli._stimulus]) -> float:
    """Return the execution time to draw the stimulus"""

    if stims == []:
        return 0.
    
    t0 = exp.clock.time
    for i, stim in enumerate(stims):
        stim.present(clear=(i==0), update=(i == len(stims)-1))
    t1 = exp.clock.time

    return (t1-t0)


def present_for(stims : list[stimuli._stimulus], t:int) -> None:
    """Present the stimulus for a time t"""

    t0 = draw(stims)
    exp.clock.wait(t-t0)
    exp.screen.clear()

colors = {
    1:"yellow",
    2:"red",
    3:"green",
    4:"yellow"
}

def make_circles(circles: list[int], radius:int, color_tags:bool) -> None:
    """There are 4 circles: return the ones specified in the circles list with a certain radius as stimulus"""


    step = radius * 3 #distance of 3 radius between circles
    circles_stims = []

    for i in circles: 
        pos = ((i - 2.5) * step, 0)
        c = stimuli.Circle(radius = radius, position=(pos), anti_aliasing=10)
        circles_stims.append(c)

        if color_tags: 
            ct = stimuli.Circle(radius=radius/3, position=(0, 0), colour=colors[i], anti_aliasing=10)
            ct.plot(c)
    
    return circles_stims



def run_trial(radius:int, color_tags:bool, ISI:int, t:int): 
    

    c1 = make_circles([1,2,3], radius, color_tags)
    c2 = make_circles([2,3,4], radius, color_tags)

    load(c1)
    load(c2)

    while True:    
        if exp.keyboard.check(K_SPACE):
            break

        for c in [c1, c2]:
            present_for(c, t)
            exp.screen.clear()
            exp.screen.update()
            exp.clock.wait(ISI)







exp = design.Experiment(name="Ternus")

control.set_develop_mode()
control.initialize(exp)


control.start()


run_trial(radius=30, color_tags=False, ISI=50, t=200)
run_trial(radius=30, color_tags=False, ISI=200, t=200)
run_trial(radius=30, color_tags=True, ISI=200, t=200)

control.end()