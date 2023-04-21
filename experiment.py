from psychopy.hardware import keyboard
from createstimuli import *
from csvhandler import *


def run_experiment(window, dynamic, trials):

    window.trialcounter = 0
    window.kb = keyboard.Keyboard()
    window.key_info = {}
    window.mouseVisible = False  # hide mouse cursor
    window.instructions_txt.draw()
    window.flip()
    key = window.kb.waitKeys()  # only returns a value when a key is pressed

    # if list of pressed keys is not empty, continue
    if key:
    # initiate trial loop
        for trial in range(int(trials)):
            window.kb.clearEvents()  # clear keyboard events
            window.trialcounter += 1
            # for each trial, create the stimuli and their positions. Target stimulus is shown or not randomly.
            create_stimuli(window, targetStim=window.setup["targetStim"][window.condition],
                           targetColor=window.setup["targetColor"][window.condition],
                           typeDistractor1=window.setup["typeDistractor1"][window.condition],
                           colorDistractor1=window.setup["colorDistractor1"][window.condition],
                           nrDistractor1=window.setup["nrDistractor1"][window.condition],
                           typeDistractor2=window.setup["typeDistractor2"][window.condition],
                           colorDistractor2=window.setup["colorDistractor2"][window.condition],
                           nrDistractor2=window.setup["nrDistractor2"][window.condition],
                           dynamic=window.setup["dynamic"][window.condition])

            window.fixation.draw()  # draw fixation cross
            window.flip()
            core.wait(1)

            # draw different instantiations of the stimuli. Note that I don't create new stimuli here, but by accessing
            # the lists in the window object, I use the ones that were created in the createFigure function
            for i in range(len(window.locations)):
                # loop through the list of positions and draw the stimuli at the respective positions
                # the length of the list of positions depends on the desired number of stimuli and hence I don't need
                # to add this information here
                window.StimuliList[i].pos = window.locations[i]
                window.StimuliList[i].draw()
            window.kb.clock.reset()  # reset timer
            window.flip()

            if dynamic == 'moving':
                # note that the timer is retrieved in the animation function that is called here
                # the animation is stopped when the participant presses 'y' or 'n'
                window.stimuli.animation(window, window.StimuliList, speed=30)
                # clear screen after animation
                window.flip()
            if dynamic == 'static' or len(window.keypress) == 0:
                # after showing static stimuli or if no key was pressed during animation,
                # wait for a keypress to continue. Maximally wait 3 seconds though. Here I exploit the functioning of
                # Python that if the first condition of a disjunction is satisfied, it does not continue to read the
                # second condition (this would otherwise throw an error in case of dynamic == 'static',
                # since window.keypress does not exist yet).
                window.keypress = window.kb.waitKeys(maxWait=3, keyList=['y', 'n'], clear=True)
                if window.keypress is not None:  # if keypress is not empty
                    for key in window.keypress:
                        # it is recommended by psychopy to use a for loop to get the keypress information.
                        window.key_info["key"] = key.name
                        window.key_info["rt"] = key.rt

                else:
                    window.key_info["key"] = 'None'
                    window.key_info["rt"] = 'None'
            # after every trial, append to the csv file. This might be more computationally expensive than collecting
            # all the data in one dictionary and then appending once per participant, but it is  more secure as
            # experiments can be aborted or interrupted and the present implementation makes sure that there is minimal
            # data loss. Note that an interrupted experiment session can be resumed with this program by entering
            # the experiment name and participant ID again (see assignCondition function).
            appendtocsv(window)




