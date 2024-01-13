import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.formula.api import ols
from segment_type import SegmentType


class RRFM:
    def __init__(self, data, quantiles):
        self.df = data
        self.quantiles = quantiles

    def generate_rrfm_codes(self):
        for x in self.df.columns:
            self.df[x] = pd.qcut(self.df[x].rank(method='first'), q=self.quantiles, labels=range(1, self.quantiles + 1))

        self.df['RFM'] = (
                self.df['recency'].astype(str) +
                self.df['frequency'].astype(str) +
                self.df['monetary_value'].astype(str)
        )

    def segment(self):
        for x in range(len(self.df.index)):
            self.df.loc[x, 'RFM_segment'] = SegmentType(self.df.loc[x, 'RFM']).name

    def quantile(self):
        fig, ax = plt.subplots(2, 2)
        colors = np.random.rand(self.quantiles, 3)
        q_range = range(1, self.quantiles + 1)
        col_count = 0

        for i in range(len(ax)):
            for j in range(len(ax[i])):
                col = self.df.iloc[:, col_count]
                ax[i, j].bar(q_range, col.value_counts(), color=colors)
                ax[i, j].set_xticks(q_range)
                ax[i, j].set_title(col.name)
                col_count += 1

        plt.suptitle('Quantiles')
        plt.subplots_adjust(wspace=0.3, hspace=0.4)
        plt.show()

    def perform_anova(self):
        anova_df = self.df[['recency', 'frequency', 'monetary_value', 'risk_score']].apply(pd.to_numeric)

        model = ols("""risk_score ~ C(recency) 
                + C(frequency) 
                + C(monetary_value) 
                + C(recency):C(frequency) 
                + C(recency):C(monetary_value) 
                + C(monetary_value):C(frequency)
                + C(recency):C(frequency):C(monetary_value)""", data=anova_df).fit()

        return sm.stats.anova_lm(model, typ=2)
