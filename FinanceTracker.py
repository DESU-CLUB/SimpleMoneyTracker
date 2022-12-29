import pandas as pd
import matplotlib as plt
import datetime
import os


#TODO: Finish refactoring FinanceTable methods touse Grouper and dt instead of nwords
#TODO: Finish the impl of helper functions
#TODO: Finish main program

class FinanceTable():
    '''
    Ideally, table structure is

    s/n  item  cost  date  remark

    Should support functions to evaluate total cost for entire month
    Should support functions to generate/load table
    Should support functions to find daily cost and thus average cost/month
    '''
    def __init__(self,path = None): #this code will be generalised for each month first
        if path != None:
            self.table = self.loadTable(path)
        self.readPath = path

    def loadTable(self,path):
        return pd.read_csv(path)

    def writeTable(self,writePath,changes):
        self.table.to_csv(writePath)

    def update(self,changes):
        if self.readPath == None:
            self.table = pd.DataFrame(changes,columns = ['item','cost','date','remarks'])
        else:
            self.table.concat(pd.DataFrame(changes),0)     

    def deleteItem(self,item,date):
        if self.table == pd.DataFrame and self.table.size >0:
            self.table.drop(self.table.loc[(self.table['item'] == item) & (self.table['date'] == date)])
        else:
            print('No items to delete')

    def findmaxCost(self,date,dateType = 'D'):
        '''
        Finds maximum cost in table, and which YY-MM-DD it was
        Date can be set to find max cost on date

        Returns None
        -------
        max cost

        '''
        if type(self.table) == pd.DataFrame:
            
            itemsOnDate = self.table
            itemsOnDate = itemsOnDate.loc[itemsOnDate['date'].dt.to_period(dateType) == date]
            maxCostRow = itemsOnDate.loc[itemsOnDate['cost'] == itemsOnDate['cost'].max()]
            
            if maxCostRow.size == 0:
                print('No data found')

            else:
                print('---------Returning item(s) with max cost-------------')
                print(maxCostRow)
        else:
            print('Invalid DataType, Generate table first!')
            
    def findDateCost(self,date,dateType = 'D',verbose = 0):#Takes specific day of month and year as input, finds cost in day/month/year
        if type(self.table) == pd.DataFrame:
            itemsOnDate = self.table.groupby(pd.Grouper(freq = dateType))
            itemsOnDate = itemsOnDate.loc[itemsOnDate['date'].dt.to_period(dateType) == date]
            if itemsOnDate.size == 0:
                print('No entries on given date/range')
                return 0
            if verbose:
                print(itemsOnDate.loc[:,itemsOnDate.columns != 'date'])
            return itemsOnDate['cost'].sum()
        
    def avgCost(self,date,dateType):
        if type(self.table) == pd.DataFrame:
            itemsOnDate = self.table
            itemsOnDate['date'] = pd.to_datetime(itemsOnDate['date'])
            itemsOnDate = itemsOnDate.loc[itemsOnDate['date'].dt.to_period(dateType) == date]
            if itemsOnDate.size == 0:
                return 0
            itemsOnDate = itemsOnDate.groupby(pd.Grouper(freq = 'D'))
            return itemsOnDate['cost'].mean()
        
    def analyzeCost(self,date,analyze = 'M'): #Prints a line graph, with date as X and spendings as Y, draws average cost line
        '''    
        #Takes two types of analyze: 
            Year: Analyzes monthly expenditure in year
            Month: Analyzes daily expenditure in month
        '''  
        itemsOnDate = self.table
        itemsOnDate['date'] = pd.to_datetime(self.table['date'])
        analyzeDict = {'M':'D','Y':'M'}
     
        itemsOnDate = itemsOnDate.loc[itemsOnDate['date'].dt.to_period(analyze) == date]
        if itemsOnDate.size == 0:
            print('No entries in given range')
        else:
            itemsOnDate.sort_values(by = 'date',inplace = True)
            itemsOnDate = itemsOnDate.groupby(pd.Grouper(freq = analyzeDict[analyze]))
            itemsOnDate.plot.line(itemsOnDate['date'],itemsOnDate['cost'].sum())
            itemsOnDate.plot.line(itemsOnDate['date'],[self.avgCost(date,analyze)]*itemsOnDate.size)
        
   
    
            
            
            
            
class MainHelper():
    def __init__(self,table):
        self.table = table
        self.main()
        
    def is_valid_date(self,date,dateType = 'D'):
        try:
            if dateType == 'D':
                datetime.datetime.strptime(date,'%YYYY-%MM-%DD')
            elif dateType == 'M':
                datetime.datetime.strptime(date,'%YYYY-%MM')
            elif dateType == 'Y':
                datetime.datetime.strptime(date,'%YYYY')
            else:
                raise ValueError
                
        except ValueError:
            return  False
        return True



    def save(self):
        save = input('Would you like to save changes[Y/N]: ')
        while save not in ['Y','N','y','n']:
            print('Valid answer required')
            save = input('Would you like to save changes[Y/N]: ')
        if save in ['y','Y']:
            if self.table.readPath != None:
                ow = input('Would you like to save changes into same file[Y/N]: ')
                while ow not in ['Y','N','y','n']:
                    print('Valid answer required')
                    ow = input('Would you like to save changes into same file[Y/N]: ')
                if ow in ['y','Y']:
                    self.table.writeTable(self.table.readPath)
                
            if self.table.readPath == None or ow in ['n','N']:
                path = input('Input path to write to: ')
                self.table.writeTable(path)

                
        
        
    def askhelper(self):
        changes = []
        while True:
            item = input('What was the item you bought: ')

            cost = input('How much did it cost: ')
            #Simple check for valid cost
            costcheck = [str(i) for i in range(10)]+['.']
            while list(filter(lambda x: x not in costcheck,list(cost))):
                cost = input('Please enter cost again: ')
            

            date = input('When did you buy it (YYYY-MM-DD): ')
            while not self.is_valid_date(date):
                date = input('Please enter date again: ')


            remarks = input('Any other remarks: ')
                
            quote = [item,cost,date,remarks]
            changes.append(quote)
                
            cont = input('Any more things to add?[Y/N]: ')
            while cont not in ['Y','N','y','n']:
                print('Valid answer required')
                cont = input('Any more things to add?[Y/N]: ')
            if cont in ['n','N']:
                break
        return changes
                
    def addItem(self):
        changes = self.askhelper()
        self.table.update(changes)
        self.save(self.table)  

    def deleteRecord(self):
        #find item then deletes it
        #give corresponding date as index if item has multiple entries
        item = input('Input item to delete: ')
        date = input('Input date item was purchased')
        self.table.deleteItem(item,date)
        pass

    def drop(self):
        if self.table.readPath != None and self.table.readPath.endswith('.csv'):
            os.remove(self.table.readPath)

    def analyzeItem(self):
        analyze = input(' Would You like to analyze month or year (M/Y)')
        if analyze not in ['M','Y','m','y']:
            print('Enter valid input')
            analyze = input(' Would You like to analyze month or year (M/Y)')

        if analyze.upper() == 'M':
            date = input('Enter date to analyze (YYYY-MM): ')
            while not self.is_valid_date(date,'M'):
                print('Enter valid date')
                date = input('Enter date to analyze (YYYY-MM): ')

        else:
            date = input('Enter date to analyze (YYYY): ')
            while not self.is_valid_date(date,'Y'):
                print('Enter valid date')
                date = input('Enter date to analyze (YYYY): ')
        
        self.table.analyzeCost(date,analyze.upper())

    def maxCost(self):
        dateFormat = {'D':'YYYY-MM-DD','M':'YYYY-MM','Y':'YYYY'}
        dateType = input('Would you like to check max cost for day/month/year (D/M/Y)')
        while dateType.upper() not in ['D','M','Y']:
            print('Invalid date type received')
            dateType = input('Would you like to check max cost for day/month/year (D/M/Y)')
            

    
        date = input(f'Enter date to check max cost ({dateType}): ')
        while not self.is_valid_date(date,dateType):
            print('Enter valid date')
            date = input(f'Enter date to check max cost ({dateType}): ')

        self.table.findMaxCost(date,dateType)
        
        
        

            
            

    def dateCost(self):
        date = input('Enter date to analyze (YYYY-MM-DD): ')
        while not self.is_valid_date(date):
            print('Enter valid date')
            date = input('Enter date to analyze (YYYY-MM-DD): ')
        
        
            


if __name__ == '__main__':
    path = input("Input Path for table (.csv): ")
    if path == '':
        table = FinanceTable()
    else:
        table = FinanceTable(path)
   
    
