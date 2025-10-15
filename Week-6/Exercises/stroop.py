from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK, K_j, K_f
import random
import itertools

""" Constants """
KEYS = [K_j, K_f]
TRIAL_TYPES = ["match", "mismatch"]

N_BLOCKS = 2
N_TRIALS_IN_BLOCK = 16

# Helper for obtaining derangements in python  
def derangements(lst): 
    ders = [] 
    for perm in itertools.permutations(lst): 
        if all(original != perm[idx] for idx, original in enumerate(lst)): 
            ders.append(lst) 
    return ders 


COLORS = ["red", "blue", "green", "orange"] 
PERMS = derangements(COLORS) # The 9 derangements 

print(PERMS)
# A list of dictionaries for the trials 
trials = ( 
  [{"trial_type": "match", "word": c, "color": c} for c in COLORS] + 
  [{"trial_type": "mismatch", "word": w, "color": c} for w,c in zip(COLORS, PERMS[0])] 
)

INSTR_START = """
In this task, you have to indicate whether the meaning of a word and the color of its font match.
Press J if they do, F if they don't.\n
Press SPACE to continue.
"""
INSTR_MID = """You have finished half of the experiment, well done! Your task will be the same.\nTake a break then press SPACE to move on to the second half."""
INSTR_END = """Well done!\nPress SPACE to quit the experiment."""

FEEDBACK_CORRECT = """O"""
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

""" Global settings """
exp = design.Experiment(name="Stroop", background_colour=C_WHITE, foreground_colour=C_BLACK)
exp.add_data_variable_names(['block_cnt', 'trial_cnt', 'trial_type', 'word', 'color', 'RT', 'correct'])

control.set_develop_mode()
control.initialize(exp)

""" Stimuli """
fixation = stimuli.FixCross()
fixation.preload()

stims = stims = {w: {c: stimuli.TextLine(w, text_colour=c) for c in COLORS} for w in COLORS}
load([stims[w][c] for w in COLORS for c in COLORS])

feedback_correct = stimuli.TextLine(FEEDBACK_CORRECT)
feedback_incorrect = stimuli.TextLine(FEEDBACK_INCORRECT)
load([feedback_correct, feedback_incorrect])

""" Experiment """
def run_trial(block_id, trial_id, trial_type, word, color):
    stim = stims[word][color]
    present_for(fixation, t=500)
    stim.present()
    key, rt = exp.keyboard.wait(KEYS)
    correct = key == K_j if trial_type == "match" else key == K_f
    exp.data.add([block_id, trial_id, trial_type, word, color, rt, correct])
    feedback = feedback_correct if correct else feedback_incorrect
    present_for(feedback, t=1000)

control.start(subject_id=1)

present_instructions(INSTR_START)
for block_id in range(1, N_BLOCKS + 1):
    for trial_id in range(1, N_TRIALS_IN_BLOCK + 1):
        trial_type = random.choice(TRIAL_TYPES)
        word = random.choice(COLORS)
        if trial_type == "match":
            color = word
        else:
            colors_wrong = [col for col in COLORS if col != word]
            color = random.choice(colors_wrong)

        run_trial(block_id, trial_id, trial_type, word, color)
    if block_id != N_BLOCKS:
        present_instructions(INSTR_MID)
present_instructions(INSTR_END)

control.end()