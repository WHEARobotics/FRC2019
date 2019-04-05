#!/usr/bin/env python3
"""
    WHEA Robotics 3881 code for FRC 2019.
"""

import wpilib
import ctre
import wpilib.drive
import math



class MyRobot(wpilib.TimedRobot):
    
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """

        """
        Button Map for Dual Joysticks
        
        (Cargo) Intake Right Joystick:
            #User Control Buttons
        1. L & R Gatherer in
        2. Piston
        POV 0: Wrist Up
        POV 180: Wrist Down

            #Automated Buttons
        11. Cargo Ground [6]
        14. Cargo Rocket Low [4]
        15. Cargo C.S. (Cargo Ship Chute) [2]
        16. Cargo Rocket Medium [1]

        (Hatch Panel) Outtake Left Joystick:
            #User Control Buttons
        1. L & R Gatherer out
        2. Piston
        POV 0: Wrist Up
        POV 180: Wrist Down

            #Automated Buttons
        14. Multi-Low (Rocket Hatch Port, Cargo Ship Hatch Port, Transfer Station) [5]
        15. Hatch Panel Rocket Medium [3]
        16. Starting Configuration (For End Game Climb) [0]
        
        """
    
        #Setup for the 4 motor drivetrain with encoders
        self.r_motorFront = ctre.wpi_talonsrx.WPI_TalonSRX(0)
        self.r_motorFront.setInverted(True)

        self.r_motorBack = ctre.wpi_talonsrx.WPI_TalonSRX(1)
        self.r_motorBack.setInverted(True)

        self.l_motorFront = ctre.wpi_talonsrx.WPI_TalonSRX(2)
        self.l_motorFront.setInverted(True)
        
        self.l_motorBack = ctre.wpi_talonsrx.WPI_TalonSRX(3)
        self.l_motorBack.setInverted(True)

        self.l_motorFront.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast) 
        self.l_motorBack.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)

        self.r_motorFront.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast) 
        self.r_motorBack.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)

        self.l_motorFront.setQuadraturePosition(0, 0)
        self.r_motorFront.setQuadraturePosition(0, 0)

        #Setup for the elbow and wrist joints with encoders
        self.elbow = ctre.wpi_talonsrx.WPI_TalonSRX(4)
        self.elbow.setInverted(True)
        
        self.wrist = ctre.wpi_talonsrx.WPI_TalonSRX(5)
        self.wrist.setInverted(True)

        self.elbow.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Brake)
        self.wrist.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Brake)

        self.elbow.setQuadraturePosition(0, 0)
        self.wrist.setQuadraturePosition(0, 0)
        
        #Setup for the gatherers
        self.l_gatherer = ctre.wpi_victorspx.WPI_VictorSPX(6)
        self.l_gatherer.setInverted(False)
        
        self.r_gatherer = ctre.wpi_victorspx.WPI_VictorSPX(7)
        self.r_gatherer.setInverted(True)

        self.l_gatherer.setNeutralMode(ctre.wpi_victorspx.WPI_VictorSPX.NeutralMode.Brake)
        self.r_gatherer.setNeutralMode(ctre.wpi_victorspx.WPI_VictorSPX.NeutralMode.Brake)

        #Setup for pneumatics
        self.piston0 = wpilib.Solenoid(1 , 0)
        self.piston1 = wpilib.Solenoid(1 , 1)
        
        #Setup for drive groups and joysticks             
        self.l_joy = wpilib.Joystick(0)
        self.r_joy = wpilib.Joystick(1)
        
        self.left = wpilib.SpeedControllerGroup(self.l_motorFront, self.l_motorBack)
        self.right = wpilib.SpeedControllerGroup(self.r_motorFront, self.r_motorBack)
        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)

        #Camera setup and extras
        self.counter = 0
        wpilib.CameraServer.launch('vision.py:main')
##        IP for camera server1: http://10.38.81.101:1181/
##        IP for camera server2: http://10.38.81.101:1182/
##        self.dashboard = wpilib.SmartDashboard()

        #Angle number for set position
##        [0] = Starting Config (8L)
##        [1] = Cargo Rocket Med (9R)                              
##        [2] = Cargo C.S. (8R)                            
##        [3] = Hatch Panel Rocket Med (7L)                  
##        [4] = Cargo Rocket Low (7R)              
##        [5] = Multi-Low (6L)  
##        [6] = Cargo Ground (6R)
        
        #Setup for arm positions/arm angles
        self.elbow_angles = [0 , 54.4 , 73 , 100.8 , 155.7 , 177.4 , 205]              
        self.wrist_angles = [0 , -100 , -55.7 , -64.3 , -5.9 , 15.3 , -24]              
        self.target_arm_position = 0
        self.desired_wrist_angle = 0 #Wrist position control
        self.arm_state = 0
        self.arm_manual = True #For switching between manual and automated modes
        self.elbow_torque = 0
        self.torque_setting = 0.025 #Elbow torque control
        self.elbow.set(0)
        self.int_elbow_angle = 0  # Initial (starting) angle between chungus and the arm.
        self.int_wrist_angle = 0 # Initial angle of arm with respect to vertical.
        
        #List of possible preset angles
##        teleop elbow angles = [0 , 10 , 45 , 90 , 150]
##        teleop wrist angles = [0 , 10 , 30 , 60 , 90]

        #Setup for optical sensors
##        red = right
##        blue = middle
##        yellow = left
        self.indecator_red = wpilib.Solenoid(1 , 2)
        self.indecator_blue = wpilib.Solenoid(1 , 4)
        self.indecator_yellow = wpilib.Solenoid(1 , 3)
        self.sensor_right = wpilib.DigitalInput(0)
        self.sensor_middle = wpilib.DigitalInput(1)
        self.sensor_left = wpilib.DigitalInput(2)
        

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        pass
    
    
    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        self.teleop_control()
    

    def teleopInit(self):
        """This function is run once each time the robot enters teleoperated mode."""
        pass
        

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.teleop_control()


    #Set target state and mode based on button press
    def check_buttons(self):
        if self.l_joy.getRawButton(14): #Multi-Low Left Joystick
            self.select_states()
            self.arm_manual = False
            self.target_arm_position = 5

        elif self.l_joy.getRawButton(15): #Hatch Panel Rocket Medium Left Joystick
            self.select_states()
            self.arm_manual = False
            self.target_arm_position = 3
            
        elif self.l_joy.getRawButton(16): #Starting Concfiguration Left Joystick
            self.select_states()
            self.arm_manual = False
            self.target_arm_position = 0

        elif self.r_joy.getRawButton(11): #Cargo Ground Right Joystick
            self.select_states()
            self.arm_manual = False
            self.target_arm_position = 6

        elif self.r_joy.getRawButton(14): #Cargo Rocket Low Right Joystick
            self.select_states()
            self.arm_manual = False
            self.target_arm_position = 4

        elif self.r_joy.getRawButton(15): #Cargo C.S. (Cargo Ship) Right Joystick
            self.select_states()
            self.arm_manual = False
            self.target_arm_position = 2

        elif self.r_joy.getRawButton(16): #Cargo Rocket Medium Right Joystick
            self.select_states()
            self.arm_manual = False
            self.target_arm_position = 1

        elif self.l_joy.getRawButton(11) or self.l_joy.getRawButton(12) or self.l_joy.getRawButton(13) or self.r_joy.getRawButton(12) or self.r_joy.getRawButton(13):
            self.select_states()
            self.arm_manual = False
            
        #Wrist Down and Wrist up Right Joystick:

        if self.r_joy.getPOV() == 180:
            self.arm_manual = True
            self.wrist.set(-0.2)
            
        elif self.r_joy.getPOV() == 0:
            self.arm_manual = True
            self.wrist.set(0.2)

        else:
            if self.arm_manual == True:
                self.wrist.set(0)

        #Elbow Down and Elbow up Left Joystick:

        if self.l_joy.getPOV() == 180:
            self.arm_manual = True
            self.elbow_torque -= self.torque_setting #Changes elbow movement based on torque setting 
            if self.elbow_torque < -1.0:
                self.elbow_torque = -1.0
                
        elif self.l_joy.getPOV() == 0:
            self.arm_manual = True
            self.elbow_torque += self.torque_setting
            if self.elbow_torque > 1.0:
                self.elbow_torque = 1.0

        else:
            if self.arm_manual == True:
                if self.elbow_torque > self.torque_setting:
                    self.elbow_torque -= self.torque_setting
                    
                elif self.elbow_torque < -self.torque_setting:
                    self.elbow_torque += self.torque_setting

                else:
                    self.elbow_torque = 0

        self.elbow.set(self.elbow_torque)

                
        #Position control loop for wrist
##        max_angle = self.arm_limit_check()
##
##        if self.r_joy.getPOV() == 180:
##            self.arm_manual = True
##            self.desired_wrist_angle -= 10
##            
##        elif self.r_joy.getPOV() == 0:
##            self.arm_manual = True
##            self.desired_wrist_angle += 10
##
##        if self.desired_wrist_angle > max_angle:
##            self.desired_wrist_angle = max_angle
##
##        arm_error = self.elbow_angle - self.desired_elbow_angle
##        constant = 0
##        wrist_torque = constant * elbow_error
##
##        if wrist_torque > 1.0:
##            wrist_torque = 1.0
##
##        elif wrist_torque < - 1.0:
##            wrist_torque = -1.0
##
##        self.wrist.set(wrist_torque)
            
            
    #Selects state 1 or 4 based on starting arm position
    def select_states(self):
        if self.target_arm_position == 0:
            self.arm_state = 4

        else:
            self.arm_state = 1
            

    #Set state and move arm based on delta arm angles        
    def arm_move(self):
        delta_wrist_angle = self.wrist_angles[self.target_arm_position] - self.wrist_angle 
        delta_elbow_angle = self.elbow_angles[self.target_arm_position] - self.elbow_angle

        if self.arm_manual == False:
            
            #Check for state transitions
            if self.arm_state == 0:
                pass # A change out of state 0 only happens when a button is pressed, inside check_buttons().

            elif self.arm_state == 1:
                if self.wrist_angle <= 0.0:
                    self.arm_state = 2 # To the next state.  Also, no need for an "else" because if the test is false, we just stay in state 1.

            elif self.arm_state == 2:
                if self.elbow.get() > 0.0:
                    if delta_elbow_angle <= 0.0:
                        self.arm_state = 3  # Target angle reached, go to next state.

                elif self.elbow.get() < 0.0: # Negative is counterclockwise.
                    if delta_elbow_angle >= 0.0:
                        self.arm_state = 3 
           
                else:
                    self.arm_state = 0 # Extraordinary case
                    
            elif self.arm_state == 3:
                if delta_wrist_angle >= 0:
                    self.arm_state = 0 # The state 3 case.

            elif self.arm_state == 4:
                if self.wrist_angle <= 0:
                    self.arm_state = 2
                
            else:
                self.arm_state = 0 # In case arm_state ever is set outside the range 0..3, reset it to zero (stopped).

            #Move arm based on state 
            if self.arm_state == 0:
                self.wrist.set(0)
                self.elbow.set(0)

            elif self.arm_state == 1:
                self.wrist.set(1)
                self.elbow.set(0)

            elif self.arm_state == 2:
                self.wrist.set(0)
                if delta_elbow_angle > 0:
                    self.elbow.set(1)
                else:
                    self.elbow.set(-1)

            elif self.arm_state == 3:
                self.elbow.set(0)
                self.wrist.set(-1)

            else:
                self.elbow.set(1)
                if self.elbow_angle > 20 and self.elbow_angle <= 45:
                    self.wrist.set(1)
                    
                elif (self.elbow_angle > 45 and self.elbow_angle <= 60) or self.wrist_angle > 30:
                    self.wrist.set(0)

                elif self.elbow_angle > 60:
                    self.wrist.set(-1)

                    
    def arm_limit_check(self):
        """
        Function to calculate the maximum wrist angle to keep the end efffector within 30 inches of the frame.
        Uses self.elbow_angle, the current angle of the arm, so make sure that you have measured it
        before calling this function.
        """
        length_arm = 15  # Length of arm between pivot points of elbow and wrist.
        length_chungus = 15 # Length of chungus from wrist pivot to far end.
        #delta_arm_angle = (delta_elbow_angle - delta_wrist_angle)
        d = 2.5 # distance of wrist pivot from robot frame.

        elbow_reach = length_arm * math.sin(math.radians(arm_angle_from_vertical))  # Horizontal distance from elbow pivot to wrist pivot.
         
        wrist_max_angle = math.degrees(math.asin((30 + d - elbow_reach) / length_chungus)) + 180 - self.arm_angle_from_vertical - self.int_wrist_angle

        return wrist_max_angle
    

    #Converts encoder counts to angles
    def convert_wrist_angle(self, counts):
        angle_shaft = counts/409600.0 * 360 #There are 409600 counts per revolution and 360 degrees in one rotation

        angle_end = 16/48 * angle_shaft #The big sproket for the wrist has 48 teeth and the small one has 16
        return angle_end
        

    def convert_elbow_angle(self, counts):
        angle_shaft = counts/409600.0 * 360 #There are 409600 counts per revolution and 360 degrees in one rotation

        angle_end = 16/48 * angle_shaft /3.25 #The big sproket for the elbow has 48 teeth and the small one has 16
        return angle_end


    #Turns on indecator lights based on corresponding sensor 
    def handle_sensor(self):
        if not self.sensor_middle.get():
            self.indecator_blue.set(True)
##            self.dashboard.putBoolean("DB/LED 1" , True)
            
        else:
            self.indecator_blue.set(False)
##            self.dashboard.putBoolean("DB/LED 1" , False)
            
        if not self.sensor_right.get():
            self.indecator_red.set(True)
##            self.dashboard.putBoolean("DB/LED 2" , True)
            
        else:
            self.indecator_red.set(False)
##            self.dashboard.putBoolean("DB/LED 2" , False)
            
        if not self.sensor_left.get():
            self.indecator_yellow.set(True)
##            self.dashboard.putBoolean("DB/LED 0" , True)
           
        else:
            self.indecator_yellow.set(False)
##            self.dashboard.putBoolean("DB/LED 0" , False)
            

    #Copy of teleop code for autonomous 
    def teleop_control(self):
        self.drive.tankDrive(self.l_joy.getRawAxis(1) , self.r_joy.getRawAxis(1))
        self.handle_sensor()
##        self.wrist_angle = self.convert_wrist_angle(self.wrist.getQuadraturePosition())
##        self.elbow_angle = self.convert_elbow_angle(self.elbow.getQuadraturePosition())
##        self.arm_angle_from_vertical = self.elbow_angle - self.int_elbow_angle
##        msg = 'Angles {0}'.format(self.elbow_angle)
##        self.dashboard.putString("DB/String 5" , msg)
        self.check_buttons()
##        self.arm_move()

            #Left and Right Joystick Buttons

        #L & R Gatherer Intake/Outtake Right and Left Joystick:
        if self.l_joy.getRawButton(1) == self.r_joy.getRawButton(1):
            self.l_gatherer.set(0) 
            self.r_gatherer.set(0)
            
        #30% picks up quickly enough without damaging anything (Intake)
        elif self.r_joy.getRawButton(1):
            self.l_gatherer.set(0.3) 
            self.r_gatherer.set(0.3)
            
        #50% shoots well but could work with less (Outtake)
        elif self.l_joy.getRawButton(1):
            self.l_gatherer.set(-0.5) 
            self.r_gatherer.set(-0.5)

        else:
            self.l_gatherer.set(0) 
            self.r_gatherer.set(0)

        #Piston Toggle Left or Right Joystick
        if self.l_joy.getRawButton(2) or self.r_joy.getRawButton(2):
            self.piston0.set(True)
            self.piston1.set(False)
        else:
            self.piston0.set(False)
            self.piston1.set(True)
        
        #Console messages for arm/drivetrain encoders
##        self.counter += 1
##
##        if self.counter % 50 == 0:
##            msg = 'Position Right Drive Motor {0}'.format(self.r_motorFront.getQuadraturePosition())
##            self.logger.info(msg)
##
##            msg = 'Angle {0}'.format(self.elbow_angle)
##            self.logger.info(msg)
        
        

if __name__ == "__main__":
    wpilib.run(MyRobot)
