#!/usr/bin/env python3
"""
    WHEA Robotics 3881 code for FRC 2018.
"""

import wpilib
import ctre
import wpilib.drive


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
        2. Wrist Down
        3. Wrist Up
        4. Piston

            #Automated Buttons
        6. Cargo Ground [6]
        7. Cargo Rocket Low [4]
        8. Cargo C.S. (Cargo Ship Chute) [2]
        9. Cargo Rocket Medium [1]

        (Hatch Panel) Outtake Left Joystick:
            #User Control Buttons
        1. L & R Gatherer out
        2. Elbow Down
        3. Elbow Up
        4. Piston

            #Automated Buttons
        6. Multi-Low (Rocket Hatch Port, Cargo Ship Hatch Port, Transfer Station) [5]
        7. Hatch Panel Rocket Medium [3]
        8. Starting Configuration (For End Game Climb) [0]
        
        """
    
        #Here is the encoder setup for the 4 motor drivetrain
        self.l_motorFront = ctre.wpi_talonsrx.WPI_TalonSRX(0)
        self.l_motorFront.setInverted(False)

        self.l_motorBack = ctre.wpi_talonsrx.WPI_TalonSRX(1)
        self.l_motorBack.setInverted(False)

        self.r_motorFront = ctre.wpi_talonsrx.WPI_TalonSRX(2)
        self.r_motorFront.setInverted(False)
        
        self.r_motorBack = ctre.wpi_talonsrx.WPI_TalonSRX(3)
        self.r_motorBack.setInverted(False)

        self.l_motorFront.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast) 
        self.l_motorBack.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)

        self.r_motorFront.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast) 
        self.r_motorBack.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)

        self.l_motorFront.setQuadraturePosition(0, 0)
        self.r_motorFront.setQuadraturePosition(0, 0)

    
        #Here is the encoder setup for the elbow and wrist joints
        self.elbow = ctre.wpi_talonsrx.WPI_TalonSRX(4)
        self.elbow.setInverted(False)
        
        self.wrist = ctre.wpi_talonsrx.WPI_TalonSRX(5)
        self.wrist.setInverted(True)

        self.elbow.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Brake)
        self.wrist.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Brake)

        self.elbow.setQuadraturePosition(0, 0)
        self.wrist.setQuadraturePosition(0, 0)

        
        #This is the setup for the gatherers
        self.l_gatherer = ctre.wpi_victorspx.WPI_VictorSPX(6)
        self.l_gatherer.setInverted(False)
        
        self.r_gatherer = ctre.wpi_victorspx.WPI_VictorSPX(7)
        self.r_gatherer.setInverted(True)

        self.l_gatherer.setNeutralMode(ctre.wpi_victorspx.WPI_VictorSPX.NeutralMode.Brake)
        self.r_gatherer.setNeutralMode(ctre.wpi_victorspx.WPI_VictorSPX.NeutralMode.Brake)

        #Setup for pnumatics
        self.piston0 = wpilib.Solenoid(1 , 0)
        self.piston1 = wpilib.Solenoid(1 , 1)
        
        #Setup for drive groups and extras               
        self.l_joy = wpilib.Joystick(0)
        self.r_joy = wpilib.Joystick(1)
        
        self.left = wpilib.SpeedControllerGroup(self.l_motorFront, self.l_motorBack)
        self.right = wpilib.SpeedControllerGroup(self.r_motorFront, self.r_motorBack)
        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)
        self.counter = 0
        self.auto_loop_counter = 0
##        self.optical = wpilib.DigitalInput(4)      
##        wpilib.CameraServer.launch()
##        IP for camera server: http://10.38.81.2:1181/
        
##        [0] = Starting Config (8L)
##        [1] = Cargo Rocket Med (9R)                              
##        [2] = Cargo C.S. (8R)                            
##        [3] = Hatch Panel Rocket Med (7L)                  
##        [4] = Cargo Rocket Low (7R)              
##        [5] = Multi-Low (6L)  
##        [6] = Cargo Ground (6R) 
        self.elbow_angles = [0 , 54.4 , 73 , 100.8 , 155.7 , 177.4 , 205]              
        self.wrist_angles = [0 , -100 , -55.7 , -64.3 , -5.9 , 15.3 , -24]              
        self.target_arm_position = 0
        self.previous_arm_position = 0
        self.wrist_state = 0
        self.elbow_state = 0
        self.arm_state = 0

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        pass
    
    
    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        pass
    

    def teleopInit(self):
        """This function is run once each time the robot enters teleoperated mode."""
        
        self.l_motorFront.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast) 
        self.l_motorBack.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)

        self.r_motorFront.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast) 
        self.r_motorBack.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Coast)

        self.l_motorFront.setQuadraturePosition(0, 0)
        self.r_motorFront.setQuadraturePosition(0, 0)

        self.elbow.setQuadraturePosition(0, 0)
        self.wrist.setQuadraturePosition(0, 0)

        self.l_gatherer.setNeutralMode(ctre.wpi_victorspx.WPI_VictorSPX.NeutralMode.Brake)
        self.r_gatherer.setNeutralMode(ctre.wpi_victorspx.WPI_VictorSPX.NeutralMode.Brake)
        

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""

        self.drive.tankDrive(self.l_joy.getRawAxis(1) , self.r_joy.getRawAxis(1))

            #Left and Right Joystick Buttons

        #L & R Gatherer Intake/Outtake Right and Left Joystick:
        if self.l_joy.getRawButton(1) == self.r_joy.getRawButton(1):
            self.l_gatherer.set(0) 
            self.r_gatherer.set(0)
        #30% picks up quickly enough without damaging anything
        elif self.r_joy.getRawButton(1):
            self.l_gatherer.set(0.3) 
            self.r_gatherer.set(0.3)
        #50% shoots well but could work with less
        elif self.l_joy.getRawButton(1):
            self.l_gatherer.set(-0.5) 
            self.r_gatherer.set(-0.5)

        else:
            self.l_gatherer.set(0) 
            self.r_gatherer.set(0)

        #Wrist Up Right Joystick:
        if self.r_joy.getRawButton(3):
            self.wrist.set(1) 
        else:
            self.wrist.set(0)

        #Piston Toggle Left or Right Joystick
        if self.l_joy.getRawButton(4) or self.r_joy.getRawButton(4):
            self.piston0.set(True)
            self.piston1.set(False)
        else:
            self.piston0.set(False)
            self.piston1.set(True)


            #Right Joystick Buttons

        #Wrist Down and Wrist up Right Joystick:
        if self.r_joy.getRawButton(2) == self.r_joy.getRawButton(3):
            self.wrist.set(0)

        elif self.r_joy.getRawButton(2):
            self.wrist.set(-1)
            
        elif self.r_joy.getRawButton(3):
            self.wrist.set(1)

        else:
            self.wrist.set(0)


        #Left Joystick Buttons
            
        #Elbow Down and Elbow up Left Joystick:
        if self.l_joy.getRawButton(2) == self.l_joy.getRawButton(3):
            self.elbow.set(0)

        elif self.l_joy.getRawButton(2):
            self.elbow.set(-1)
            
        elif self.l_joy.getRawButton(3):
            self.elbow.set(1)

        else:
            self.elbow.set(0)
            

        self.counter += 1

        if self.counter % 50 == 0:
            msg = 'Position Right Drive Motor {0}'.format(self.r_motorFront.getQuadraturePosition())
            self.logger.info(msg)

            msg = 'Position of Elbow & Wrist {0} {1}'.format(self.elbow.getQuadraturePosition() , self.wrist.getQuadraturePosition())
            self.logger.info(msg)

##            msg = 'Status of Optical Interrupter {0}'.format(self.optical.get())
##            self.logger.info(msg)


    #Set state based on button press
    def check_buttons(self):
        if self.l_joy.getRawButton(6): #Multi-Low Left Joystick
            self.target_arm_position = 5
            self.arm_state = 1

        elif self.l_joy.getRawButton(7): #Hatch Panel Rocket Medium Left Joystick
            self.target_arm_position = 3
            self.arm_state = 1   
            
        elif self.l_joy.getRawButton(8): #Starting Concfiguration Left Joystick
            self.target_arm_position = 0
            self.arm_state = 1

        elif self.r_joy.getRawButton(6): #Cargo Ground Right Joystick
            self.target_arm_position = 6
            self.arm_state = 1

        elif self.r_joy.getRawButton(7): #Cargo Rocket Low Right Joystick
            self.target_arm_position = 4
            self.arm_state = 1

        elif self.r_joy.getRawButton(8): #Cargo C.S. (Cargo Ship) Right Joystick
            self.target_arm_position = 2
            self.arm_state = 1

        elif self.r_joy.getRawButton(9): #Cargo Rocket Medium Right Joystick
            self.target_arm_position = 1
            self.arm_state = 1

            
    def arm_move(self):
        self.wrist_angle = convert_wrist_angle(self.wrist.getQuadraturePosition())
        self.elbow_angle = convert_elbow_angle(self.elbow.getQuadraturePosition())

        delta_wrist_angle = self.wrist_angles[self.target_arm_position] - self.wrist_angle 
        delta_elbow_angle = self.elbow_angles[self.target_arm_position] - self.elbow_angle
        
    #Check for state transitions
    if self.arm_state == 0:
        pass # A change out of state 0 only happens when a button is pressed, inside check_buttons().

        elif self.arm_state == 1:
            if self.delta_wrist_angle <= 0.0:
                self.arm_state = 2 # To the next state.  Also, no need for an "else" because if the test is false, we just stay in state 1.

        elif self.arm_state == 2:
            if self.elbow.get() > 0.0:
                if self.delta_elbow_angle <= 0.0:
                    self.arm_state = 3  # Target angle reached, go to next state.

        elif self.elbow.get() < 0.0: # Negative is counterclockwise.
            if self.delta_elbow_angle <= 0.0:
                self.arm_state = 3 
       
            else:
                self.delta_elbow angle == 0.0:
                    self.arm_state = 0 # Extraordinary case
                
    else:      
        self.arm_state == 3:   # This is the 0.0 case, which would not expect in state 2, so panic and stop.
            if self.delta_wrist_angle >= 0:
                self.arm_state = 0 # The state 3 case.

        #Move arm based on state 
        if self.arm_state == 0:
            self.wrist.set(0)
            self.elbow.set(0)

        elif self.arm_state == 1:
            self.wrist.set(0.2)
            self.elbow.set(0)

        elif self.arm_state == 2:
            self.wrist.set(0)
            if elbow_angle > 0:
                self.elbow.set(0.2)
            else:
                self.elbow.set(-0.2)
        else:
            self.elbow.set(0)
            self.wrist.set(-0.2)


    #Converts encoder counts to angles
    def convert_wrist_angle (self, counts):

        angle_shaft = counts/409600.0 * 360 #There are 409600 counts per revolution and 360 degrees in one rotation

        angle_end = 16/48 * angle_shaft #The big sproket for the wrist has 48 teeth and the small one has 16
        return angle_end
        


    def convert_elbow_angle (self, counts):

        angle_shaft = counts/409600.0 * 360 #There are 409600 counts per revolution and 360 degrees in one rotation

        angle_end = 16/48 * angle_shaft #The big sproket for the elbow has 48 teeth and the small one has 16
        return angle_end   



if __name__ == "__main__":
    wpilib.run(MyRobot)
