import pandas as pd
import matplotlib as plt

class FinanceTable():
    def __init__(self,path = None):
        if path == None:
            self.table = self.generateTable()
        else:
            self = self.loadTable(path)
        
    def self.generateTable(self):