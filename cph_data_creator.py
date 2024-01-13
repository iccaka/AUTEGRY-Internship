from datetime import datetime
import pandas as pd


class CPHDataCreator:

    def __init__(self, date, df):
        self.date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        self.data_frame = df

    def generate_new_cols(self):
        for index in self.data_frame.index:
            if self.date >= datetime.strptime(self.data_frame.loc[index, 'date'], '%Y-%m-%d %H:%M:%S'):
                self.generate_act_ina_install_revolv_credits_count(index)

            self.generate_act_paid_amount(index)

        self.generate_act_ina_credits_count()

    def generate_act_ina_install_revolv_credits_count(self, index):
        matching_rows = self.data_frame.loc[
            (self.data_frame['account_id'] == self.data_frame.loc[index, 'account_id'])
            & (self.data_frame['contract_id'] != self.data_frame.loc[index, 'contract_id'])
        ]

        self.data_frame.at[index, 'cph_act_credits_count_install'] = len(matching_rows[
            (matching_rows['credit_type'] == 'install')
            & (matching_rows['status'] == 'active')
        ])
        self.data_frame.at[index, 'cph_act_credits_count_revolv'] = len(matching_rows[
            (matching_rows['credit_type'] == 'install')
            & (matching_rows['status'] == 'paid')
        ])
        self.data_frame.at[index, 'cph_ina_credits_count_install'] = len(matching_rows[
            (matching_rows['credit_type'] == 'revolve')
            & (matching_rows['status'] == 'active')
        ])
        self.data_frame.at[index, 'cph_ina_credits_count_revolv'] = len(matching_rows[
            (matching_rows['credit_type'] == 'revolve')
            & (matching_rows['status'] == 'paid')
        ])

    def generate_act_ina_credits_count(self):
        self.data_frame['cph_act_credits_count'] = \
            self.data_frame['cph_act_credits_count_install'] + \
            self.data_frame['cph_act_credits_count_revolv']

        self.data_frame['cph_ina_credits_count'] = \
            self.data_frame['cph_ina_credits_count_install'] + \
            self.data_frame['cph_act_credits_count_revolv']

    def generate_act_paid_amount(self, index):
        count = 0
        index_date = datetime.strptime(self.data_frame.loc[index, 'date'], '%Y-%m-%d %H:%M:%S')

        matching_rows = self.data_frame.loc[
            (self.data_frame['account_id'] == self.data_frame.loc[index, 'account_id'])
            & (self.data_frame['contract_id'] != self.data_frame.loc[index, 'contract_id'])
            & (self.data_frame['status'] == 'active')
            & (pd.to_datetime(self.data_frame['date']) < index_date),
            'payment'
        ]

        for x in matching_rows:
            for y in x:
                if pd.to_datetime(y) < index_date:
                    count += x[y]
                else:
                    break

        self.data_frame.at[index, 'cph_act_paid_amount'] = count
