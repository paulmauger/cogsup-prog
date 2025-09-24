from expyriment import design, control, stimuli, io
import expyriment.misc.geometry as geo

control.set_develop_mode()

# Create an object of class Experiment: This stores the global settings of your experiment & handles the data file, screen, and input devices
exp = design.Experiment(name = "Square")

# Initialize the experiment: Must be done before presenting any stimulus
control.initialize(exp)

size = exp.screen.size[0] // 20

width = exp.screen.size[0]
height = exp.screen.size[1]

#create 4 squares at the corners of the screen: positions are relative to the screen size
pos1 = geo.coordinates_to_position((exp.screen.size[0]-size//2, exp.screen.size[1]-size//2))
pos2 = geo.coordinates_to_position((size//2, exp.screen.size[1]-size//2))
pos3 = geo.coordinates_to_position((exp.screen.size[0]-size// 2, size//2))
pos4 = geo.coordinates_to_position((size//2, size//2))

square1 = stimuli.Rectangle(size=
(size, size), colour="red", position=(pos1), line_width=1)
square2 = stimuli.Rectangle((size, size), colour="red", position=(pos2), line_width=1)
square3 = stimuli.Rectangle((size, size), colour="red", position=(pos3), line_width=1)
square4 = stimuli.Rectangle((size, size), colour="red", position=(pos4), line_width=1)

"""
edges = []
for x in (-w, w):
    for y in (-h, h):
        edges.append((x//2, y//2))

-> you'll only show a quarter of the square so you have to adjust

"""

# Start running the experimen
control.start(subject_id=1)

# Present the squares
square1.present(clear=True, update=False)
square2.present(clear=False, update=False)
square3.present(clear=False, update=False)
square4.present(clear=False, update=True)



# Leave it on-screen until a key is pressed
exp.keyboard.wait()


# End the current session and quit expyriment
control.end()