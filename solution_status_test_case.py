import unittest
import pandas as pd
from show_status import DataComparison

class DataComparisonTestCase(unittest.TestCase):


    def setUp(self):
        _file_headers=['ticker','open','bid','ask','prim_volume','tradable_med_volume_21','volat_21','mkt_cap']
        self.baseLineResults=[['prim_volume', 'total_count', 2, 2, 0, '0.0%'],
                      ['prim_volume', 'non_zero_count', 2, 2, 0, '0.0%'],
                      ['prim_volume', 'zero_count', 0, 0, 0, '0%'],
                      ['prim_volume', 'pos_count', 0, 2, -2, '100%'],
                      ['prim_volume', 'neg_count', 2, 0, 2, '-100.0%'],
                      ['prim_volume', 'pos_to_neg', 0, 2, -2, '100%'],
                      ['prim_volume', 'neg_to_pos', 2, 0, 2, '-100.0%'],
                      ['prim_volume', 'stayed_pos', 0, 0, 0, '0%'],
                      ['prim_volume', 'stayed_neg', 0, 0, 0, '0%'],
                      ['prim_volume', 'mean_total_value', -350.0, 350.0, -700.0, '0.0%'],
                      ['prim_volume', 'mean_non_zero_value', -350.0, 350.0, -700.0, '0.0%'],
                      ['prim_volume', 'mean_pos_value', 0, 350.0, -350.0, '100%'],
                      ['prim_volume', 'mean_neg_value', 0, 350.0, -350.0, '100%'],
                      ['prim_volume', 'median_total_value', -350.0, 350.0, -700.0, '0.0%'],
                      ['prim_volume', 'median_non_zero_value', -350.0, 350.0, -700.0, '0.0%'],
                      ['prim_volume', 'median_pos_value', 0, 350.0, -350.0, '100%'],
                      ['prim_volume', 'median_neg_value', -350.0, 0, -350.0, '-100.0%']]

        self.column ='prim_volume'
        self.input_data_Day1=pd.read_csv('test_day_1_snap.csv',header=True, names=_file_headers)
        self.input_data_Day2=pd.read_csv('test_day_2_snap.csv',header=True, names=_file_headers)

        self._generate_results()

    def _generate_results(self):
        comparison = DataComparison(self.column,self.input_data_Day1,self.input_data_Day1)
        self.target_results=comparison.generate_comparison_report()

    def test_results(self):
        result_headers=['Column','Field','day_1_stats','day_2_stats','diff_day_1_vs_day2','diff_day_1_vs_day_2(%)']
        baseLine=pd.DataFrame(self.baseLineResults,columns=result_headers)
        target=pd.DataFrame(self.target_results,columns=result_headers)

        #diffs = (baseLine != target).any(1)
        for i in baseLine.index:
            targetRow =  target.ix[i]
            for field in result_headers:
                baseLineVal = baseLine.ix[i][field]
                targetVal = targetRow[field]
                print "field: %s baseline: %s target : %s" % (field,baseLineVal,targetVal)
                assert baseLineVal == targetVal


if __name__ == '__main__':
    unittest.main()
