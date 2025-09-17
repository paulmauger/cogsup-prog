from expyriment import design, control, stimuli

control.set_develop_mode()

displacement_X = 400
step_size = 10
# Create an object of class Experiment: This stores the global settings of your experiment & handles the data file, screen, and input devices
exp = design.Experiment(name = "Square")

# Initialize the experiment: Must be done before presenting any stimulus
control.initialize(exp)

# Create a fixation cross (color, size, and position will take on default values)
# Create a 50px-sized squared
square_green = stimuli.Rectangle((50, 50), colour=(0, 255, 0), position=(0, 0))
square_red = stimuli.Rectangle((50, 50), colour=(255, 0, 0), position=(-400, 0))


# Start running the experimen
control.start(subject_id=1)

# Present the fixation cross and the square
square_red.present(clear=True, update=False)
square_green.present(clear=False, update=True)


while square_red.position[0] - square_green.position[0] < 50: 
    square_red.move((step_size, 0)) #movex, movey 
    square_red.present(clear=True, update=False)
    square_green.present(clear=False, update=True)


while square_green.position[0] < displacement_X: 
    square_green.move((step_size, 0)) #movex, movey 
    square_red.present(clear=True, update=False)
    square_green.present(clear=False, update=True)
    
# Leave it on-screen until a key is pressed
exp.keyboard.wait()

# End the current session and quit expyriment
control.end()