from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import os


class PyqtInterface():
    def __init__(self):
        super().__init__()
        # a class that, when called, opens the experimenter UI and collects the experiment parameters
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        self.app = QApplication([])
        self.window_pyqt = uic.loadUi("assignment3UI.ui")
        # connect signals
        self.window_pyqt.NextButton.clicked.connect(self.pageOperations)
        # if on the first page (i.e. if the signal comes from the "create New Experiment" button), then move to
        # the next page without checks
        self.window_pyqt.createNewExperiment.clicked.connect(self.turnPage)
        self.window_pyqt.ContinueExperiment.clicked.connect(self.pageOperations)

        self.window_pyqt.secondDistractorCheck.stateChanged.connect(self.checkSecondDistractor)
        self.window_pyqt.secondDistractorCheck_2.stateChanged.connect(self.checkSecondDistractor)
        self.window_pyqt.ConsentCheckBox.stateChanged.connect(self.checkConsent)
        # a variable that will be retrieved in the main file to check whether all checks are passed and the experiment
        # can continue. This is needed because otherwise the experiment would just start when cancelling the UI but
        # before finishing the demographics section
        self.canContinueExperiment = False
        self.secondDistractorIsChecked = False
        self.secondDistractor_2IsChecked = False
        # hide error messages and next button
        for element in [self.window_pyqt.errormsg, self.window_pyqt.errormsg_2, self.window_pyqt.errormsg_3,
                        self.window_pyqt.errormsg_4, self.window_pyqt.NewExperimentError,
                        self.window_pyqt.NextButton]:
            element.hide()
        # disable the second distractor widgets
        for widget in [self.window_pyqt.typeDistractorStimulus2, self.window_pyqt.colorDistractorStimulus2,
                       self.window_pyqt.NumberDistractor2, self.window_pyqt.typeDistractorStimulus2_2,
                       self.window_pyqt.colorDistractorStimulus2_2, self.window_pyqt.NumberDistractor2_2]:
            widget.setEnabled(False)
        # I initialize these variables here so that they can be used in the experimentVariables function
        self.typeDistractor2 = [None, None]
        self.colorDistractor2 = [None, None]
        self.nrDistractor2 = [None, None]
        self.targetStimulus = [None, None]
        self.targetColor = [None, None]
        self.typeDistractor1 = [None, None]
        self.colorDistractor1 = [None, None]
        self.nrDistractor1 = [None, None]
        self.dynamic = [None, None]
        self.window_pyqt.show()
        self.app.exec_()

    def experimentVariables(self):
        # this function collects the experiment parameters provided by the experimenter, both for condition 1 and 2
        # and returns them as a dictionary where the keys correspond to the modular parameters and always the first
        # value corresponds to condition 1 and the second to condition 2
        # first condition information is fetched when the next button is clicked on the second page
        if self.window_pyqt.idx == 1:
            self.targetStimulus[0] = self.window_pyqt.typeTargetStimulus.currentText()
            self.targetColor[0] = self.window_pyqt.colorTargetStimulus.currentText()
            self.typeDistractor1[0] = self.window_pyqt.typeDistractorStimulus1.currentText()
            self.colorDistractor1[0] = self.window_pyqt.colorDistractorStimulus1.currentText()
            self.nrDistractor1[0] = self.window_pyqt.NumberDistractor1.value()
            self.dynamic[0] = self.window_pyqt.StimulusDynamic.currentText()
            # depending on whether the second distractor is checked, the values are either appended or None is appended
            # this is done for both conditions
            if self.secondDistractorIsChecked:
                values = (self.window_pyqt.typeDistractorStimulus2.currentText(),
                          self.window_pyqt.colorDistractorStimulus2.currentText(),
                          self.window_pyqt.NumberDistractor2.value())
            else:
                values = (None, None, None)
            self.typeDistractor2[0] = values[0]
            self.colorDistractor2[0] = values[1]
            self.nrDistractor2[0] = values[2]
        # second condition information is fetched when the next button is clicked on the second page
        elif self.window_pyqt.idx == 2:
            self.targetStimulus[1] = self.window_pyqt.typeTargetStimulus_2.currentText()
            self.targetColor[1] = self.window_pyqt.colorTargetStimulus_2.currentText()
            self.typeDistractor1[1] = self.window_pyqt.typeDistractorStimulus1_2.currentText()
            self.colorDistractor1[1] = self.window_pyqt.colorDistractorStimulus1_2.currentText()
            self.nrDistractor1[1] = self.window_pyqt.NumberDistractor1_2.value()
            self.dynamic[1] = self.window_pyqt.StimulusDynamic_2.currentText()
            # depending on whether the second distractor is checked, the values are either appended or None is appended
            if self.secondDistractor_2IsChecked:
                values = (self.window_pyqt.typeDistractorStimulus2_2.currentText(),
                          self.window_pyqt.colorDistractorStimulus2_2.currentText(),
                          self.window_pyqt.NumberDistractor2_2.value())
            else:
                values = (None, None, None)
            self.typeDistractor2[1] = values[0]
            self.colorDistractor2[1] = values[1]
            self.nrDistractor2[1] = values[2]
        trials = self.window_pyqt.trials.value()
        # will be needed in another method, hence it is assigned to self
        self.expName = self.window_pyqt.experimentName.text().replace(" ", "")
        return {"targetStim": self.targetStimulus, "targetColor": self.targetColor,
                "typeDistractor1": self.typeDistractor1, "colorDistractor1": self.colorDistractor1, "nrDistractor1": self.nrDistractor1,
                "typeDistractor2": self.typeDistractor2, "colorDistractor2": self.colorDistractor2,
                "nrDistractor2": self.nrDistractor2, "dynamic": self.dynamic, "trials": trials, "expName": self.expName}

    def checkErrors(self, expVariables):
        # this function checks for errors and missing values in the experiment variables
        # it takes the dictionary with the experiment parameters as input and returns a boolean value.
        # Crucially, this function does not make visible changes on the respective page - that is what the
        # function pageOperations is there for.
        # Furthermore, this part of the UI is split into two information sections, firstly experimental
        # parameters and secondly the participant information. The latter is checked in the
        # function checkDemographics. This is also necessitated by the fact that the experiment information does not
        # have to be provided for each participant, as one can also access existing experiments - so these two
        # functions have different use cases.
        errorMsg = ""
        if 0 < self.window_pyqt.idx < 3:
            # in both conditions, the number of stimuli for distractor 1 and 2 should be provided
            if expVariables["nrDistractor1"][self.window_pyqt.idx-1] == 0:
                # -1 because page 1 corresponds to condition 1, which has position 0 in the dictionary
                errorMsg = "Please provide a number of desired stimuli for distractor 1"
            elif expVariables["nrDistractor2"][self.window_pyqt.idx-1] == 0:
                errorMsg = "Please provide a number of desired stimuli for distractor 2"
            if self.window_pyqt.idx == 1:
                # to avoid redundancy, the error message is only assigned to label on the respective page
                self.window_pyqt.errormsg.setText(errorMsg)
            elif self.window_pyqt.idx == 2:
                self.window_pyqt.errormsg_2.setText(errorMsg)
        elif self.window_pyqt.idx == 3:
            self.folder_name = self.window_pyqt.experimentParameters["expName"]
            # check whether a number of trials was provided
            if expVariables["trials"] == 0:
                errorMsg = "Please provide a number of desired trials"
            elif os.path.exists(self.folder_name) or self.expName == "" or not self.expName.isalnum():
                # check whether the experiment name already exists, whether it is empty or whether it is alphanumeric
                # spaces were removed in the experimentVariables function, so no need to check for that here
                errorMsg = "Please choose a different name. Please only use alphanumeric characters and" \
                           " non-empty strings."
            self.window_pyqt.errormsg_3.setText(errorMsg)
        return errorMsg == ""

    def checkDemographics(self, demographics):
        # this function checks for errors and missing values in the demographics data
        # it takes the dictionary with the experiment parameters as input and returns a boolean value.
        errorMsg = ""
        if demographics["name"] == "":
            errorMsg = "Please enter your name"
        elif demographics["age"] == 0:
            errorMsg = "Please enter your age"
        elif demographics["age"] < 18:
            errorMsg = "You can only participate in this study if you are at least 18 years old"
        elif demographics["gender"] == None:
            errorMsg = "Please choose your sex"
        elif demographics["education"] == "":
            errorMsg = "Please enter your highest level of education"

        self.window_pyqt.errormsg_4.setText(errorMsg)
        return errorMsg == ""

    def pageOperations(self):
        # check current index - will be needed to move pages
        self.window_pyqt.idx = self.window_pyqt.stackedWidget.currentIndex()

        pageCanTurn = False  # initialise variable that determines whether conditions fulfilled and page can be turned

        if self.window_pyqt.idx == 0:
            self.folder_name = self.window_pyqt.ExistingExperimentName.text().replace(" ", "")
            if os.path.exists(self.folder_name):
                # if the experiment name exists, then save its file path so that the program knows where to access it.
                # Then, skip the part of the interface where the experimenter can enter the experiment parameters and
                # head directly to demographics. This section is only triggered if the experimenter clicks the
                # button "continue with this experiment!" as the button "create new experiment" triggers a different
                # function that turns page without checking for errors.
                self.filename = f"{self.folder_name}/expPar{self.folder_name}.csv"
                self.window_pyqt.stackedWidget.setCurrentIndex(4)
                self.window_pyqt.NextButton.show()
            else:
                errorMsg = "This experiment does not exist yet. You can always create a new experiment with that name" \
                           " though"
                self.window_pyqt.NewExperimentError.setText(errorMsg)
                self.window_pyqt.NewExperimentError.show()

        elif 0 < self.window_pyqt.idx < 4:
            # the pages 2-4 are checked by the same function (checkErrors) because they contain the same type
            # of information, i.e., experiment parameter information
            # call the function that collects the experiment parameters
            self.window_pyqt.experimentParameters = self.experimentVariables()
            if self.checkErrors(self.window_pyqt.experimentParameters):  # if no errors are found
                if self.window_pyqt.idx == 3:
                    # if the experimenter enters an experiment name that does not already exist,
                    # the program creates a folder corresponding to the desired experiment name and within that
                    # folder creates a csv with the experiment parameters
                    os.makedirs(self.folder_name)
                    self.filename = f"{self.folder_name}/expPar{self.folder_name}.csv"
                    writeParam = open(self.filename, "w")
                    writeParam.write(f"Condition,targetStim,targetColor,typeDistractor1,"
                                     f"colorDistractor1,nrDistractor1,typeDistractor2,colorDistractor2,"
                                     f"nrDistractor2,dynamic,trials,expName")
                    for q in range(len(self.window_pyqt.experimentParameters["targetStim"])):
                        writeParam.write(f"\n{q+1},"
                                         f"{self.window_pyqt.experimentParameters['targetStim'][q]},"
                                         f"{self.window_pyqt.experimentParameters['targetColor'][q]},"
                                         f"{self.window_pyqt.experimentParameters['typeDistractor1'][q]},"
                                         f"{self.window_pyqt.experimentParameters['colorDistractor1'][q]},"
                                         f"{self.window_pyqt.experimentParameters['nrDistractor1'][q]},"
                                         f"{self.window_pyqt.experimentParameters['typeDistractor2'][q]},"
                                         f"{self.window_pyqt.experimentParameters['colorDistractor2'][q]},"
                                         f"{self.window_pyqt.experimentParameters['nrDistractor2'][q]},"
                                         f"{self.window_pyqt.experimentParameters['dynamic'][q]},"
                                         f"{self.window_pyqt.experimentParameters['trials']},"
                                         f"{self.window_pyqt.experimentParameters['expName']}")
                    writeParam.close()
                #pageCanTurn = True
                self.window_pyqt.stackedWidget.setCurrentIndex(self.window_pyqt.idx + 1)

            else:
                # if there are errors, show the error message and do not turn,
                # as the experimenter needs to fix the errors
                error_msgs = [self.window_pyqt.errormsg, self.window_pyqt.errormsg_2, self.window_pyqt.errormsg_3]
                if self.window_pyqt.idx-1 < len(error_msgs):
                    error_msgs[self.window_pyqt.idx-1].show()

        elif self.window_pyqt.idx == 4:
            self.window_pyqt.NextButton.setEnabled(False)
            pageCanTurn = True
        elif self.window_pyqt.idx == 6:
            self.window_pyqt.participantDemographics = self.getDemographics()
            if self.checkDemographics(self.window_pyqt.participantDemographics):
                # if all the checks are passed, then move to the experiment
                self.canContinueExperiment = True  # experiment only proceeds if all checks have been passed
                self.window_pyqt.close()
            else:
                self.window_pyqt.errormsg_4.show()
        else:
            pageCanTurn = True
        if pageCanTurn:
            self.window_pyqt.stackedWidget.setCurrentIndex(self.window_pyqt.idx + 1)



    def checkSecondDistractor(self):
        # enable or disable the widgets corresponding to the second distractor
        if self.window_pyqt.secondDistractorCheck.isChecked():
            self.secondDistractorIsChecked = True
            for widget in [self.window_pyqt.typeDistractorStimulus2, self.window_pyqt.colorDistractorStimulus2,
                           self.window_pyqt.NumberDistractor2]:
                widget.setEnabled(True)
        else:
            self.secondDistractorIsChecked = False
            for widget in [self.window_pyqt.typeDistractorStimulus2, self.window_pyqt.colorDistractorStimulus2,
                           self.window_pyqt.NumberDistractor2]:
                widget.setEnabled(False)
        if self.window_pyqt.secondDistractorCheck_2.isChecked():
            self.secondDistractor_2IsChecked = True
            for widget in [self.window_pyqt.typeDistractorStimulus2_2, self.window_pyqt.colorDistractorStimulus2_2,
                           self.window_pyqt.NumberDistractor2_2]:
                widget.setEnabled(True)
        else:
            self.secondDistractor_2IsChecked = False
            for widget in [self.window_pyqt.typeDistractorStimulus2_2, self.window_pyqt.colorDistractorStimulus2_2,
                           self.window_pyqt.NumberDistractor2_2]:
                widget.setEnabled(False)

    def turnPage(self):
        self.window_pyqt.idx = self.window_pyqt.stackedWidget.currentIndex()
        self.window_pyqt.stackedWidget.setCurrentIndex(self.window_pyqt.idx + 1)
        self.window_pyqt.NextButton.show()

    def getDemographics(self):
        # this function collects the personal details of the participant
        ID = self.window_pyqt.participantID.text().strip()
        name = self.window_pyqt.NameInput.text().strip()
        age = self.window_pyqt.AgeSpin.value()
        gender = None
        for radio in self.window_pyqt.groupedSex.children():
            if radio.isChecked():
                gender = radio.text()
        education = self.window_pyqt.EducationComboBox.currentText()
        isStudent = self.window_pyqt.StudentCheckbox.isChecked()
        return {"ID": ID, "gender": gender, "name": name, "age": age, "education": education,
                "isStudent": isStudent}

    def checkConsent(self):
        # if consent is given, enable moving forward in the study by enabling the next button
        if self.window_pyqt.ConsentCheckBox.isChecked():
            self.window_pyqt.NextButton.setEnabled(True)
        else:
            self.window_pyqt.NextButton.setEnabled(False)





