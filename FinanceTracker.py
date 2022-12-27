import pandas as pd
import matplotlib as plt
import datetime

class FinanceTable():
    '''
    Ideally, table structure is

    s/n  item  cost  date  remark

    Should support functions to evaluate total cost for entire month
    Should support functions to generate/load table
    Should support functions to find daily cost and thus average cost/month
    '''
    def __init__(self,path = None): #this code will be generalised for each month first
        if path == None:
            self.table = self.generateTable()
            self.month = datetime.date.today().month
        else:
            self.table = self.loadTable(path)
            #Code to find earliest date in table 
        self.readPath = path

        
    def generateTable(self): #Good practice to make list, then grow data in list before making Dataframe
        return []


    def loadTable(self,path):
        return pd.read_csv(path)

    def writeTable(self,writePath):
        if self.readPath == None:
            df = pd.DataFrame(self.table,columns = ['item','cost','date','remarks'])
            df.to_csv()
        
        


def is_valid_date(date):
    try:
        datetime.datetime.strptime(date,'%m-%d')
    except ValueError:
        return  False
    return True
    


if __name__ == '__main__':


    while True:
        item = input('What was the item you bought: ')
        cost = input('How much did it cost: ')

        #Simple check for valid cost
        costcheck = [str(i) for i in range(9)]+['.']
        while list(filter(lambda x: x not in costcheck,list(cost))):
            cost = input('Please enter cost again: ')
        

        date = input('When did you buy it (MM-DD): ')
        while not is_valid_date(date):
            date = input('Please enter date again: ')


        remarks = input('Any other remarks: ')



