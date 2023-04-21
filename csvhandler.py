from random import randint
import os
import csv

def assignCondition(window):
    # This function assigns the condition of the participant. If this is the first participant (i.e. there is no csv
    # file with participant data in it), then a csv is created with headlines and the condition is assigned randomly.
    # If this is not the first participant (i.e. the csv file with the participant data already exists), this function
    # reads that csv, identifies unique participants and their conditions and assigns the condition that was not
    # assigned to the last participant. There are only two conditions in this experiment.
    # If a participant has already participated (and maybe the experiment was interrupted), the participant will be
    # assigned their previous condition. Participants are identified based on their ID number.

    filename = "participant_info.csv"
    window.file_path = os.path.join(window.folder_name, filename)
    if not os.path.isfile(window.file_path):
        assignedCondition = randint(0, 1)
        firstline = open(window.file_path, "w")
        firstline.write(f"ID,trial,condition,targetStim,targetColor,typeDistractor1,colorDistractor1,nrDistractor1,"
                        f"typeDistractor2,colorDistractor2,nrDistractor2,dynamic,expName,gender,name,age,education,"
                        f"isStudent,rt,response,correctResponse\n")
        firstline.close()

    else:
        open_file = open(window.file_path, "r")
        participantData = list(csv.DictReader(open_file, delimiter=','))
        open_file.close()
        ID, Condition = [], []
        for row in participantData:
            # identify unique participant ID's
            if row['ID'] not in ID:
                ID.append(row['ID'])
                # and their condition
                Condition.append(int(row['condition']))
        if window.demographics['ID'] not in ID:
            if Condition[-1] == 1:
                # don't confuse index and condition number. This if statement checks for condition 1, and assigns index
                # 1 if condition was one, as index 1 corresponds to condition 2 in the respective list
                assignedCondition = 1
            else:
                assignedCondition = 0
        else:
            # if this participant has already been in the experiment, get the condition she was assigned to and continue
            # with that condition
            idx = ID.index(window.demographics['ID'])
            assignedCondition = Condition[idx]-1
    return assignedCondition

def appendtocsv(window):
    participantCompleteInfo = open(window.file_path, "a")
    participantCompleteInfo.write(f"{window.demographics['ID']},"
                                  f"{window.trialcounter},"
                                  f"{window.condition+1},"
                                  f"{window.setup['targetStim'][window.condition]},"
                                  f"{window.setup['targetColor'][window.condition]},"
                                  f"{window.setup['typeDistractor1'][window.condition]},"
                                  f"{window.setup['colorDistractor1'][window.condition]},"
                                  f"{window.setup['nrDistractor1'][window.condition]},"
                                  f"{window.setup['typeDistractor2'][window.condition]},"
                                  f"{window.setup['colorDistractor2'][window.condition]},"
                                  f"{window.setup['nrDistractor2'][window.condition]},"
                                  f"{window.setup['dynamic'][window.condition]},"
                                  f"{window.setup['expName'][window.condition]},"
                                  f"{window.demographics['gender']},"
                                  f"{window.demographics['name']},"
                                  f"{window.demographics['age']},"
                                  f"{window.demographics['education']},"
                                  f"{window.demographics['isStudent']},"
                                  f"{window.key_info['rt']},"
                                  f"{window.key_info['key']},"
                                  f"{window.targetPresented}\n")
    participantCompleteInfo.close()