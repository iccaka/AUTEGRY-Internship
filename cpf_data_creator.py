import pandas as pd
import numpy as np


class CPFDataCreator:

    def __init__(self, m, data):
        self.m = m
        self.data_frame = self.__transform_to_df(data)

        dict_cols = self.__get_dict_cols_names()

        self.__add_m_nan_cols(dict_cols)
        self.__dict_to_m_cols(dict_cols)

    def generate_new_cols(self):
        for x in range(self.m):
            self.data_frame[f'cpf_req_bad_contract_N{x}M'] = 'NaN'
            self.data_frame[f'cpf_req_overdue_period_M{x}'] = 'NaN'
            self.data_frame[f'cpf_req_max_overdue_periods_N{x}M'] = 'NaN'
            self.data_frame[f'cpf_req_sum_service_count_N{x}M'] = 'NaN'
            self.data_frame[f'cpf_cst_bad_contract_N{x}M'] = 'NaN'
            self.data_frame[f'cpf_cst_overdue_period_M{x}'] = 'NaN'
            self.data_frame[f'cpf_cst_max_overdue_periods_N{x}M'] = 'NaN'
            self.data_frame[f'cpf_cst_sum_service_periods_N{x}M'] = 'NaN'
            self.data_frame[f'cpf_cst_paid_amount_M{x}'] = 'NaN'
            self.data_frame[f'cpf_cst_sum_paid_amount_N{x}M'] = 'NaN'

        for index in self.data_frame.index:
            self.generate_req_bad_contract(index)
            self.generate_req_overdue_period(index)
            self.generate_req_max_overdue_periods(index)
            self.generate_req_sum_service_count(index)

        for index in self.data_frame.index:
            self.generate_cst_bad_contract(index)
            self.generate_cst_overdue_period(index)
            self.generate_cst_max_overdue_periods(index)
            self.generate_cst_sum_service_periods(index)
            self.generate_cst_paid_amount(index)
            self.generate_cst_sum_paid_amount(index)

    def generate_req_bad_contract(self, index):
        row = self.data_frame.loc[index, :]
        perform_iter = iter(row['perform'].values())
        is_status_bad_ended = False

        for x in range(self.m):
            if next(perform_iter, -1 if is_status_bad_ended else 1) < 0:
                is_status_bad_ended = True if row['status'] == 'bad_ended' else False
                self.data_frame.at[index, f'cpf_req_bad_contract_N{x}M'] = True
            elif is_status_bad_ended:
                self.data_frame.at[index, f'cpf_req_bad_contract_N{x}M'] = True
            else:
                self.data_frame.at[index, f'cpf_req_bad_contract_N{x}M'] = False

    def generate_req_overdue_period(self, index):
        row = self.data_frame.loc[index, :]
        exp_cum_payment = np.array(list(row['exp_cum_payment'].values()))
        cum_payment = np.array(list(row['cum_payment'].values()))
        compare_array = exp_cum_payment > cum_payment
        self.data_frame[f'cpf_req_overdue_period_M{0}'] = False
        count = 1

        for x in compare_array:
            self.data_frame.at[index, f'cpf_req_overdue_period_M{count}'] = compare_array[count - 1]
            count += 1

    def generate_req_max_overdue_periods(self, index):
        max_count = 0
        count = max_count

        for x in range(self.m):
            curr_el = self.data_frame.loc[index, f'cpf_req_overdue_period_M{x}']

            if curr_el:
                count += 1

                if count > max_count:
                    max_count = count
            else:
                count = 0

            self.data_frame.at[index, f'cpf_req_max_overdue_periods_N{x}M'] = max_count

    def generate_req_sum_service_count(self, index):
        row = self.data_frame.loc[index, :]
        count = 0

        self.data_frame.at[index, f'cpf_req_sum_service_count_N{0}M'] = 1

        for x in range(1, self.m):
            count += 0 if row[f'cpf_req_overdue_period_M{x}'] else 1
            self.data_frame.at[index, f'cpf_req_sum_service_count_N{x}M'] = count

    def generate_cst_bad_contract(self, index):
        matching_rows = self.data_frame.loc[
            self.data_frame['account_id'] == self.data_frame.loc[index, 'account_id'],
            list(f'cpf_req_bad_contract_N{x}M' for x in range(self.m))
        ]

        for x in range(self.m):
            self.data_frame.at[index, f'cpf_cst_bad_contract_N{x}M'] = True \
                if (matching_rows[f'cpf_req_bad_contract_N{x}M']).any() else False

    def generate_cst_overdue_period(self, index):
        matching_rows = self.data_frame.loc[
            self.data_frame['account_id'] == self.data_frame.loc[index, 'account_id'],
            list(f'cpf_req_overdue_period_M{x}' for x in range(self.m))
        ]

        self.data_frame.at[index, 'cpf_cst_overdue_period_M0'] = False

        for x in range(1, self.m):
            self.data_frame.at[index, f'cpf_cst_overdue_period_M{x}'] = True \
                if (matching_rows[f'cpf_req_overdue_period_M{x}']).any() else False

    def generate_cst_max_overdue_periods(self, index):
        matching_rows = self.data_frame.loc[
            self.data_frame['account_id'] == self.data_frame.loc[index, 'account_id'],
            list(f'cpf_req_max_overdue_periods_N{x}M' for x in range(self.m))
        ]

        for x in range(self.m):
            self.data_frame.at[index, f'cpf_cst_max_overdue_periods_N{x}M'] = \
                matching_rows[f'cpf_req_max_overdue_periods_N{x}M'].max()

    def generate_cst_sum_service_periods(self, index):
        matching_rows = self.data_frame.loc[
            self.data_frame['account_id'] == self.data_frame.loc[index, 'account_id'],
            list(f'cpf_req_sum_service_count_N{x}M' for x in range(self.m))
        ]

        for x in range(self.m):
            self.data_frame.at[index, f'cpf_cst_sum_service_periods_N{x}M'] = \
                matching_rows[f'cpf_req_sum_service_count_N{x}M'].min()

    def generate_cst_paid_amount(self, index):
        matching_rows = self.data_frame.loc[
            self.data_frame['account_id'] == self.data_frame.loc[index, 'account_id'],
            list(f'payment_{x}' for x in range(self.m))
        ]

        for x in range(self.m):
            try:
                self.data_frame.at[index, f'cpf_cst_paid_amount_M{x}'] = matching_rows[f'payment_{x}'].mean()
            except TypeError:
                continue

    def generate_cst_sum_paid_amount(self, index):
        matching_rows = self.data_frame.loc[
            self.data_frame['account_id'] == self.data_frame.loc[index, 'account_id'],
            list(f'cum_payment_{x}' for x in range(self.m))
        ]

        for x in range(self.m):
            try:
                self.data_frame.at[index, f'cpf_cst_sum_paid_amount_N{x}M'] = matching_rows[f'cum_payment_{x}'].mean()
            except TypeError:
                continue

    def __transform_to_df(self, data):
        result = pd.DataFrame(data).T
        result.reset_index(inplace=True)
        result = result.rename(columns={'index': 'contract_id'})
        return result

    def __get_dict_cols_names(self):
        return [x for x in self.data_frame.columns if type(self.data_frame[f'{x}'][0]) is dict]

    def __add_m_nan_cols(self, dict_cols):
        for x in dict_cols:
            for y in range(self.m):
                self.data_frame.replace(f'{x}_{y}', np.NaN)

    def __dict_to_m_cols(self, dict_cols):
        for index in self.data_frame.index:
            for col in dict_cols:
                count = 0

                if len(self.data_frame[col][index]) <= self.m:
                    for x in self.data_frame[col][index]:
                        self.data_frame.at[index, f'{col}_{count}'] = self.data_frame[col][index][x]
                        count += 1
                else:
                    for x in self.data_frame[col][index]:
                        if count < self.m:
                            self.data_frame.at[index, f'{col}_{count}'] = self.data_frame[col][index][x]
                            count += 1

    def __del_cols(self, cols_to_del):
        self.data_frame = self.data_frame.drop(columns=cols_to_del)
