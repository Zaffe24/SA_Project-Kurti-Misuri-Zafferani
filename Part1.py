from Part2 import *
from pandas import *


'''The class Read() will read the predefined Data sets, converting them into DataFrames objects. 
It's formed by two identical methods, each for a Data set, invoked specifically by class Operations' methods.
The methods are protected because the Data sets can't be accessed neither changed to avoid malfunctioning 
 of the project, well suited for the predefined Data sets.
 '''
class Read():
    '''read_it_g() and read_it_d() are used to access the private __read_it_g() and __read_it_d().
     User is not allowed to change the predefined Datasets '''
    def read_it_g():
        return Read.__read_it_g()
    def __read_it_g():
        Gene = pandas.read_csv('gene_evidences.tsv', delimiter='\t', engine='python')
        return Gene
    def read_it_d():
        return Read.__read_it_d()
    def __read_it_d():
        Disease = pandas.read_csv('disease_evidences.tsv', delimiter='\t', engine='python')
        return Disease


''' Class Operations() is the connection between the three parts of the whole project.
It receives inputs by Part 3 in the form of objects and it invokes Part 2 through the methods oper_no() and oper_yes(),
that are dictionaries with the operation name as the key for the specific operation. 
They are divided according to the needing of a user's input or not. 
'''
class Operations():

    """ Label can be Gene or the Disease according to the Dataset chosen and it's private according to Part 3
    where the object is already available for the user;
     Filter is used for the column choice needed in some operations
    of Part 2 and my_key is the element to look for in Part 2.
    Filter and my_key are by default set to 0 and changed through methods set_filter() and set_key()"""
    def __init__(self, label, Filter=0, my_key=0):
        self.__label= label #Gene or Disease dataset
        self.Filter=Filter #column (for id=0 or symbol/name=4)
        self.my_key= my_key #element

    '''set_it() method will provide access to __set_filter() that is used to change the filter of the object.
     It is private because already given to the user that should not change it'''
    def set_it(self,new_filter):
        self.__set_filter(new_filter)
        return
    def __set_filter(self,new_filter):
        self.Filter= new_filter

    '''set_key() is used for change the element to look for in Part 2 operations'''
    def set_key(self,new_key):
        self.my_key=new_key

    '''read_it_gene() and read_it_disease() are used to have access to the Datasets'''
    def read_it_gene(self):
        return Read.read_it_g()
    def read_it_disease(self):
        return Read.read_it_d()

    '''D_set() and D_other() are used to define how the Datasets have to be used according to the label of the object.
    It invokes the read_it_gene() and read_it_disease()'''
    def D_set(self):
        if self.__label=='Gene':
            return self.read_it_gene()
        else:
            return self.read_it_disease()
    def D_other(self):
        if self.__label=='Gene':
            return self.read_it_disease()
        else:
            return self.read_it_gene()

    '''oper_no() and oper_yes() are the connections with Part 2. They are accessed with oper_No() and oper_Yes(). 
    The right usage of the datasets is defined with D_set() and D-other() invocations.
    oper_no() does not require user's input while oper_yes() yes. 
    They are divided also to lower the time of processing.
    The specificity for private methods is due to avoid user's direct interactions with the core of connection between Parts'''
    def oper_No(self,what):
        return self.__oper_no(what)
    def __oper_no(self, what):
        registry_n = {'Shape':MetaData(self.D_set()).dimensions(),'Semantics':MetaData(self.D_set()).semantics(),
                      'ID':MetaData(self.D_set()).list_names(),'Top':MetaData(self.D_set()).most_frequent(MetaData(self.D_other()))}
        return registry_n[what]
    def oper_Yes(self,what):
        return self.__oper_yes(what)
    def __oper_yes(self, what):
        registry_y = {'COVID-symbol': MetaData(self.D_set()).covid_sentence(self.Filter, self.my_key),
                      'Association': MetaData(self.D_set()).association(MetaData(self.D_other()), self.Filter, self.my_key)}
        return registry_y[what]

