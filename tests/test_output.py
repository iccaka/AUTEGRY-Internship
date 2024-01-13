import unittest
import output_data_creator as creator


class TestOutput(unittest.TestCase):
    test_data = {
        '1': {}
    }
    DEFAULT_INTEREST_PERCENTAGE = 10

    def setUp(self):
        self.odc = creator.OutputDataCreator(self.DEFAULT_INTEREST_PERCENTAGE, self.test_data)
        self.odc.generate_new_cols()
        self.result = self.odc.data

    def test_exp_cum_payment_addition(self):
        self.assertEqual(self.result['1']['exp_cum_payment'], {
            '2019-01': 0,
            '2019-02': 55,
            '2019-03': 110,
            '2019-04': 165,
            '2019-05': 220,
            '2019-06': 220,
            '2019-07': 220
        })

    def test_exp_cum_paid_principal_addition(self):
        self.assertEqual(self.result['1']['exp_cum_paid_principal'], {
            '2019-01': 0,
            '2019-02': 35,
            '2019-03': 90,
            '2019-04': 145,
            '2019-05': 200,
            '2019-06': 200,
            '2019-07': 200
        })

    def test_payment_addition(self):
        self.assertEqual(self.result['1']['payment'], {
            '2019-01': 0,
            '2019-02': 0,
            '2019-03': 0,
            '2019-04': 110,
            '2019-05': 66.0,
            '2019-06': 0,
            '2019-07': 44.0
        })

    def test_cum_payment_addition(self):
        self.assertEqual(self.result['1']['cum_payment'], {
            '2019-01': 0,
            '2019-02': 0,
            '2019-03': 0,
            '2019-04': 110,
            '2019-05': 176,
            '2019-06': 176,
            '2019-07': 220
        })

    def test_paid_principal_addition(self):
        self.assertEqual(self.result['1']['paid_principal'], {
            '2019-01': 0,
            '2019-02': 0,
            '2019-03': 0,
            '2019-04': 90,
            '2019-05': 66,
            '2019-06': 0,
            '2019-07': 44
        })

    def test_cum_paid_principal_addition(self):
        self.assertEqual(self.result['1']['cum_paid_principal'], {
            '2019-01': 0,
            '2019-02': 0,
            '2019-03': 0,
            '2019-04': 90,
            '2019-05': 156,
            '2019-06': 156,
            '2019-07': 200
        })

    def test_overdue_amt_addition(self):
        self.assertEqual(self.result['1']['overdue_amt'], {
            '2019-01': 0,
            '2019-02': 55,
            '2019-03': 110,
            '2019-04': 55,
            '2019-05': 44,
            '2019-06': 44,
            '2019-07': 0
        })

    def test_overdue_principal_addition(self):
        self.assertEqual(self.result['1']['overdue_principal'], {
            '2019-01': 0,
            '2019-02': 35,
            '2019-03': 90,
            '2019-04': 55,
            '2019-05': 44,
            '2019-06': 44,
            '2019-07': 0
        })
