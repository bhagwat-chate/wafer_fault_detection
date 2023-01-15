import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
from file_operations import file_methods
from wafer.logger import logging
from wafer.exception import WaferException
import sys, os
class KMeansClustering:

    def __init__(self):
        pass

    def elbow_plot(self, data):

        wcss=[]
        try:
            for i in range(1, 11):
                kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
                kmeans.fit(data)
                wcss.append(kmeans.inertia_)
            plt.plot(range(1, 11), wcss)
            plt.title('Elbow Method')
            plt.xlabel('Number of clusters')
            plt.ylabel('WCSS')
            plt.savefig("wafer/core_ml/data_preprocessing/elbow_plot.PNG")
            self.kn = KneeLocator(range(1, 11), wcss, curve='convex', direction='decreasing')
            logging.info("The Elbow method plot saved")

            return self.kn.knee
        
        except WaferException as e:
            raise WaferException(e, sys)

    def create_clusters(self, data, number_of_clusters):
        try:
            self.data = data
            self.kmeans = KMeans(n_clusters=number_of_clusters, init='k-means++', random_state=42)
            self.y_means = self.kmeans.fit_predict(data)
            self.file_op = file_methods.File_Operation()
            self.save_model = self.file_op.save_model(self.kmeans, 'KMeans')

            self.data['Cluster']=self.y_kmeans

        except WaferException as e:
            raise WaferException(e, sys)