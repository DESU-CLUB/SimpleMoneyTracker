import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os


#TODO: Create SELECT for PD dataframe, add avgcost functionality into main
#TODO: Create dummy data for testing purposes
##TODO: Increase range of avgcost to week???

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

    def writeTable(self,writePath):
        self.table.to_csv(writePath,index = False)
        self.readPath = writePath

    def update(self,changes):
        if self.readPath == None:
            self.table = pd.DataFrame(changes,columns = ['item','cost','date','remarks'])
        else:
            self.table.concat(pd.DataFrame(changes),0)     

    def deleteItem(self,item,date):
        if type(self.table) == pd.DataFrame and self.table.size >0:
            result = self.table.loc[(self.table['item'] == item) & (self.table['date'] == date)]
            if result.size >0:
                self.table.drop(result.index,inplace = True)
            else:
                print('No items to delete')
        else:
            print('No items to delete')


    def checkItems(self,date,dateType): #Check items on given date
        if type(self.table) == pd.DataFrame:
            itemsOnDate = self.table
            itemsOnDate['date'] = pd.to_datetime(itemsOnDate['date'])
            itemsOnDate = itemsOnDate.loc[itemsOnDate['date'].dt.to_period(dateType) == date]

            if itemsOnDate.size == 0:
                print('No data found')

            else:
                print(f'---------Returning item(s) purchased on {date}-------------')
                print(itemsOnDate)
        else:
            print('Invalid DataType, Generate table first!')
            
           
    def findMaxCost(self,date,dateType = 'D'):
        '''
        Finds maximum cost in table, and which YY-MM-DD it was
        Date can be set to find max cost on date

        Returns None
        -------
        max cost

        '''
        if type(self.table) == pd.DataFrame:
            
            itemsOnDate = self.table
            itemsOnDate['date'] = pd.to_datetime(itemsOnDate['date'])
            itemsOnDate = itemsOnDate.loc[itemsOnDate['date'].dt.to_period(dateType) == date]
            maxCostRow = itemsOnDate.loc[itemsOnDate['cost'] == itemsOnDate['cost'].max()]
            
            if maxCostRow.size == 0:
                print('No data found')

            else:
                print('---------Returning item(s) with max cost-------------')
                print(maxCostRow)
                print()
                print(f'Max Cost is {maxCostRow["cost"].values}')
        else:
            print('Invalid DataType, Generate table first!')
            
    def findTotalCost(self,date,dateType = 'D',verbose = 0):#Takes specific day of month and year as input, finds total cost in day/month/year
        if type(self.table) == pd.DataFrame:
            itemsOnDate = self.table
            itemsOnDate['date'] = pd.to_datetime(itemsOnDate['date'])
            itemsOnDate = itemsOnDate.loc[itemsOnDate['date'].dt.to_period(dateType) == date]
            if itemsOnDate.size == 0:
                print('No entries on given date/range')
                return 0
            if verbose:
                print(itemsOnDate.loc[:,itemsOnDate.columns != 'date'])
            return itemsOnDate['cost'].sum()
        
    def avgCost(self,date,dateType):
        avgDict = {'M':'D','Y':'M'}
        if type(self.table) == pd.DataFrame:
            itemsOnDate = self.table
            itemsOnDate['date'] = pd.to_datetime(itemsOnDate['date'])
            itemsOnDate = itemsOnDate.loc[itemsOnDate['date'].dt.to_period(dateType) == date]
            if itemsOnDate.size == 0:
                return 0
            itemsOnDate['date'] = pd.to_datetime(itemsOnDate['date'])
            itemsOnDate = itemsOnDate.groupby(pd.Grouper(key = 'date',freq = avgDict[dateType]))
            return itemsOnDate['cost'].sum().mean()
        
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
            itemsOnDate['date'] = pd.to_datetime(itemsOnDate['date'])
            dates = itemsOnDate['date'].drop_duplicates().to_numpy()
            print(dates)
            itemsOnDate = itemsOnDate.groupby(pd.Grouper(key = 'date',freq = analyzeDict[analyze]))
            
            plt.plot(dates,itemsOnDate['cost'].sum(),'r-')
            plt.plot(dates,[self.avgCost(date,analyze)]*len(itemsOnDate),'b-')
            plt.show()
        
   
    
            
            
            
            
class MainHelper():
    def __init__(self,table):
        self.table = table
        self.dateFormat = {'D':'YYYY-MM-DD','M':'YYYY-MM','Y':'YYYY'}


    def optionPrinter(self):
        
        options = ['Add item to table',
           'Delete item from table',
           'Print items on given date',
           'Check Maximum Cost',
           'Check Total Cost',
           'Analyze Cost over a range',
            'Delete Entire Table',
           'Quit Application',
           'Restate Options']
        for idx,option in enumerate(options,1):
            print(f'{idx}: {option}')
        print('\n\n')

    def is_valid_date(self,date,dateType = 'D'):
        try:
            if dateType == 'D':
                datetime.datetime.strptime(date,'%Y-%m-%d')
            elif dateType == 'M':
                datetime.datetime.strptime(date,'%Y-%m')
            elif dateType == 'Y':
                datetime.datetime.strptime(date,'%Y')
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
        
        ow = 'N'
        if save in ['y','Y']:
            if self.table.readPath != None:
                ow = input('Would you like to save changes into same file[Y/N]: ')
                while ow not in ['Y','N','y','n']:
                    print('Valid answer required')
                    ow = input('Would you like to save changes into same file[Y/N]: ')
                if ow in ['y','Y']:
                    self.table.writeTable(self.table.readPath)
                
            if self.table.readPath == None or ow in ['n','N']:
                path = input('Input path to write to (include name of file): ')
                while not path.endswith('.csv'):
                    print('Invalid path')
                    path = input('Input path to write to (include name of file): ')
                self.table.writeTable(path)
                self.path = path

                
        
        
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
                date = input('Please enter date again (YYYY-MM-DD): ')


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
        self.save()  

    def length(self):
        return len(self.table.table)

    def deleteRecord(self):
        #find item then deletes it
        #give corresponding date as index if item has multiple entries
        item = input('Input item to delete: ')
        date = input('Input the date item was purchased (YYYY-MM-DD): ')
        self.table.deleteItem(item,date)
        self.save()

    def findItemOnDate(self):
        dateType = input('Would you like to find items for day/month/year (D/M/Y): ')
        while dateType.upper() not in ['D','M','Y']:
            print('Invalid date type received')
            dateType = input('Would you like to find items for day/month/year (D/M/Y): ')

        date = input(f'Enter date to check max cost ({self.dateFormat[dateType.upper()]}): ')
        while not self.is_valid_date(date,dateType.upper()):
            print('Enter valid date')
            date = input(f'Enter date to find items ({self.dateFormat[dateType.upper()]}): ')

        self.table.checkItems(date,dateType.upper())


    def drop(self):
        if self.table.readPath != None and self.table.readPath.endswith('.csv'):
            os.remove(self.table.readPath)
        else:
            print('Invalid path')

    def analyzeItem(self):
        analyze = input(' Would You like to analyze month or year (M/Y): ')
        if analyze not in ['M','Y','m','y']:
            print('Enter valid input')
            analyze = input(' Would You like to analyze month or year (M/Y): ')

    
        date = input(f'Enter date to analyze ({self.dateFormat[analyze.upper()]}): ')
        while not self.is_valid_date(date,analyze.upper()):
            print('Enter valid date')
            date = input(f'Enter date to analyze ({self.dateFormat[analyze.upper()]}): ')

        self.table.analyzeCost(date,analyze.upper())

    def maxCost(self):
        
        dateType = input('Would you like to check max cost for day/month/year (D/M/Y): ')
        while dateType.upper() not in ['D','M','Y']:
            print('Invalid date type received')
            dateType = input('Would you like to check max cost for day/month/year (D/M/Y): ')

        date = input(f'Enter date to check max cost ({self.dateFormat[dateType.upper()]}): ')
        while not self.is_valid_date(date,dateType.upper()):
            print('Enter valid date')
            date = input(f'Enter date to check max cost ({self.dateFormat[dateType.upper()]}): ')

        self.table.findMaxCost(date,dateType.upper())

            

    def totalCost(self):
        dateType = input('Would you like to check total cost for day/month/year (D/M/Y): ')
        while type(dateType) == str and dateType.upper() not in ['D','M','Y']:
            print('Invalid date type received')
            dateType = input('Would you like to check total cost for day/month/year (D/M/Y): ')



        date = input(f'Enter date to check total cost ({self.dateFormat[dateType.upper()]}): ')
        while not self.is_valid_date(date,dateType.upper()):
            print('Enter valid date')
            date = input(f'Enter date to check total cost ({self.dateFormat[dateType.upper()]}): ')

        verbose = input('Would you like output all items purchased on date/range (Y/N) :')
        while type(verbose) == str and verbose.upper() not in ['Y','N']:
            print('Invalid input')
            verbose = input('Would you like output all items purchased on date/range (Y/N) :')

        print(f'Total cost for {date} is ${self.table.findTotalCost(date,dateType.upper(),0 if verbose.upper() == "N" else 1)}')
        

        
        
def main(helper,path):
    if helper == None:
        return
    if path == '':
        print('Proceeding to generate table..........')
        helper.addItem()
    print()
    print('What would you like to do today?')
    helper.optionPrinter()
    

    
    while True:
        if helper.length() == 0:
            print('Nothing left in dataframe. Proceeding to drop table..........')
            helper.drop()
            break

        option = input('Choose option: ')
        if option == '1':
            print('Adding item......')
            helper.addItem()
            
        elif option == '2':
            print('Deleting item......')
            helper.deleteRecord()

        elif option == '3':
            print('Finding item.....')
            helper.findItemOnDate()

        elif option == '4':
            print('Finding max cost......')
            helper.maxCost()

        elif option == '5':
            print('Finding total cost......')
            helper.totalCost()            

        elif option == '6':
            print('Analyzing cost......')
            helper.analyzeItem()
         
        elif option == '7':
            print('Are you sure?')
            cfm = input('Type in \"DELETE\" to confirm deletion of table: ')
            if cfm == 'DELETE':
                print('Dropping table.......')
                helper.drop()
                break

        elif option == '8':
            print('Have a nice day')
            break
        elif option == '9':
            helper.optionPrinter()

        elif option == '10':
            print(helper.table.table)
        else:
            print('Invalid option')

    


def initialise():
    print('---------Welcome to Finance Tracker------------')
    path = input("Input Path for table (.csv) [Press Enter if making new table]: ")
    if path == '':
        table = FinanceTable()
    elif path.endswith('.csv'):
        table = FinanceTable(path)
    else:
        print('Invalid Path')
        return(None,None)
    
    helper = MainHelper(table)
    return (helper,path)
            


if __name__ == '__main__':
    main(*initialise())

    



   
   
    
