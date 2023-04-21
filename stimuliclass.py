from psychopy import visual
import math


class Stimuli:
    def __init__(self, window):
        self.window = window
        # initialise list to save created stimuli in.
        window.StimuliList = []

    def createFigure(self, figure, color):
        # method to create the different stimuli
        if figure == 'Circle':
            # create circle
            self.window.StimuliList.append(visual.Circle(self.window, units='pix', radius=self.window.stim_size/2,
                                                       edges=100, fillColor=color, lineColor=color))
        elif figure == 'Triangle':
            # create triangle
            vertices = ((-self.window.stim_size / 2, 0), (0, self.window.stim_size), (self.window.stim_size / 2, 0))
            self.window.StimuliList.append(visual.ShapeStim(self.window, vertices=vertices,
                                                            fillColor=color, lineColor=color))
        else:
            # create square
            self.window.StimuliList.append(visual.Rect(self.window, units='pix', width=self.window.stim_size,
                                                     height=self.window.stim_size, fillColor=color,
                                                     lineColor=color))

    def animation(self, window, stimuli, speed=20):
        self.window = window
        self.speed = speed
        self.stimuli = stimuli

        for frame in range(120):  # this is frame based animation, and it assumes you have a 60Hz monitor
            window.keypress = window.kb.getKeys(['y', 'n'], clear=True)
            # break out of loop when yes or no key is pressed and save key information in window.keypress
            if window.keypress:
                for key in window.keypress:
                    # because after keypress, the animation ends, window.keypress only saves one key. However,
                    # it is recommended by psychopy to use a for loop to get the keypress information.
                    window.key_info["key"] = key.name
                    window.key_info["rt"] = key.rt
                break
            for c in range(len(self.stimuli)):
                dir_x = math.cos(window.angles[c])
                dir_y = math.sin(window.angles[c])
                self.stimuli[c].pos += (dir_x * self.speed, dir_y * self.speed)
                self.stimuli[c].draw()
            window.flip()








