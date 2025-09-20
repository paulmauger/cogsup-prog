from expyriment import design, control, stimuli
from expyriment.misc import geometry

control.set_develop_mode()

displacement_X = 400
step_size = 10
# Create an object of class Experiment: This stores the global settings of your experiment & handles the data file, screen, and input devices
exp = design.Experiment(name = "Square")

# Initialize the experiment: Must be done before presenting any stimulus
control.initialize(exp)

# Create a fixation cross (color, size, and position will take on default values)
# Create a 50px-sized squared
triangle = stimuli.Shape(position=(-100, 0), colour=(128,0,128), vertex_list=geometry.vertices_triangle(60., 50., 50.))

hexagon = stimuli.Shape(position=(100, 0), colour=(255, 255, 0), vertex_list=geometry.vertices_regular_polygon(6, 28.87))


# Start running the experimen
control.start(subject_id=1)

# Present the fixation cross and the square
hexagon.present(clear=True, update=False)
triangle.present(clear=False, update=True)

# Leave it on-screen until a key is pressed
exp.keyboard.wait()

# End the current session and quit expyriment
control.end()