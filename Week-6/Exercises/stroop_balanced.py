from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK, K_r, K_b, K_g, K_o
import random
import itertools

""" Constants """
COLORS = ["red", "blue", "green", "orange"]
KEYS = [K_r, K_b, K_g, K_o]

COLOR_KEY_MAP = dict(zip(COLORS, KEYS))

N_BLOCKS = 2 
N_TRIALS_IN_BLOCK = 16


INSTR_START = """
In this task, you have to indicate the color of the font in which a word is written.

Press:
R for red
B for blue
G for green
O for orange

Press SPACE to continue.
"""

INSTR_MID = """You have finished block {block_num} of {total_blocks}. Well done!
Your task will be the same.

Take a break, then press SPACE to continue.
"""
INSTR_END = """Well done! You have completed the experiment.

Press SPACE to quit."""

FEEDBACK_INCORRECT = """X"""

""" Helper functions """
def load(stims):
    for stim in stims:
        stim.preload()

def timed_draw(*stims):
    t0 = exp.clock.time
    exp.screen.clear()
    for stim in stims:
        stim.present(clear=False, update=False)
    exp.screen.update()
    t1 = exp.clock.time
    return t1 - t0

def present_for(*stims, t=1000):
    dt = timed_draw(*stims)
    exp.clock.wait(t - dt)

def present_instructions(text):
    instructions = stimuli.TextScreen(text=text, text_justification=0, heading="Instructions")
    instructions.present()
    exp.keyboard.wait()


# Helper for obtaining derangements in python  
def derangements(lst): 
    ders = [] 
    for perm in itertools.permutations(lst): 
        if all(original != perm[idx] for idx, original in enumerate(lst)): 
            ders.append(list(perm)) 
    return ders 


""" Global settings """
exp = design.Experiment(name="Stroop Balanced", background_colour=C_WHITE, foreground_colour=C_BLACK)
exp.add_data_variable_names(['block_cnt', 'trial_cnt', 'trial_type', 'word', 'color', 'RT', 'correct'])

control.set_develop_mode()
control.initialize(exp)

""" Stimuli """
fixation = stimuli.FixCross()
fixation.preload()

stims = {w: {c: stimuli.TextLine(w, text_colour=c) for c in COLORS} for w in COLORS}
load([stims[w][c] for w in COLORS for c in COLORS])

feedback_correct = stimuli.TextLine("")
feedback_incorrect = stimuli.TextLine(FEEDBACK_INCORRECT)
load([feedback_correct, feedback_incorrect])

""" Experiment """
def run_trial(block_id, trial_id, trial_type, word, color):
    stim = stims[word][color]
    present_for(fixation, t=500)
    stim.present()
    key, rt = exp.keyboard.wait(KEYS)
    correct = key == COLOR_KEY_MAP[color]
    exp.data.add([block_id, trial_id, trial_type, word, color, rt, correct])
    feedback = feedback_correct if correct else feedback_incorrect
    present_for(feedback, t=1000)


COLORS = ["red", "blue", "green", "orange"] 
PERMS = derangements(COLORS) # The 9 derangements 

subject_id = 1 #MODIFY FOR EACH SUBJECT

order = (subject_id - 1) # modulo arithmetic 
perm = PERMS[order] # Choose based on subject ID 
# A list of dictionaries for the trials 
trials = ( 
  [{"trial_type": "match", "word": c, "color": c} for c in COLORS] + 
  [{"trial_type": "mismatch", "word": w, "color": c} for w, c in zip(COLORS, perm)]
)


# Create 32 trials, divided in 2 blocks, in a nested list 
block_repetitions = N_TRIALS_IN_BLOCK // len(trials) 
blocks = [] 
for b in range(1, N_BLOCKS + 1): 
    b_trials = trials * block_repetitions # 16 trials 
    random.shuffle(b_trials) 
    block_trials = [{"block_id": b, "trial_id": i, **t} for i, t in enumerate(b_trials, 1)] 
    blocks.append(block_trials) # len(blocks) = 2; len(trials) = 16


""" Experiment """ 
control.start(subject_id=subject_id)
present_instructions(INSTR_START) 
for block_id, block in enumerate(blocks, 1): 
    for trial in block: 
        run_trial(**trial) 
    if block_id != N_BLOCKS: 
        present_instructions(INSTR_MID.format(block_num=block_id, total_blocks=N_BLOCKS)) 
present_instructions(INSTR_END) 
control.end()