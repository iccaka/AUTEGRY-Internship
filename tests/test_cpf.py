import unittest
import cpf_data_creator as cpf_creator


class TestCPF(unittest.TestCase):
    test_data = {
        '1': {}
    }
    DEFAULT_INTEREST_PERCENTAGE = 10
    DEFAULT_M = 4

    def setUp(self):
        self.cpfdc = cpf_creator.CPFDataCreator(self.DEFAULT_M, self.test_data)
        self.cpfdc.generate_new_cols()
        self.result = self.cpfdc.data_frame

    def test_generate_req_bad_contract(self):
        self.assertEqual(self.result.loc[0, 'cpf_req_bad_contract_N0M'], False)
        self.assertEqual(self.result.loc[0, 'cpf_req_bad_contract_N1M'], False)
        self.assertEqual(self.result.loc[0, 'cpf_req_bad_contract_N2M'], False)
        self.assertEqual(self.result.loc[0, 'cpf_req_bad_contract_N3M'], False)

    def test_generate_req_overdue_period(self):
        self.assertEqual(self.result.loc[0, 'cpf_req_overdue_period_M0'], False)
        self.assertEqual(self.result.loc[0, 'cpf_req_overdue_period_M1'], False)
        self.assertEqual(self.result.loc[0, 'cpf_req_overdue_period_M2'], False)
        self.assertEqual(self.result.loc[0, 'cpf_req_overdue_period_M3'], False)
        self.assertEqual(self.result.loc[0, 'cpf_req_overdue_period_M4'], False)
        self.assertEqual(self.result.loc[0, 'cpf_req_overdue_period_M5'], False)
        self.assertEqual(self.result.loc[0, 'cpf_req_overdue_period_M6'], False)

    def test_generate_req_max_overdue_periods(self):
        self.assertEqual(self.result.loc[0, 'cpf_req_max_overdue_periods_N0M'], 0)
        self.assertEqual(self.result.loc[0, 'cpf_req_max_overdue_periods_N1M'], 0)
        self.assertEqual(self.result.loc[0, 'cpf_req_max_overdue_periods_N2M'], 0)
        self.assertEqual(self.result.loc[0, 'cpf_req_max_overdue_periods_N3M'], 0)

    def test_generate_req_sum_service_count(self):
        self.assertEqual(self.result.loc[0, 'cpf_req_sum_service_count_N0M'], 1)
        self.assertEqual(self.result.loc[0, 'cpf_req_sum_service_count_N1M'], 1)
        self.assertEqual(self.result.loc[0, 'cpf_req_sum_service_count_N2M'], 2)
        self.assertEqual(self.result.loc[0, 'cpf_req_sum_service_count_N3M'], 3)

    def test_generate_cst_bad_contract(self):
        self.assertEqual(self.result.loc[0, 'cpf_cst_bad_contract_N0M'], False)
        self.assertEqual(self.result.loc[0, 'cpf_cst_bad_contract_N0M'], False)
        self.assertEqual(self.result.loc[0, 'cpf_cst_bad_contract_N0M'], False)
        self.assertEqual(self.result.loc[0, 'cpf_cst_bad_contract_N0M'], False)

    def test_generate_cst_overdue_period(self):
        self.assertEqual(self.result.loc[0, 'cpf_cst_overdue_period_M0'], False)
        self.assertEqual(self.result.loc[0, 'cpf_cst_overdue_period_M0'], False)
        self.assertEqual(self.result.loc[0, 'cpf_cst_overdue_period_M0'], False)
        self.assertEqual(self.result.loc[0, 'cpf_cst_overdue_period_M0'], False)

    def test_generate_cst_max_overdue_periods(self):
        self.assertEqual(self.result.loc[0, 'cpf_cst_max_overdue_periods_N0M'], 0)
        self.assertEqual(self.result.loc[0, 'cpf_cst_max_overdue_periods_N1M'], 0)
        self.assertEqual(self.result.loc[0, 'cpf_cst_max_overdue_periods_N2M'], 0)
        self.assertEqual(self.result.loc[0, 'cpf_cst_max_overdue_periods_N3M'], 0)

    def test_generate_cst_sum_service_periods(self):
        self.assertEqual(self.result.loc[0, 'cpf_cst_sum_service_periods_N0M'], 1)
        self.assertEqual(self.result.loc[0, 'cpf_cst_sum_service_periods_N1M'], 1)
        self.assertEqual(self.result.loc[0, 'cpf_cst_sum_service_periods_N2M'], 2)
        self.assertEqual(self.result.loc[0, 'cpf_cst_sum_service_periods_N3M'], 3)

    def test_generate_cst_paid_amount(self):
        self.assertEqual(self.result.loc[0, 'cpf_cst_paid_amount_M0'], 18)
        self.assertEqual(self.result.loc[0, 'cpf_cst_paid_amount_M1'], 280.8)
        self.assertEqual(self.result.loc[0, 'cpf_cst_paid_amount_M2'], 93.60000000000001)
        self.assertEqual(self.result.loc[0, 'cpf_cst_paid_amount_M3'], 187.20000000000002)

    def test_generate_cst_sum_paid_amount(self):
        self.assertEqual(self.result.loc[0, 'cpf_cst_sum_paid_amount_N0M'], 18)
        self.assertEqual(self.result.loc[0, 'cpf_cst_sum_paid_amount_N1M'], 298.8)
        self.assertEqual(self.result.loc[0, 'cpf_cst_sum_paid_amount_N2M'], 392.40000000000003)
        self.assertEqual(self.result.loc[0, 'cpf_cst_sum_paid_amount_N3M'], 579.6)
