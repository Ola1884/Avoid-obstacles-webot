"""my_controllerTry controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot,DistanceSensor,Motor

#time in [ms] in simulation step
TIME_STEP = 64
MAX_SPEED = 6.28

# create the Robot instance.
robot = Robot()

#initia[lize devices
ps = []
psNames = [
     'left sensor','right sensor'
]

for i in range(2):
   ps.append(robot.getDevice(psNames[i]))
   ps[i].enable(TIME_STEP)

leftBMotor= robot.getDevice('left_backward motor')
leftFMotor= robot.getDevice('left_forward motor')

rightBMotor= robot.getDevice('right_backward motor')
rightFMotor= robot.getDevice('right_forward motor')

for motor in [leftBMotor,leftFMotor,rightBMotor,rightFMotor]:
  motor.setPosition(float('inf'))
  motor.setVelocity(0.0)


#feedback loop:step simulation until seeing an exit
while robot.step(TIME_STEP) != 1:
    #read sensors output
    psValues= []
    for i in range(2):
       psValues.append(ps[i].getValue())
       
    #detect obstacles
    left_obstacle= psValues[0] < 1000.0 
    right_obstacle= psValues[1] < 1000.0 
    
    #initialize speed with 50% max speed
    leftSpeed = 0.5 * MAX_SPEED
    rightSpeed = 0.5 * MAX_SPEED
    #modify speed according to obstacles
    if left_obstacle:
      #turn right
      leftSpeed = 0.5 * MAX_SPEED
      rightSpeed = -0.5 * MAX_SPEED
    elif right_obstacle:
      #turn left
      leftSpeed = -0.5 * MAX_SPEED
      rightSpeed = 0.5 * MAX_SPEED
    
    #write acutators inputs
    leftBMotor.setVelocity(leftSpeed)
    leftFMotor.setVelocity(leftSpeed)
    rightBMotor.setVelocity(rightSpeed)
    rightFMotor.setVelocity(rightSpeed)