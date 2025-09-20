from expyriment import design, control, stimuli
import random, math
import numpy as np

control.set_develop_mode()

displacement_X = 400
step_size = 10
# Create an object of class Experiment: This stores the global settings of your experiment & handles the data file, screen, and input devices
exp = design.Experiment(name = "Square")

# Initialize the experiment: Must be done before presenting any stimulus
control.initialize(exp)

#random angle to get the random axis of motion
alpha = 2 * math.pi * random.random()
rotation_matrix = np.array([[math.cos(alpha), -math.sin(alpha)], 
                            [math.sin(alpha), math.cos(alpha)]])

pos = np.array([-300, 0])

new_pos = np.dot(pos, rotation_matrix)

steps = (-new_pos[0] / 40, -new_pos[1] / 40)

# Create a fixation cross (color, size, and position will take on default values)
# Create a 50px-sized squared
square_green = stimuli.Rectangle((50, 50), colour=(0, 255, 0), position=(0, 0))
square_red = stimuli.Rectangle((50, 50), colour=(255, 0, 0), position=(round(new_pos[0]), round(new_pos[1])))


# Start running the experimen
control.start(subject_id=1)

# Present the fixation cross and the square
square_red.present(clear=True, update=False)
square_green.present(clear=False, update=True)


while square_red.overlapping_with_stimulus(square_green)[0] == False : 
    square_red.move(steps) #movex, movey 
    square_red.present(clear=True, update=False)
    square_green.present(clear=False, update=True)


#absolute value because the position can become more and more negative along a random axis
while abs(square_green.position[0])+abs(square_green.position[1]) < displacement_X: 
    square_green.move(steps) #movex, movey 
    square_red.present(clear=True, update=False)
    square_green.present(clear=False, update=True)
    
# Leave it on-screen until a key is pressed
exp.keyboard.wait()

# End the current session and quit expyriment
control.end()