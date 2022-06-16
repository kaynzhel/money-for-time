'''
'''
import os
from getInterface import Interface

def main():
    program = Program()
    program.run()

class Program:
    def __init__(self):
        self.continue_prog = True
        self.input = ''
        self.interface = Interface() # calls the class Interface from getInterface
    
    def run(self):
    	# a method that runs the program
        self.clear()
        self.signIn()
        while self.continue_prog:
            while not self.input in ('C', 'c', 'A', 'a', 'L', 'l'):
                self.instructions()
            if self.input == 'C' or self.input == 'c':
                self.interface.checkMoney()
            elif self.input == 'A' or self.input == 'a':
                self.interface.addTime()
            else:
                self.interface.getLastUpdate()
            self.decideContinue()   
        self.interface.closeDB()

    def signIn(self):
    	# a method that runs the opening statement of the program
        proper_inputs = ('L','l','S','s')
        user_decide = ''
        print("LOG IN or SIGN UP")
        while user_decide not in proper_inputs:
            user_decide = input("Press L/l to log in or S/s to sign up: ")
        if user_decide == 'L' or user_decide == 'l': self.interface.getID()
        else: self.interface.makeID()
        
    def instructions(self):
        print("\nWhat do you want to do?")
        print("Press C if you want to check your balance.")
        print("Press A if you want to add your time.")
        print("Press L if you want to see when you last updated.")
        self.input = input("Key: ")

    def decideContinue(self):
        proper_inputs = ('Y','y','N','n')
        user_decide = ''
        while user_decide not in proper_inputs:
            user_decide = input("\nPress Y/y if you want to continue. N/n if not. ")
        if user_decide == 'N' or user_decide == 'n':
            self.continue_prog = False
        else:
            self.resetVariables()
            self.clear()

    def resetVariables(self):
        self.input = ''
        self.interface.resetVariables()

    def clear(self):
        os.system('clear')   

main()