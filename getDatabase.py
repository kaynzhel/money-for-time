'''
References: https://sqlite.org/datatype3.html
Last edited: April 04, 2021
'''
import sqlite3

class Database():
    def __init__(self):
        self.connection = sqlite3.connect('./moneyForTime.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(' PRAGMA foreign_keys=ON; ')
        self.defineTables()
        self.connection.commit()
    
    def closeDatabase(self):
        # closes the database when the user decides not to continue
        self.connection.close()

    def defineTables(self):
        # defines the following tables of the database
        # time_input in table time is in minutes
        user_query = '''
                    CREATE TABLE IF NOT EXISTS user (
                        user_id INTEGER,
                        name TEXT,
                        PRIMARY KEY (user_id));
                    '''
        
        time_query = '''
                    CREATE TABLE IF NOT EXISTS time (
                        user_id INTEGER,
                        time_input REAL,
                        data_time_updated TEXT,
                        update_num INTEGER,
                        FOREIGN KEY (user_id) REFERENCES user(user_id));
                    '''
        
        money_query = '''
                    CREATE TABLE IF NOT EXISTS money (
                        user_id INTEGER,
                        time REAL,
                        money_per_time REAL,
                        PRIMARY KEY (user_id),
                        FOREIGN KEY (user_id) REFERENCES user(user_id));
                    '''
        
        self.cursor.execute(user_query)
        self.cursor.execute(time_query)
        self.cursor.execute(money_query)
        self.connection.commit()
    
    def checkID(self, user_id):
        # checks if an ID exists or not
        user = (user_id,)
        check_query = '''
                        SELECT *
                        FROM user
                        WHERE user_id = ?
                        LIMIT 1;
                        '''
        self.cursor.execute(check_query, user)
        data = self.cursor.fetchall()
        self.connection.commit()

        if len(data) != 0: return True # the id exists
        else: return False # the id does not exist

    def checkMoney(self, user_id):
        # checks if the user already inputted a certain money for time
        user = (user_id,)
        check_query = '''
                        SELECT *
                        FROM money 
                        WHERE user_id = ?;
                    '''
        self.cursor.execute(check_query, user)
        data = self.cursor.fetchall()
        self.connection.commit()

        if len(data) != 0: return True # the id exists
        else: return False # the id does not exist

    def checkIfRowTimeExists(self, user_id):
        # check if there exists at least one update for the account
        user = (user_id,)
        check_query = '''
                        SELECT *
                        FROM time
                        WHERE user_id = ?
                        LIMIT 1;
                        '''
        self.cursor.execute(check_query, user)
        data = self.cursor.fetchall()
        self.connection.commit()

        if len(data) != 0: return True # there is at least one input
        else: return False # there is no input

    def getLastInput(self, user_id):
        # gets the last input of a certain user
        update_num = self.getUpdateNum(user_id)
        last_input = '''
                    SELECT time_input, data_time_updated
                    FROM time
                    WHERE user_id = :id
                    AND update_num = :number;'''
        self.cursor.execute(last_input, {"id":user_id, "number":update_num})
        data = self.cursor.fetchone() # data[0]: time , data[1] = date
        self.connection.commit()
        return data[0], data[1]

    def getUpdateNum(self, user_id):
        # gets and returns how many updates there are for the user
        user = (user_id,)
        check_rows = '''
                    SELECT COUNT(*)
                    FROM time
                    WHERE user_id = ?;'''
        self.cursor.execute(check_rows, user)
        update_num = self.cursor.fetchone()[0]
        self.connection.commit()
        return update_num

    def getName(self, user_id):
        # takes the name of the user
        user = (user_id,)
        get_name = '''
                    SELECT name
                    FROM user
                    WHERE user_id = ?;'''
        self.cursor.execute(get_name, user)
        name = self.cursor.fetchone()[0]
        self.connection.commit()
        return name

    def getTotalTime(self, user_id):
        # gets the total time for a certain user
        total = 0
        user = (user_id,)
        get_time = '''
                    SELECT time_input
                    FROM time
                    WHERE user_id = ?;'''
        self.cursor.execute(get_time, user)
        time_list = self.cursor.fetchall()
        self.connection.commit()

        for index in range(len(time_list)): total += time_list[index][0]
        return total

    def getMoneyTime(self, user_id):
        # gets the money amount per specific time
        user = (user_id,)
        get_money_time = '''
                            SELECT time, money_per_time
                            FROM money
                            WHERE user_id = ?;
                        '''
        self.cursor.execute(get_money_time, user)
        data = self.cursor.fetchone() # data[0]: time, data[1] = money_per_time
        self.connection.commit()
        return data[0], data[1]

    def addUser(self, user_id, user_name):
        # adds a user if it does not exist
        data = (user_id, user_name)
        insert_user = '''INSERT INTO user(user_id, name) VALUES (?,?);'''
        self.cursor.execute(insert_user, data)
        self.connection.commit()

    def addTime(self, user_id, input_time, current_time):
        # adds the time for the user
        update_num = self.getUpdateNum(user_id) + 1
        data = (user_id, input_time, current_time, update_num)
        insert_time = '''INSERT INTO time(user_id, time_input, data_time_updated, update_num) VALUES (?,?,?,?);'''
        self.cursor.execute(insert_time, data)
        self.connection.commit()
    
    def addMoney(self, update, user_id, time_mins, prize_amt):
        # inserts or updates the given time
        data_not_exists = (user_id, time_mins, prize_amt)
        user = (user_id,)
        time_mins_data = (time_mins,)
        prize_amt_data = (prize_amt,)
        if update:
            query = '''
                        UPDATE money
                        SET time = :time_input
                        SET money_per_time = :amount
                        WHERE user_id = :id;
                    '''
            self.cursor.execute(query, {"time_input":time_mins_data, "amount":prize_amt_data, "id":user})
        else:
            query = '''INSERT INTO money(user_id, time, money_per_time) VALUES (?,?,?);'''
            self.cursor.execute(query, data_not_exists)
        self.connection.commit()