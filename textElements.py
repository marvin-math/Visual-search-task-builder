from psychopy import visual

def create_text_elements(window):
    # instructions text
    instructions_message = f"This is a visual search task. You will see {window.setup['dynamic'][window.condition]}" \
    f" stimuli \nand your goal is to identify whether a target stimulus is present or not.\n The target stimulus is a" \
    f" {window.setup['targetStim'][window.condition]} and is colored {window.setup['targetColor'][window.condition]}.\n" \
    f"There are {window.setup['trials'][window.condition]} trials that will be presented in succession.\n" \
    f"Please make as accurate and as fast as possible decisions, prioritising accuracy over speed.\n" \
    f"You can respond by pressing the 'y' key if the target stimulus is present and the 'n' key if it is not.\n" \
    f" The next trial will start after you pressed one of these keys, or after 3 seconds.\n" \
    f"Press any key to continue and start with the experiment"
    window.instructions_txt = visual.TextStim(window, text=instructions_message, height=30, pos=[0, 0])
    # fixation cross
    window.fixation = visual.TextStim(window, text='+', height=20, alignText='center')
