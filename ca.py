import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd


class CA:
    def __init__(self, data, k, elbow_iter, silhouette_iter):
        self.df = data
        self.df.iloc[:, :] = StandardScaler().fit_transform(self.df.iloc[:, :])
        self.k = k
        self.elbow_iter = elbow_iter
        self.silhouette_iter = silhouette_iter

    def elbow(self):
        fig, ax = plt.subplots(2, 2)

        e_range = range(1, self.elbow_iter + 1)
        col_count = 0
        for i in range(len(ax)):
            for j in range(len(ax[i])):
                sse = []
                df_col = self.df.iloc[:, col_count]

                for k in e_range:
                    sse.append(self.k_means(df_col, k)[1])

                ax[i, j].plot(e_range, sse)
                ax[i, j].set_xticks(e_range)
                ax[i, j].set_xlabel('# of clusters')
                ax[i, j].set_ylabel('SSE')
                ax[i, j].set_title(df_col.name)
                col_count += 1

        plt.suptitle('Elbow')
        plt.subplots_adjust(wspace=0.5, hspace=0.5)
        plt.show()

    def silhouette(self):
        fig, ax = plt.subplots(2, 2)

        s_range = range(2, self.silhouette_iter + 1)
        col_count = 0
        for i in range(len(ax)):
            for j in range(len(ax[i])):
                silhouette_s = []
                df_col = self.df.iloc[:, col_count]

                for k in s_range:
                    silhouette_s.append(silhouette_score(
                        df_col.to_numpy().reshape(-1, 1),
                        self.k_means(df_col, k)[0],
                        metric='euclidean'
                    ))

                ax[i, j].plot(s_range, silhouette_s)
                ax[i, j].set_xticks(s_range)
                ax[i, j].set_xlabel('# of clusters')
                ax[i, j].set_ylabel('Silhouette score')
                ax[i, j].set_title(df_col.name)
                col_count += 1

        plt.suptitle('Silhouette')
        plt.subplots_adjust(wspace=0.5, hspace=0.5)
        plt.show()

    def k_means_results(self):
        fig, ax = plt.subplots(2, 2)
        colors = np.random.rand(self.k, 3)
        k_range = range(1, self.k + 1)

        col_count = 0
        for i in range(len(ax)):
            for j in range(len(ax[i])):
                df_col = self.df.iloc[:, col_count]
                ax[i, j].bar(k_range, pd.Series(self.k_means(df_col, self.k)[0]).value_counts(), color=colors)
                ax[i, j].set_xticks(k_range)
                ax[i, j].set_title(df_col.name)
                col_count += 1

        plt.suptitle('k-means')
        plt.subplots_adjust(wspace=0.3, hspace=0.4)
        plt.show()

    def k_means(self, col, _k):
        kmeans = KMeans(init='random', n_clusters=_k, n_init=10)
        kmeans.fit(col.to_numpy().reshape(-1, 1))
        return kmeans.labels_, kmeans.inertia_
