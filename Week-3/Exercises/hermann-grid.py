from expyriment import design, control, stimuli

NUM_ROWS = 8
NUM_COLS = 12

SQUARE_SIZE = 50
SPACING = 10


control.defaults.background_colour = 'white'
control.defaults.foreground_colour = 'black'

control.set_develop_mode()

exp = design.Experiment(name="Hermann")
control.initialize(exp)


canvas = stimuli.Canvas(size= (exp.screen.size[0], exp.screen.size[1]), colour='white')


for row in range(NUM_ROWS):
    for col in range(NUM_COLS):
        top_left_x = SPACING + col * (SQUARE_SIZE + SPACING)
        top_left_y = SPACING + row * (SQUARE_SIZE + SPACING)

        x_pos = (top_left_x + SQUARE_SIZE / 2) - exp.screen.size[0] / 2
        y_pos = -(top_left_y + SQUARE_SIZE / 2) + exp.screen.size[1] / 2

        square = stimuli.Rectangle(size=(SQUARE_SIZE, SQUARE_SIZE), position=(x_pos, y_pos), colour='black'
        )
        square.plot(canvas)

control.start()
canvas.present()  
exp.keyboard.wait()  
control.end()


