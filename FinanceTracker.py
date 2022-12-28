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
            pass
        else:
            self.table = self.loadTable(path)
        self.readPath = path

    def loadTable(self,path):
        return pd.read_csv(path)

    def writeTable(self,writePath,changes):
        if self.readPath == None:
            self.table = pd.DataFrame(changes,columns = ['item','cost','date','remarks'])
            self.table.to_csv(writePath)
        else:
            self.table.concat(pd.DataFrame(changes),0)
            self.table.to_csv(writePath)
            
    def findmaxCost(self,date):
        '''
        Finds maximum cost in table, and which YY-MM-DD it was
        Date can be set to find max cost on date

        Returns None
        -------
        max cost

        '''
        if type(self.table) == pd.DataFrame:
            if date != 'None':
                nWords = len(date)
                itemsOnDate = self.table.loc[self.table['date'][nWords] == date]
            else:
                itemsOnDate = self.table
                
            maxCostRow = itemsOnDate.loc['cost' == itemsOnDate.max(0)['cost']]
                
                
            cost = maxCostRow['cost']
            date = maxCostRow['date']
            item = maxCostRow['item']
            print('---------Returning item with max cost-------------')
            print(f'{item} bought on {date} had max cost of {cost}')
        else:
            print('Invalid DataType, Generate table first!')
            
    def findDateCost(self,date,verbose = 0):#Takes specific day of month and year as input, finds cost in day
        if type(self.table) == pd.DataFrame:
            nWords = len(date)
            itemsOnDate = self.table.loc[self.table['date'][nWords] == date]
            if verbose:
                print(itemsOnDate.loc[:,itemsOnDate.columns != 'date'])
            return itemsOnDate['cost'].sum()
        
    def avgCost(self,date):
        if type(self.table) == pd.DataFrame:
            nWords = len(date)
            itemsOnDate = self.table.loc[self.table['date'][nWords] == date]
            return itemsOnDate['cost'].mean()
        
    def analyzeCost(): #Prints a line graph, with date as X and spendings as Y, draws average cost line
        
            
        
        


def is_valid_date(date):
    try:
        datetime.datetime.strptime(date,'%m-%d')
    except ValueError:
        return  False
    return True

def save(table,changes):
    save = input('Would you like to save changes[Y/N]: ')
    while save not in ['Y','N','y','n']:
        print('Valid answer required')
        save = input('Would you like to save changes[Y/N]: ')
    if save in ['y','Y']:
        if table.readPath != None:
            ow = input('Would you like to save changes into same file[Y/N]: ')
            while ow not in ['Y','N','y','n']:
                print('Valid answer required')
                ow = input('Would you like to save changes into same file[Y/N]: ')
            if ow in ['y','Y']:
                table.writeTable(table.readPath,changes)
            
        if table.readPath == None or ow in ['n','N']:
            path = input('Input path to write to: ')
            table.writeTable(path,changes)

            
    
    
def askhelper():
    changes = []
    while True:
        item = input('What was the item you bought: ')
        cost = input('How much did it cost: ')

        #Simple check for valid cost
        costcheck = [str(i) for i in range(10)]+['.']
        while list(filter(lambda x: x not in costcheck,list(cost))):
            cost = input('Please enter cost again: ')
        

        date = input('When did you buy it (YY-MM-DD): ')
        while not is_valid_date(date):
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
            
            
        
    
            


if __name__ == '__main__':
    path = input("Input Path for table (.csv): ")
    if path == '':
        table = FinanceTable()
    else:
        table = FinanceTable(path)
    changes = askhelper()
    save(table,changes)
        
    
