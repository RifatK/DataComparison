

from optparse import OptionParser
import sys
import pandas as pd
from collections import OrderedDict
from functools import wraps
import math

_INPUT_FILE_DAY_1='day_1_snap.csv'
_INPUT_FILE_DAY_2='day_2_snap.csv'
_file_headers=['ticker','open','bid','ask','prim_volume','tradable_med_volume_21','volat_21','mkt_cap']
_result_headers=['Column','Field','day_1_stats','day_2_stats','diff_day_1_vs_day2','diff_day_1_vs_day_2(%)']
_RESULT_FILE='output_fmt[1].txt'

def argParser():
   parser = OptionParser(description="Report Analysis from Two days of Data")
   parser.add_option('-c', '--columns', default="",
                     help='type of column: ticker  open  bid  ask  prim_volume  tradable_med_volume_21  volat_21  mkt_cap')

   (co, ca) = parser.parse_args()

   columns = co.columns.split(",")
   return columns

def load_files_to_dataframe(file_name):
    data_set = None
    try:
        data_set= pd.read_csv(file_name,header=True, names=_file_headers)
    except  IOError:
        print("File : %s not found " % file_name)
    finally:
        return data_set

def exceptionHandler(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception, ex:
                #raise
                return False
    return wrapper


def write_results_to_file(dataList,file_name,result_headers):
    data = pd.DataFrame(dataList,columns=result_headers)
    data.to_csv(file_name, sep='\t',index=False)



class DataComparison(object):

    def __init__(self,column,dataSetDay1,dataSetDay2,index_column='ticker'):
        self.index_column = index_column
        self.column= column
        self.dataSetDay1 = dataSetDay1
        self.dataSetDay2=dataSetDay2

        self.comparisonReport = []
        self.line_seperator="--"
        self.build_pandas_data()
        self.build_functions_map()

    def build_functions_map(self):
        self.median_functions_map= OrderedDict([
            ('median_total_value',self.get_median_value)
            ,('median_non_zero_value',self.get_median_nonzero)
            ,('median_pos_value',self.get_median_postive)
            ,('median_neg_value', self.get_median_negative)])

        self.mean_functions_map= OrderedDict([
            ('mean_total_value',self.get_mean_value)
            ,('mean_non_zero_value',self.get_mean_nonzero)
            ,('mean_pos_value',self.get_mean_postive)
            ,('mean_neg_value', self.get_mean_postive)])

        self.fluctuations_functions_map= OrderedDict([
            ('pos_to_neg',self.get_pos_to_negative_count)
            ,('neg_to_pos',self.get_negative_to_pos_count)
            ,('stayed_pos',self.get_stayed_positive_count)
            ,('stayed_neg', self.get_stayed_negative_count)])

        self.summary_functions_map= OrderedDict([
            ('non_zero_count',self.get_non_zero_count)
            ,('zero_count',self.get_zero_count)
            ,('pos_count',self.get_pos_count)
            ,('neg_count', self.get_neg_count)])


    def build_pandas_data(self):
        self.super_set = self._build_join_sets(self.dataSetDay1,self.dataSetDay2)
        self.x_col= "_".join([self.column,'x'])
        self.y_col= "_".join([self.column,'y'])


    def _build_join_sets(self,dataSetDay1,dataSetDay2):
        return  pd.merge(dataSetDay1,dataSetDay2,on=self.index_column,how='inner')


    def generate_comparison_report(self):
        if self.generate_summary_data():
            print("successfully generated summary data")
        else:
            print("Error occured in generating summary data")
            return None

        if self.generate_fluctuation_data():
            print("successfully generated fluctuation data")
        else:
            print("Error occured in generating fluctuation data")
            return None

        if self.generate_mean_data():
            print("successfully generated mean data")
        else:
            print("Error occured in generating mean data")
            return None

        if self.generate_median_data():
             print("successfully generated median data")
        else:
            print("Error occured in generating median data")
            return None

        return self.comparisonReport

    @exceptionHandler
    def generate_median_data(self):

       for field,function in  self.median_functions_map.iteritems():
            day_1_var =function(self.column,self.dataSetDay1)
            day_2_var =function(self.column,self.dataSetDay2)
            self.comparisonReport.append([self.column,field,day_1_var ,day_2_var ,self.get_diff_count(day_1_var,day_2_var),self.get_percentage_diff(day_1_var,day_2_var)])
       return True

    @exceptionHandler
    def generate_mean_data(self):

        for field,function in  self.mean_functions_map.iteritems():
            day_1_var =function(self.column,self.dataSetDay1)
            day_2_var =function(self.column,self.dataSetDay2)
            self.comparisonReport.append([self.column,field,day_1_var ,day_2_var ,self.get_diff_count(day_1_var,day_2_var),self.get_percentage_diff(day_1_var,day_2_var)])

        self.add_section_seperator()
        return True

    @exceptionHandler
    def generate_fluctuation_data(self):

        for field,function in  self.fluctuations_functions_map.iteritems():
            day_1_var =function(self.x_col,self.y_col,self.super_set)
            day_2_var =function(self.y_col,self.x_col,self.super_set)
            self.comparisonReport.append([self.column,field,day_1_var ,day_2_var ,self.get_diff_count(day_1_var,day_2_var),self.get_percentage_diff(day_1_var,day_2_var)])


        self.add_section_seperator()
        return True

    @exceptionHandler
    def generate_summary_data(self):

        #total_count exception to the rule
        day_1_var =self.get_total_count(self.dataSetDay1)
        day_2_var =self.get_total_count(self.dataSetDay2)
        self.comparisonReport.append([self.column,'total_count',day_1_var ,day_2_var ,self.get_diff_count(day_1_var,day_2_var),self.get_percentage_diff(day_1_var,day_2_var)])

        for field,function in  self.summary_functions_map.iteritems():
            day_1_var =function(self.column,self.dataSetDay1)
            day_2_var =function(self.column,self.dataSetDay2)
            self.comparisonReport.append([self.column,field,day_1_var ,day_2_var ,self.get_diff_count(day_1_var,day_2_var),self.get_percentage_diff(day_1_var,day_2_var)])

        self.add_section_seperator()
        return True


    ## Helper Functions

    def get_diff_count(self,num1,num2):
        return self.is_nan_check(num1-num2)


    def get_percentage_diff(self,num1,num2):
        dflt_val= "0%"
        if num1 == 0 and num2 == 0:
           return dflt_val
        try:
           num1,num2=abs(num1),abs(num2)
           if num1== 0: return "100%"
           percentage = self.is_nan_check(((num2-num1)/num1) * 100)
           return "".join([str(round(percentage,2)),"%"])
        except ZeroDivisionError:
           return dflt_val

    # Summary set

    def add_section_seperator(self):
        self.comparisonReport.append([self.column,self.line_seperator])

    def get_total_count(self,data):
        return len(data.index)

    def get_non_zero_count(self,column,data):
        return len(data[data[column] != 0])

    def get_zero_count(self,column,data):
        return len(data[data[column] == 0])

    def get_pos_count(self,column,data):
        return len(data[data[column] > 0])

    def get_neg_count(self,column,data):
        return len(data[data[column] < 0])

    #Fluctuations
    def get_pos_to_negative_count(self,x_col,y_col,data):
        return self.is_nan_check(len(data[(data[x_col] > 0) & (data[y_col] < 0)]))

    def get_negative_to_pos_count(self,x_col,y_col,data):
        return self.is_nan_check(len(data[(data[x_col] < 0) & (data[y_col] > 0)]))

    def get_stayed_positive_count(self,x_col,y_col,data):
        return self.is_nan_check(len(data[(data[x_col] > 0) & (data[y_col] > 0)]))

    def get_stayed_negative_count(self,x_col,y_col,data):
        return self.is_nan_check(len(data[(data[x_col] < 0) & (data[y_col] < 0)]))

    # Mean Functions
    def get_mean_value(self,column,data):
        return self.is_nan_check(data[column].mean())

    def get_mean_nonzero(self,column,data):
        return self.is_nan_check(data[data[column] != 0][column].mean())

    def get_mean_postive(self,column,data):
        return self.is_nan_check(data[data[column] > 0][column].mean())

    def get_mean_negative(self,column,data):
        return self.is_nan_check(data[data[column] < 0][column].mean())

    # Median Functions
    def get_median_value(self,column,data):
        return self.is_nan_check(data[column].median())

    def get_median_nonzero(self,column,data):
        return self.is_nan_check(data[data[column] != 0][column].median())

    def get_median_postive(self,column,data):
        return self.is_nan_check(data[data[column] > 0][column].median())

    def get_median_negative(self,column,data):
        return self.is_nan_check(data[data[column] < 0][column].median())

    def is_nan_check(self,val):
        return 0 if math.isnan(val) else val

def dataIsValid(column,day1,day2):
    isValid = True
    message=""
    if day1 is None or day1.empty :
        isValid = False
        message+="Day1 data is invalid "

    if day2 is None or day2.empty :
        isValid = False
        message+="Day2 data is invalid "

    if column  not in _file_headers:
        isValid = False
        message+="invalid Columns"

    return isValid,message


def main():
    list_of_columns=argParser() # returning list on purpose incase we want to process more columns in the future
    column =list_of_columns[0]
    day1 = load_files_to_dataframe(_INPUT_FILE_DAY_1)
    day2 = load_files_to_dataframe(_INPUT_FILE_DAY_2)

    valid,message= dataIsValid(column,day1,day2)
    if not valid:
        print(message)
        exit(0)


    showStatus=DataComparison(column,day1,day2)
    compairsonReport = showStatus.generate_comparison_report()
    if compairsonReport :
        print("Writing results to file %s" % _RESULT_FILE)
        write_results_to_file(compairsonReport ,_RESULT_FILE,_result_headers)
    else:
        print("Error occured while processing Comparison Report")

if __name__ == "__main__":
    sys.exit(main())
