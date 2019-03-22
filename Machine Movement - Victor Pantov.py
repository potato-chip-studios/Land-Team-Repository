GPIO17 = False
GPIO18 = False
GPIO22 = False
GPIO23 = False

def fullStop():
  GPIO17 = False
  GPIO18 = False
  GPIO22 = False
  GPIO23 = False
  #print("Not moving, boss :( \n")


def Move(direction):
  if (direction == 1): #fwd
    GPIO17 = True
    GPIO18 = True
    #print("Going forward, vroom vroom \n")
  elif (direction == 2): #bwd
    GPIO22 = True
    GPIO23 = True
    #print("Going backward, vroom vroom \n")
  elif (direction == 3): #right
    GPIO17 = True
    GPIO22 = True
    #print("Going right, vroom vroom \n")
  else:
    GPIO18 = True
    GPIO23 = True
    #print("Going left, vroom vroom \n")

def Stop(prevDir):
  if (prevDir == 1):
    GPIO17 = False
    GPIO18 = False
  elif (prevDir == 2):
    GPIO22 = False
    GPIO23 = False
  elif (prevDir == 3):
    GPIO17 = False
    GPIO22 = False
  elif(prevDir == 0): # no movement
    return
  else:
    GPIO18 = False
    GPIO23 = False

def MachineMovement(pseudoInput, previousDir): #replace pseudoInput with output from machine vision
  if (pseudoInput == 1): #fwd
    if (previousDir == pseudoInput):
      Move(previousDir)
      return previousDir
    else:
      Stop(previousDir)
      previousDir = 1
      Move(previousDir)
      return previousDir
  elif (pseudoInput == 2): #bwd
    if (previousDir == pseudoInput):
      Move(previousDir)
      return previousDir
    else:
      Stop(previousDir)
      previousDir = 2
      Move(previousDir)
      return previousDir
  elif (pseudoInput == 3): #right
    if (previousDir == pseudoInput):
      Move(previousDir)
      return previousDir
    else:
      Stop(previousDir)
      previousDir = 3
      Move(previousDir)
      return previousDir
  elif (pseudoInput == 4): #left
    if (previousDir == pseudoInput):
      Move(previousDir)
      return previousDir
    else:
      Stop(previousDir)
      previousDir = 4
      Move(previousDir)
      return previousDir
  else: #stopperino
    fullStop()
    #print(previousDir) #debugging if I have my doubts
    return previousDir

#################
# 1 - forward   #
# 2 - backward  #
# 3 - right     #
# 4 - left      #
# 5 - full stop #
#################

dirBuffer = MachineMovement(3, 0)
dirBuffer = MachineMovement(4, dirBuffer)
dirBuffer = MachineMovement(3, dirBuffer)
dirBuffer = MachineMovement(1, dirBuffer)
dirBuffer = MachineMovement(0, dirBuffer)

#Code written by: Victor Pantov 24/02/2019