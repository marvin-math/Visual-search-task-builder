import random
import stimuliclass
from psychopy import core


def create_stimuli(window, targetStim, targetColor, typeDistractor1, colorDistractor1,
                   nrDistractor1, typeDistractor2, colorDistractor2, nrDistractor2, dynamic):
    window.stim_size = 100
    window.locations = []
    window.pos = ()
    window.angles = []

    x_min, x_max = int(-window.screen_width/2), int(window.screen_width/2)
    y_min, y_max = int(-window.screen_height/2), int(window.screen_height/2)

    window.presentStimulus = random.randint(0, 1)  # random generator determining whether the target is presented or not

    if nrDistractor2 != 'None':
        # if there are two types of distractors, the total number of stimuli is the sum of the number of distractors
        nr_stimuli = int(nrDistractor1) + int(nrDistractor2)
    else:
        # if there is only one type of distractor, its number corresponds to the total number of stimuli
        nr_stimuli = int(nrDistractor1)
    if window.presentStimulus == 1:
        nr_stimuli += 1  # if the target is presented, the total number of stimuli is increased by 1
    # create unique stimulus positions.
    # A for loop is used to make sure that the desired number of stimuli is created. To achieve this, a counter is run
    # to count the number of created unique positions. The loop continues until the desired number of positions
    # is reached. The combination of for loop plus an additional counter avoids using a while loop, which is done
    # intentionally to avoid an infinite loop in case the desired number of positions cannot be reached.
    # If a given random draw is too close to a previous draw, the loop continues until a suitable position is found.
    # The alternative would be to compute all unique positions first and then randomly draw from that list
    # but this would be computationally more expensive and therefore less scalable.
    positions_counter = 0
    for i in range(10000):
        # draw random position
        window.pos = random.choice(range(x_min, x_max)), random.choice(range(y_min, y_max))
        if i == 0:  # append the first position without any checks
            window.locations.append(window.pos)
            positions_counter += 1
        else:
            # check if the position is too close to any of the previous positions
            # if it is, the loop for loop is stopped and another random draw is made
            # if it is not too close, the position is appended to the list of positions and the number of appended
            # positions is increased by 1. Only increasing after a suitable position is found makes sure that the
            # while loop continues until the desired number of positions is reached
            for b in range(len(window.locations)):
                dist_x = abs(window.pos[0] - window.locations[b][0])
                dist_y = abs(window.pos[1] - window.locations[b][1])

                if dist_x > window.stim_size or dist_y > window.stim_size:
                    # if the distance between the current position and the previous positions is larger than the
                    # stimulus size, the position is accepted. However, all previous positions have to be checked in
                    # order to make sure that the current position is not too close to any of them. Hence, the position
                    # is only appended after the loop. If any of the previous positions is too close, the loop is
                    # stopped and another random draw is made.
                    distanceIsOk = True
                else:
                    distanceIsOk = False
                    break
            if distanceIsOk:
                window.locations.append(window.pos)
                positions_counter += 1
            if positions_counter == nr_stimuli:
                # break the loop if the desired number of positions is reached
                break
            if i == 9999:
                # if the loop is run 10000 times without reaching the desired number of positions, the loop is stopped
                # and the program is stopped
                print('Could not create enough unique positions')
                print('Please change the number of stimuli or the screen size')
                core.quit()
                break



    # initialize stimuli class
    window.stimuli = stimuliclass.Stimuli(window)
    window.targetPresented = None
    # create the stimuli by calling the createFigure method of the stimuli class
    # by doing this, the created stimuli are saved in a list of the window object (see stimuliclass.py)
    # this is computationally efficient in the animation case as I don't have to create the stimuli every time
    # I want to draw them.
    for z in range(len(window.locations)):
        if dynamic == 'moving':
            angles = random.uniform(0, 360)
            window.angles.append(angles)
        if z == 0:
            # the first stimulus is always the target, but it is not always presented. The target stimulus is randomly
            # either presented or not on a given trial
            if window.presentStimulus == 1:
                window.stimuli.createFigure(targetStim, targetColor)
                window.targetPresented = 'Yes'
            else:
                # if the target is not presented, the first stimulus is a distractor
                window.stimuli.createFigure(typeDistractor1, colorDistractor1)
                window.targetPresented = 'No'

        else:
            if typeDistractor2 == 'None':
                # if there is only one type of distractor, create all distractors of that type
                window.stimuli.createFigure(typeDistractor1, colorDistractor1)
            else:
                if z < int(nrDistractor1):
                    # if there are two types of distractors, create as many distractors of type 1 as specified
                    window.stimuli.createFigure(typeDistractor1, colorDistractor1)
                elif z < nr_stimuli:
                    # the total number of distractors is the sum of both types
                    window.stimuli.createFigure(typeDistractor2, colorDistractor2)






