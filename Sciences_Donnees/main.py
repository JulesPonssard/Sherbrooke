
from scipy.spatial.distance import euclidean, sqeuclidean, cityblock, cosine, mahalanobis

import numpy as np
import pandas as pd
import random


dist_dict = {
    "euclidienne": euclidean,
    "euclidienne_carree": sqeuclidean,
    "manhattan": cityblock,
    "cosinus": cosine,
    "mahalanobis" : mahalanobis
}



"""
a = [1, 2]
b = [4, 6]

x = dist_dict["euclidienne"](a, b)         : 5.0
y = dist_dict["euclidienne_carree"](a, b)  : 25.0

moyennes_colonnes = np.mean(data, axis=0)  # Une moyenne par colonne
moyennes_lignes = np.mean(data, axis=1)    # Une moyenne par ligne
"""

class Methode1:
    def __init__(self, data):
        self.data = data
        # Cache commun a toutes les classes 
        self.inv_cov = None

    def _distance(self, patient, centre, mesureChoix):
        if mesureChoix == "mahalanobis":
            if self.inv_cov is None:
                self.cov = np.atleast_2d(np.cov(self.data, rowvar=False))
                # La pseudo-inverse accepte aussi une covariance singuliere.
                self.inv_cov = np.linalg.pinv(self.cov, hermitian=True)
            return dist_dict[mesureChoix](patient, centre, self.inv_cov)
        return dist_dict[mesureChoix](patient, centre)
        
    
    def DistIntraClasse(self,tumeurs : str, mesureChoix):
        
        data_tumeurs = self.data.loc[classes == tumeurs]
        xc = data_tumeurs.mean(axis=0)
        print(xc)
        
        max = 0
        for i in range(0,data_tumeurs.shape[0]):
            tmp = self._distance(data_tumeurs.iloc[i], xc, mesureChoix)
            if tmp > max:
                max = tmp
        print(max)
        print("OK")
        return max
        
    def DistInterClasse(self,tumeurs1, tumeurs2, mesureChoix):
        
        # Tumeurs 1, Centre tumeurs2
        data_tm1 = self.data.loc[classes == tumeurs1]
        n = data_tm1.shape[0]
         #alea = data_tm1.iloc[random.randint(0,n-1)]
        
        data_tm2 = self.data.loc[classes == tumeurs2]
        xc_tm2 = data_tm2.mean(axis=0)
        
        distC1_C2 = float("inf")
        for i in range(0,n):
            tmp = self._distance(data_tm1.iloc[i], xc_tm2, mesureChoix)
            if tmp < distC1_C2:
                distC1_C2 = tmp
        print(distC1_C2)
        #print(xc_tm2)
        
        # Tumeurs 2, Centre tumeurs1
        m = data_tm2.shape[0]
            #alea = data_tm1.iloc[random.randint(0,n-1)]

        xc_tm1 = data_tm1.mean(axis=0)
        
        distC2_C1 = float("inf")
        for i in range(0,m):
            tmp = self._distance(data_tm2.iloc[i], xc_tm1, mesureChoix)
            if tmp < distC2_C1:
                distC2_C1 = tmp
        print(distC2_C1)
        #print(xc_tm1)
        
        return min(distC1_C2, distC2_C1)
    
    def overlap(self, tumeurs1, tumeurs2, mesureChoix):
        dC1 = self.DistIntraClasse(tumeurs1,mesureChoix)
        dC2 =  self.DistIntraClasse(tumeurs2,mesureChoix)
        
        dIC1C2 = 2*self.DistInterClasse(tumeurs1,tumeurs2,mesureChoix)
        
        return (dC1+dC2) / dIC1C2
    

            
    
data_100 = pd.read_csv("./donnees_reduites/data_100.csv", index_col=0)
labels = pd.read_csv("./donnees_reduites/labels.csv", index_col=0)
#classes = labels["Class"].reindex(data_100.index)

data = pd.read_csv("./data.csv", index_col=0)

data_5000 = pd.read_csv("./donnees_reduites/data_5000.csv", index_col=0)
classes = labels["Class"].reindex(data_100.index)


patients_brca = data_100.loc[classes == "BRCA"]

print(patients_brca)
print(patients_brca["gene_505"])
print(patients_brca.iloc[10])

x = Methode1(data_100)
x.DistIntraClasse("BRCA","mahalanobis")
x.DistInterClasse("BRCA","COAD","mahalanobis")
x.overlap("BRCA","PRAD","euclidienne")
#labels = ["BRCA", "COAD", "KIRC", "LUAD", "PRAD"]
print(data_100["gene_505"][2])
print(len(data_100["gene_505"]))

for i in range(0,patients_brca.shape[0]):
    print(i)
    
    
"""import numpy as np
from scipy.spatial import distance

# Sample dataset (3 features: height, weight, age)
X = np.array([
    [170, 65, 30],
    [165, 62, 28],
    [180, 75, 35],
    [175, 68, 31]
])

# Compute mean and inverse covariance matrix
mean_vec = np.mean(X, axis=0)
cov_matrix = np.cov(X, rowvar=False)
inv_cov_matrix = np.linalg.inv(cov_matrix)

# Compute Mahalanobis distance for a single point
point = np.array([190, 85, 50])
dist = distance.mahalanobis(point, mean_vec, inv_cov_matrix)

print(f"Mahalanobis distance: {dist:.2f}")

        """