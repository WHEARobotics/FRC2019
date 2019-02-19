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
        6. Cargo Ground
        7. Cargo Rocket Low
        8. Cargo C.S. (Cargo Ship Chute)
        9. Cargo Rocket Medium 

        (Hatch Panel) Outtake Left Joystick:
            #User Control Buttons
        1. L & R Gatherer out
        2. Elbow Down
        3. Elbow Up
        4. Piston

            #Automated Buttons
        6. Multi-Low (Rocket Hatch Port, Cargo Ship Hatch Port, Transfer Station)
        7. Hatch Panel Rocket Medium 
        8. Starting Configuration (For End Game Climb)
        
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
        self.wrist.setInverted(False)

        self.elbow.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Brake)
        self.wrist.setNeutralMode(ctre.wpi_talonsrx.WPI_TalonSRX.NeutralMode.Brake)

        self.elbow.setQuadraturePosition(0, 0)
        self.wrist.setQuadraturePosition(0, 0)

        
        #This is the setup for the gatherers
        self.l_gatherer = ctre.wpi_victorspx.WPI_VictorSPX(6)
        self.l_gatherer.setInverted(False)
        
        self.r_gatherer = ctre.wpi_victorspx.WPI_VictorSPX(7)
        self.r_gatherer.setInverted(False)

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
        wpilib.CameraServer.launch()
##        IP for camera server: http://10.38.81.2:1181/
        self.elbow_angles = [0 , 90 , 150 , 180 , 200]
        self.wrist_angles = [0 , 90 , 150 , 180 , 200]
        self.target_arm_position = 0
        self.previous_arm_position = 0
        self.wrist_state = 0
        self.elbow_state = 0

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

            #Right Joystick Buttons
        
        #L & R Gatherer Intake Right Joystick:
        if self.r_joy.getRawButton(1):
            self.l_gatherer.set(1) 
            self.r_gatherer.set(1)  
        else:
            self.l_gatherer.set(0) 
            self.r_gatherer.set(0)
            

        #Wrist Down Right Joystick:
        if self.r_joy.getRawButton(2):
            self.wrist.set(-1) 
        else:
            self.wrist.set(0)
            

        #Wrist Up Right Joystick:
        if self.r_joy.getRawButton(3):
            self.wrist.set(1) 
        else:
            self.wrist.set(0)


        #Piston Toggle Right Joystick
        if self.r_joy.getRawButton(4):
            self.piston0.set(True)
            self.piston1.set(False)
        else:
            self.piston0.set(False)
            self.piston1.set(True)


        #Cargo Ground Right Joystick
        if self.r_joy.getRawButton(6):
            pass


        #Cargo Rocket Low Right Joystick
        if self.r_joy.getRawButton(7):
            pass


        #Cargo C.S. (Cargo Ship) Right Joystick
        if self.r_joy.getRawButton(8):
            pass


        #Cargo Rocket Medium Right Joystick
        if self.r_joy.getRawButton(9):
            pass


        #Left Joystick Buttons
        
        #L & R Gatherer Outtake Left Joystick:
        if self.l_joy.getRawButton(1):
            self.l_gatherer.set(-1) 
            self.r_gatherer.set(-1)  
        else:
            self.l_gatherer.set(0) 
            self.r_gatherer.set(0)
            

        #Elbow Down Left Joystick:
        if self.l_joy.getRawButton(2):
            self.wrist.set(-1) 
        else:
            self.wrist.set(0)
            

        #Elbow Up Left Joystick:
        if self.r_joy.getRawButton(3):
            self.wrist.set(1) 
        else:
            self.wrist.set(0)


        #Piston Toggle Left Joystick
        if self.l_joy.getRawButton(4):
            self.piston0.set(True)
            self.piston1.set(False)
        else:
            self.piston0.set(False)
            self.piston1.set(True)


        #Multi-Low Left Joystick
        if self.r_joy.getRawButton(6):
            pass


        #Hatch Panel Rocket Medium Left Joystick
        if self.r_joy.getRawButton(7):
            pass


        #Starting Concfiguration Left Joystick
        if self.r_joy.getRawButton(8):
            pass
            

        self.counter += 1

        if self.counter % 50 == 0:
            msg = 'Posistion of Left & Right Drive Motors {0} {1}'.format(self.l_motorFront.getQuadraturePosition() , self.r_motorFront.getQuadraturePosition())
            self.logger.info(msg)

            msg = 'Velocity of Left & Right Drive Motors {0} {1}'.format(self.l_motorFront.getQuadratureVelocity() , self.r_motorFront.getQuadratureVelocity())
            self.logger.info(msg)

            msg = 'Posistion of Elbow & Wrist {0} {1}'.format(self.elbow.getQuadraturePosition() , self.wrist.getQuadraturePosition())
            self.logger.info(msg)

            msg = 'Velocity of Elbow & Wrist {0} {1}'.format(self.elbow.getQuadratureVelocity() , self.wrist.getQuadratureVelocity())
            self.logger.info(msg)

##            msg = 'Status of Optical Interrupter {0}'.format(self.optical.get())
##            self.logger.info(msg)


    def arm_move(self):
        wrist_angle = self.wrist.getQuadraturePosition()
        elbow_angle = self.elbow.getQuadraturePosition()

        self.delta_wrist_angle = self.wrist_angles[self.target_arm_position] - wrist_angle 
        self.delta_elbow_angle = self.elbow_angles[self.target_arm_position] - elbow_angle
        
        if (self.wrist.getQuadraturePosition() > 0) or (self.elbow.getQuadraturePosition() > 0):
            if self.delta_wrist_angle or self.delta_elbow_angle == 0:
                state = 0

        if self.wrist.getQuadraturePosition() > 0:
            if self.delta_wrist_angle <= 0:
                state = 2

            else:
                state = 1

        if self.elbow.getQuadraturePosition() > 0:
            if self.delta_elbow_angle <= 0:
                state = 3

            else:
                state = 2


        if arm_state == 0:
            self.wrist.set(0)
            self.elbow.set(0)

        elif arm_state == 1:
            self.wrist.set(0.2)
            self.elbow.set(0)

        elif arm_state == 2:
            self.wrist.set(0)
            if elbow_angle > 0:
                self.elbow.set(0.2)
            else:
                self.elbow.set(-0.2)
        else:
            self.elbow.set(0)
            self.wrist.set(-0.2)



##        if arm_state == 0:
##            pass
##
##        elif arm_state == 1:
##            if wrist_angle == self.wrist_angles[self.target_arm_position]:
##                self.arm_state = 2
##
##        elif arm_state == 2:
##            if elbow_angle == self.elbow_angles[self.target_arm_position]:
##                self.arm_state = 3
##
##        else:
##            if wrist_angle == self.wrist_angles[self.target_arm_position]:
##                self.arm_state = 0
##
##            elif elbow_angle == self.elbow_angles[self.target_arm_position]:
##                self.arm_state = 0
                               
                               
        
    def arm_check_state(self):
        pass
   



if __name__ == "__main__":
    wpilib.run(MyRobot)
