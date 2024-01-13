from datetime import datetime
from dateutil.relativedelta import *


class OutputDataCreator:

    def __init__(self, interest_percentage, data):
        self.interest_percentage = interest_percentage
        self.data = data

    def generate_new_cols(self):
        self.exp_cum_payment_addition()
        self.exp_cum_paid_principal_addition()
        self.payment_addition()
        self.cum_payment_addition()
        self.paid_principal_addition()
        self.cum_paid_principal_addition()
        self.overdue_amt_addition()
        self.overdue_principal_addition()

    def exp_cum_payment_addition(self):
        for x in self.data:
            record = self.data[x]

            if 'exp_cum_payment' not in record:
                date = record['date']
                installment = record['installment']
                amount = record['amount']
                period = record['period']
                credit_type = record['credit_type']
                perform_len = len(record['perform'])
                starting_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                exp_cum_payment = {}
                cum_amount = 0
                months_difference = self.__calculate_months_difference(starting_date, period)

                if self.__is_nan(installment):
                    installment = self.__calculate_installment(
                        amount,
                        period,
                        credit_type,
                        months_difference
                    )
                    record['installment'] = installment

                if credit_type == 'revolv' and months_difference > 0:
                    exp_cum_payment[starting_date.strftime('%Y-%m')] = cum_amount
                else:
                    exp_cum_payment[starting_date.strftime('%Y-%m')] = 0

                for y in range(perform_len - 1):
                    starting_date = starting_date + relativedelta(months=1)

                    if cum_amount < amount:
                        cum_amount += installment

                    exp_cum_payment[starting_date.strftime('%Y-%m')] = cum_amount

                record['exp_cum_payment'] = exp_cum_payment

    def exp_cum_paid_principal_addition(self):
        for x in self.data:
            record = self.data[x]

            if 'exp_cum_paid_principal' not in record:
                installment = record['installment']
                perform_len = len(record['perform'])
                principal = installment - (record['amount'] * self.interest_percentage / 100)
                exp_cum_paid_principal = {}
                starting_date = datetime.strptime(record['date'], '%Y-%m-%d %H:%M:%S')
                exp_cum_paid_principal[starting_date.strftime('%Y-%m')] = 0

                for y in range(perform_len - 1):
                    starting_date = starting_date + relativedelta(months=1)

                    if principal < 0:
                        principal += installment
                    else:
                        exp_cum_paid_principal[starting_date.strftime('%Y-%m')] = principal
                        continue

                    exp_cum_paid_principal[starting_date.strftime('%Y-%m')] = 0

                record['exp_cum_paid_principal'] = exp_cum_paid_principal

    def payment_addition(self):
        for x in self.data:
            record = self.data[x]

            if 'payment' not in self.data:
                installment = record['installment']
                perform = record['perform']
                payment = {}
                last_month = ''

                for y in perform:
                    if perform[y] >= 0:
                        payment[y] = installment * perform[y]
                    else:
                        if record['credit_type'] == 'revolv':
                            payment[y] = installment - self.__sum_to(last_month, payment)
                        else:
                            payment[y] = (installment * record['period']) - self.__sum_to(last_month, payment)

                    last_month = y

                record['payment'] = payment

    def cum_payment_addition(self):
        for x in self.data:
            record = self.data[x]

            if 'cum_payment' not in self.data:
                payment = record['payment']
                cum_amount = 0
                cum_payment = {}

                for y in payment:
                    cum_amount += payment[y]
                    cum_payment[y] = cum_amount

                record['cum_payment'] = cum_payment

    def paid_principal_addition(self):
        for x in self.data:
            record = self.data[x]

            if 'paid_principal' not in record:
                amount = record['amount']
                perform = record['perform']
                installment = record['installment']
                interest = amount * self.interest_percentage / 100
                cum_principals_amount = 0
                is_interest_paid = False
                paid_principal = {}

                for y in perform:
                    if perform[y] == -1:
                        paid_principal[y] = amount - cum_principals_amount
                    elif perform[y] == 0:
                        paid_principal[y] = 0
                    else:
                        if not is_interest_paid:
                            is_interest_paid = True
                            principal = (perform[y] * installment) - interest
                        else:
                            principal = perform[y] * installment

                        paid_principal[y] = principal
                        cum_principals_amount += principal

                record['paid_principal'] = paid_principal

    def cum_paid_principal_addition(self):
        for x in self.data:
            record = self.data[x]

            if 'cum_paid_principal' not in self.data:
                paid_principal = record['paid_principal']
                cum_amount = 0
                cum_paid_principal = {}

                for y in paid_principal:
                    cum_amount += paid_principal[y]
                    cum_paid_principal[y] = cum_amount

                record['cum_paid_principal'] = cum_paid_principal

    def overdue_amt_addition(self):
        for x in self.data:
            record = self.data[x]

            if 'overdue_amt' not in self.data:
                exp_cum_payment = record['exp_cum_payment']
                cum_payment = record['cum_payment']
                overdue_amt = {}

                for y in exp_cum_payment:
                    if y in cum_payment and y in exp_cum_payment:
                        overdue_amt[y] = exp_cum_payment[y] - cum_payment[y]
                    else:
                        overdue_amt[y] = 0

                record['overdue_amt'] = overdue_amt

    def overdue_principal_addition(self):
        for x in self.data:
            record = self.data[x]

            if 'overdue_principal' not in record:
                exp_cum_paid_principal = record['exp_cum_paid_principal']
                cum_paid_principal = record['cum_paid_principal']
                overdue_principal = {}

                for y in exp_cum_paid_principal:
                    if y in cum_paid_principal and y in exp_cum_paid_principal:
                        overdue_principal[y] = exp_cum_paid_principal[y] - cum_paid_principal[y]
                    else:
                        overdue_principal[y] = 0

                record['overdue_principal'] = overdue_principal

    def __calculate_installment(self, amount, period, credit_type, months_difference):
        if credit_type == "install":
            return amount * (1 + (self.interest_percentage / 100)) / period

        if months_difference == 0:
            return amount * (1 + (self.interest_percentage / 100))

        return amount * (1 + (self.interest_percentage / 100)) / months_difference

    def __calculate_months_difference(self, starting_date: datetime, period):
        ending_date = starting_date + relativedelta(days=period)
        return (ending_date.year - starting_date.year) * 12 + (ending_date.month - starting_date.month)

    def __is_nan(self, n):
        return n != n

    def __sum_to(self, month, data):
        result = 0

        for x in data:
            if month != x:
                result += data[x]
                continue

            break

        return result
