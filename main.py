import pyglet
import pyqtclass
from experiment import *
import csv
from textElements import *

pyqt = pyqtclass.PyqtInterface()  # this calls the pyqt interface. It is opened and closed with this one line
# experiment only proceeds if all checks have been passed - so if demographics or experiment parameters are skipped,
# the experiment will not start
if pyqt.canContinueExperiment:
    # create window
    win = visual.Window(fullscr=True, units='pix')

    # demographics data from the pyqt interface
    win.demographics = pyqt.getDemographics()
    # read in the experiment setup as specified in the respective csv file
    win.folder_name = pyqt.folder_name
    file = open(pyqt.filename, 'r')
    content = csv.reader(file)
    column_names = next(content)  # get the first line
    win.setup = {name: [] for name in column_names}  # create a dictionary with the column names as keys
    for line in content:  # iterate over the remaining lines
        for key, value in zip(column_names, line):  # iterate over the column names and the values in the line
            win.setup[key].append(value)  # append the value to the list of values for the key
    file.close()
    # the win.size function gave different results than what psychopy worked with in the background, so I used pyglet
    # to get the screen size as this is what psychopy uses
    display = pyglet.canvas.get_display()
    screen = display.get_default_screen()
    win.screen_width, win.screen_height = screen.width, screen.height
    win.condition = assignCondition(win)  # checks if this is the first participant and assigns condition
    create_text_elements(win)
    # this runs the experiment loop. The function to create the stimuli and animate them is called inside this function
    run_experiment(win, dynamic=win.setup["dynamic"][win.condition], trials=win.setup["trials"][win.condition])

    win.close()
    quit()


