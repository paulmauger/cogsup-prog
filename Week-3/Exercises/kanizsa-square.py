from expyriment import design, control, stimuli, io
import expyriment.misc.geometry as geo
from expyriment.misc.constants import C_GREY
control.set_develop_mode()

# Create an object of class Experiment: This stores the global settings of your experiment & handles the data file, screen, and input devices
exp = design.Experiment(name = "Square", background_colour=C_GREY)

# Initialize the experiment: Must be done before presenting any stimulus
control.initialize(exp)
print((exp.screen.size[0]/2, exp.screen.size[1]/2))

square_size = exp.screen.size[0] / 4
circle_size = exp.screen.size[0] / 12

#create 4 squares at the corners of the screen 


square1 = stimuli.Rectangle((square_size*2, square_size*2), colour=C_GREY, position=(0,0))

pos1 = (square_size, square_size) 
pos2 = (-square_size, square_size)
pos3 = (-square_size, -square_size)
pos4 = (square_size, -square_size)

circle1 = stimuli.Circle(circle_size, colour="black", position=pos1)
circle2 = stimuli.Circle(circle_size, colour="black", position=pos2)
circle3 = stimuli.Circle(circle_size, colour="white", position=pos3)
circle4 = stimuli.Circle(circle_size, colour="white", position=pos4)


# Start running the experimen
control.start(subject_id=1)

circle1.present(clear=True, update=False)
circle2.present(clear=False, update=False)
circle3.present(clear=False, update=False)
circle4.present(clear=False, update=False)
square1.present(clear=False, update=True)


# Leave it on-screen until a key is pressed
exp.keyboard.wait()


# End the current session and quit expyriment
control.end()