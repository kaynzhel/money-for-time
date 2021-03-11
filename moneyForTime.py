'''
Last edited: March 4, 2021
'''
import os
from time import time, ctime

def main():
    program = Program()
    program.run()
    
class Program:
    def __init__(self):
        self.continue_prog = True
        self.money = 0
        self.prize_amt = 0
        self.time_mins = 0
        self.input_time = 0
        self.total_time = 0
        self.file_name = ''
        self.input = ''
        self.current_time = ''
        self.date_file_name = ''
    
    def run(self):
        self.clear()
        self.getFile()
        while self.continue_prog:
            while not self.input in ('C', 'c', 'A', 'a', 'L', 'l'):
                self.getInstructions()
            if self.input == 'C' or self.input == 'c':
                self.checkMoney()
            elif self.input == 'A' or self.input == 'a':
                self.addTime()
            else:
                self.getLastUpdate()
            self.decideContinue()   

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
        self.money = 0
        self.prize_amt = 0
        self.time_mins = 0
        self.input_time = 0
        self.total_time = 0
        self.input = ''
        self.current_time = ''  

    def clear(self):
        os.system('clear')   

    def getFile(self):
        self.file_name = input('Please enter your account name: ')
        self.date_file_name = self.file_name + '_date'

    def checkMoney(self):
        self.getTimeMins()
        self.getPrizeMoney()
        self.getTotalTime()
        self.getMoney()
        print("\nThis is the the total time: " + str(self.total_time) + " minutes")
        print("This is how much money you have: $ {:.2f}".format(self.money))

    def addTime(self):
        self.getInputTime()
        self.getTotalTime()
        print("\nThis is the time that you inputted: " + str(self.input_time))
        print("This is the the total time: " + str(self.total_time) + " minutes")

    def getInstructions(self):
        print("\nWhat do you want to do?")
        print("Press C if you want to check your balance.")
        print("Press A if you want to add your time.")
        print("Press L if you want to see when you last updated.")
        self.input = input("Key: ")

    def getTimeMins(self):
        incorrect = True
        while incorrect and self.time_mins <= 0:
            try:
                self.time_mins = float(input('How many minutes for a specific amount? '))
            except:
                print("It must be a number!")
            else:
                if self.time_mins <= 0:
                    print("It must be a positive number. Try again.")
                else:
                    incorrect = False
    
    def getPrizeMoney(self):
        incorrect = True
        while incorrect and self.prize_amt <= 0:
            try:
                self.prize_amt = float(input("What's the prize reward in $? "))
            except:
                print("It must be a number!")
            else:
                if self.prize_amt <= 0:
                    print("It must be a positive number. Try again.")
                else:
                    incorrect = False
    
    def getTotalTime(self):
        file = open(self.file_name, 'r')
        for line in file.readlines():
            self.total_time += int(line)
        file.close()
    
    def getMoney(self):
        self.money = (self.total_time / float(self.time_mins)) * float(self.prize_amt)

    def getInputTime(self):
        incorrect = True
        
        while incorrect:
            self.input_time = 0
            try:
                self.input_time += int(input('What is your time in hours? ')) * 60
                self.current_time = time()
                self.input_time += int(input('What is your time in minutes? '))
            except:
                print("It must be an integer number!")
            else:
                if self.input_time < 0:
                    print("It must not be a negative number!")
                else:
                    incorrect = False
        
        file = open(self.file_name, 'a') # a is for append
        file.write('{}\n'.format(self.input_time))
        file.close()
        self.addCurrentTime()
    
    def addCurrentTime(self):
        file = open(self.date_file_name, 'w')
        file.write(ctime(self.current_time))
        file.close()

    def getLastUpdate(self):
        try:
            file = open(self.date_file_name, 'r')
            date = file.read()
            file.close()
        except:
            print("\nYou haven't made your account! Go add a time.")
        else:
            file = open(self.file_name, 'r')
            for last_time in file.readlines(): pass
            file.close()
            print("\nThis is the last time you updated: " + date)
            print("This is the last time you inputted (in minutes): " + str(last_time))

main()
