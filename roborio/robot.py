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
        self.piston = wpilib.Solenoid(1 , 0)
        
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
##        if self.r_joy.getRawButton(4):
##            self.piston.set(True)
##            self.piston.set(True)
##        else:
##            self.piston.set(False)
##            self.piston.set(False)


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
##        if self.l_joy.getRawButton(4):
##            self.piston.set(True)
##            self.piston.set(True)
##        else:
##            self.piston.set(False)
##            self.piston.set(False)


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



if __name__ == "__main__":
    wpilib.run(MyRobot)
