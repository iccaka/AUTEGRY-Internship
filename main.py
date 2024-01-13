import config_reader as reader
import io_manager
import output_data_creator as odc_creator
import cpf_data_creator as cpf_creator
import cph_data_creator as cph_creator
import rrfm
import ca
import matplotlib.pyplot as plt


if __name__ == '__main__':
    cr = reader.ConfigReader()
    data = io_manager.read_json(cr.input_file)

    odc = odc_creator.OutputDataCreator(cr.interest_percentage, data)
    odc.generate_new_cols()

    cpfdc = cpf_creator.CPFDataCreator(cr.m, odc.data)
    cpfdc.generate_new_cols()

    cphdc = cph_creator.CPHDataCreator(cr.date, cpfdc.data_frame)
    cphdc.generate_new_cols()

    rrfm_df_init = io_manager.read_csv(cr.rrfm_file)
    rrfm_df_init = rrfm_df_init.rename(columns={
        'days_from_last_payment': 'recency',
        'approved_count': 'frequency',
        'amount_paid': 'monetary_value',
        'max_overdue_days': 'risk_score'})

    # q_df ---> 'quantiles' data frame
    q_df = rrfm_df_init.loc[:, ['risk_score', 'recency', 'frequency', 'monetary_value']]

    rrfm = rrfm.RRFM(q_df.copy(), cr.quantiles)
    rrfm.generate_rrfm_codes()
    rrfm.quantile()
    rrfm.segment()
    rrfm_anova_df = rrfm.perform_anova()
    print(rrfm_anova_df)

    rfm_seg_val_count = rrfm.df['RFM_segment'].value_counts()
    rfm_seg_val_count.plot(kind='barh')
    plt.tight_layout()
    plt.show()

    ca = ca.CA(q_df, cr.k, cr.elbow_iter, cr.silhouette_iter)
    ca.elbow()
    ca.k_means_results()
    ca.silhouette()
