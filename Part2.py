from pandas import *
from flask import *


'''Takes as parameter only one DataFrame, it represents the object on which all the operations will occur.'''
'''This class allows to create few descrete methods that can then be implemented in different ways to solve several dinstict opearations. It maintains
the software's core slim and understandable.'''

class MetaData():
    
    
    '''The only attribute passed is the data-set already converted by Part 1 in a pandas.DataFrame, it is protected because it can
    be accessed only internally the scope of the class.'''
    '''It also converts automatically the DataFrame in a numpy array thanks to the built-in function .to_numpy().'''
    
    def __init__(self, data : DataFrame): 
        self.__data=data
        self.__array = self.__data.to_numpy()
        
        
    '''The method .dimensions() solves operation 1.'''    
    '''It returns a tuple containing the dimensions of the DataFrame attribute, this operation is achieved by the invoking the
    pandas attribute .shape.'''
    
    def dimensions(self)->tuple:
        Dimensions=tuple(self.__data.shape) 
        return Dimensions
    
    
    '''The method .semantics() solves operation 2.'''    
    '''It returns a list containing the labels of the DataFrame columns, this operation is achieved by the invocking the
    pandas attribute .columns.'''
    
    def semantics(self) -> list:
        Semantics=list(self.__data.columns)  
        return Semantics
    
    
    '''The method .list_names() solves operation 3 and 5.'''
    '''It returns a list containing in ascending order the gene symbols or the disease names according to the type of object passed.'''
    
    def list_names(self)->list:
        result_1 = self.__data[self.semantics()[4]].value_counts(sort=True, ascending=True)
        return list(result_1.index)
    
    '''The method .__all_sentences() is protected since it is designed as an auxiliary function, thus it can be invoked only inside the
    class scope. It takes as parameters the index of the column (n_column), that contains the (element) parameter, and (item_index) that is
    instead the index of the column in which the item corresponding to (element) must be searched in, it is set as 1
    by default so that it can be directly implemented by the .sentence() method to detect the items in the 'sentence' column.'''
    '''If the parameter (element) is present in the column of the DataFrame with index [n_column] then the item on the same row belonging to
    the column with index equal to the parameter (item_index) will be added to a list, this allows the programmer to re-use this method for
    different purposes by changing only one parameter. The possibility of unwelcomed outcomes are taken into account and managed.  '''
    
    def __all_sentences(self, n_column, element, item_index=1)-> list or str:
        array=self.__array
        result=[]
        for item in array:
            if str(item[n_column]) == str(element):
                result.append(item[item_index])
        if len(result)>=1:
            return result
        else:
            return 'input not valid'
        
     
    '''The method .covid_sentence() solves operations 4 and 6.'''
    '''It takes the same parameters of the previous method except for (item_index) which is set by default.
    It invokes .__all_sentences() in order to obtain the complete list of sentences related to the (key), if
    the item which is a HTML sentence is directly related to COVID19 then it will be added to the new list created.
    Markup() is a module that allows to implement Markup languages. This method takes into account also the possibility
    that no correlation with COVID19 is found.'''
    
    def covid_sentence(self,n_column, key)-> list or str:
        covid_refs=[]
        slicing=self.__all_sentences(n_column, key)
        if slicing!= 'input not valid':
            for covid in slicing:
                if 'COVID19' in covid:
                    covid_refs.append(Markup(covid))
            if len(covid_refs)>=1:
                return covid_refs
            else:
                return 'no correlation found'
        else:
            return slicing
        
        
    '''It is an auxiliary method that cannot be invoked out of the internal scope of the class, it takes as parameters an instance (other)
    of the MetaData class, (number) which defines the criterium to which merge the 2 DataFrames with.
    It returns a new DataFrame created by the built-in pandas method pandas.merge(), thus it will be used by other methods to solve more
    complex analytical operations.'''
    
    def __merging(self, other, number=3)->DataFrame:
        Merge=pandas.merge(self.__data, other.__data,how='inner', on=self.semantics()[number], sort=True)
        return Merge
    
    
    '''The method .association() solves operations 8 and 9.'''
    '''It takes as parameters (other) which is the MetaData instance to merge the DataFrame with and (element) which is the item to whom
    the association is found. The protected method .__merging() is used to create the merged DataFrame in which to perform the next operation,
    the number 3 as merging criterium stands for the 'pmid' label because this enables us to find the publications that connects a certain gene
    to a certain disease and viceversa. The .__all_sentences() method is invoked on the merged DataFrame and it returns a list containing all the
    items associated to the (element) parameter which will be the only given by the user, the (item_index) parameter is fixed as 9 because it stands for the
    'gene_symbol' or 'disease_name' according to the DataFrame used to merge the instance's one with.'''
    '''Eventually a list is returned with all the gene symbols or disease names that are associated to the element passed as parameter.'''
    
    def association(self,other,n_column, element)-> list or str:
        merged=self.__merging(other)
        association_list=MetaData(merged).__all_sentences(n_column, element, item_index=9)
        if association_list!= 'input not valid':
            no_duplicates = list(set(association_list))
            return no_duplicates
        else:
            return association_list
        
        
    '''The method .most_frequent() solves operation 7.'''
    '''The only parameters taken are those needed by the protected method .__merging(), in particular (number) was set to 3 since
    it refers to the label of the ['pmid'] column that is the merging criterium, the method uses the pandas built-in function .groupby()
    to align the element-couples belonging to the columns ['gene_symbol'] and ['disease_name'] sharing the same['pmid']. Since the task
    requires to return the top 10 discrete associations, we exploit the built-in functions of Pandas .count() and .sort_values() to
    obtain a descending DataFrame. In the end the method returns a list containing the 10 most frequent discrete associations between
    genes and diseases, moreover it's irrelevant which DataFrame is chosen as self and which one as (other) because the output will be the same.'''
    
    def most_frequent(self,other, number=3)->list:
        merged=self.__merging(other, number)
        extended=MetaData(merged)
        grouped=merged.groupby([extended.semantics()[4], extended.semantics()[9]]).count()
        top10=grouped.sort_values([self.semantics()[number]], ascending=False)
        return list(top10.index)[:10]
    

