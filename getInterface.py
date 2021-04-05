'''
Last edited: April 04, 2021
'''
from getDatabase import Database
from time import time, ctime
import random

class Interface:
    def __init__(self):
        # variables for checking money
        self.money = 0 # total money you have
        self.prize_amt = 0 # $ per self.time_mins
        self.time_mins = 0 # time per self.prize_amt
        # variables for the time
        self.input_time = 0 # what the user has currently inputted
        self.total_time = 0 # the total time that the user has inputted
        self.user_id = 0 
        self.user_name = ''
        self.current_time = '' # current time when the user inputted his/her/their time
        self.database = Database() # calls the class Database from getDatabase

    def resetVariables(self):
        self.money = 0
        self.prize_amt = 0
        self.time_mins = 0
        self.input_time = 0
        self.total_time = 0
        self.current_time = ''  

    def closeDB(self):
        self.database.closeDatabase()

    def getID(self):
        # gets the user ID of the current user
        valid_id = False # an id already

        while valid_id == False:
            try:
                self.user_id = int(input('Please enter your user ID: '))
            except:
                print("Your user id is an integer number. Try again!")
            else:
                exists = self.database.checkID(self.user_id)
                if exists == False: self.makeID()
                valid_id = True

    def makeID(self):
        # main method that makes the user ID
        self.user_name = input('You are not registered yet! Enter your name to start: ')
        self.generateID()
        print("This is your user ID: " + str(self.user_id))
        self.database.addUser(self.user_id, self.user_name)

    def generateID(self):
        # generates a random id and checks if it is available
        lower = 1
        upper = 1000000
        exists = True

        while exists:
            self.user_id = random.randint(lower, upper)
            exists = self.database.checkID(self.user_id)

    def checkMoney(self):
        # a method that runs the 'c' function of the prgram
        proper_inputs = ('Y','y','N','n')
        user_decide = ''
        check = True
        
        exists = self.database.checkMoney(self.user_id) # checks if the user exists in the table money
        if exists:
            self.time_mins, self.prize_amt = self.database.getMoneyTime(self.user_id)
            print("\nYou already have a set amount for your money per specific minutes.")
            print("Time: " + str(self.time_mins) + ", Money per time: " + str(self.prize_amt))
            print("\nDo you want to change it or continue?")
            while user_decide not in proper_inputs:
                user_decide = input("Press 'Y/y' to continue or 'N/n' to change it: ")
            if user_decide == 'N' or user_decide == 'n':
                print("Update your information:")
                self.getTimeMins()
                self.getPrizeMoney()
                self.database.addMoney(True, self.user_id, self.time_mins, self.prize_amt) # updates
        else:
            time_exists = self.database.checkIfRowTimeExists(self.user_id)
            if time_exists:
                self.database.addMoney(False, self.user_id, self.time_mins, self.prize_amt) # inserts
                print("You do not have a set amount yet. Go add one!")
                self.getTimeMins()
                self.getPrizeMoney()
            else:
                check = False
                print("You have not inputted anything yet. Go add a time!")

        if check: 
            self.total_time = self.database.getTotalTime(self.user_id)
            self.getMoney()
        print("\nThis is the the total time: " + str(self.total_time) + " minutes")
        print("This is how much money you have: $ {:.2f}".format(self.money))

    def addTime(self):
        # performs the "A" process
        self.getInputTime()
        self.total_time = self.database.getTotalTime(self.user_id)
        print("\nThis is the time that you inputted: " + str(self.input_time))
        print("This is the the total time: " + str(self.total_time) + " minutes")
    
    def getLastUpdate(self):
        # performs the "L" process
        exists = self.database.checkIfRowTimeExists(self.user_id)
        if exists:
            last_input, date = self.database.getLastInput(self.user_id)
            print("\nThis is the last time you updated: " + date)
            print("This is the last time you inputted (in minutes): " + str(last_input))
        else: print("You have not inputted anything yet. Go add a time!")

    def getTimeMins(self):
        # gets the time that the user wants for a specific amount
        incorrect = True
        while incorrect and self.time_mins <= 0:
            try:
                self.time_mins = float(input('How many minutes for a specific amount? '))
            except:
                print("It must be a number!")
            else:
                if self.time_mins <= 0:
                    print("It must be a positive number. Try again!")
                else:
                    incorrect = False

    def getPrizeMoney(self):
        # gets the prize amount for a specific time inputted by the user
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
    
    def getMoney(self):
        # gets the total money of the current user
        self.money = (self.total_time / float(self.time_mins)) * float(self.prize_amt)

    def getInputTime(self):
        # gets the time of the user
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
        
        self.database.addTime(self.user_id, self.input_time, ctime(self.current_time))