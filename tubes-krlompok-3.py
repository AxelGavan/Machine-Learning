# -*- coding: utf-8 -*-
"""Tubes.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UpZTRfkBPgyEImCNecEVaOUCid5HSutj

## 1. Import Package
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler

"""## 2. Import dataset"""

from google.colab import drive
drive.mount('/content/drive/')

#Read dataset
#import pandas as pd
df = pd.read_csv('/content/drive/My Drive/Colab Notebooks/DataTubes1.csv')
df2 = pd.read_csv('/content/drive/My Drive/Colab Notebooks/DataTubes2.csv')
df3 = pd.read_csv('/content/drive/My Drive/Colab Notebooks/DataTubes3.csv')
#df = pd.read_csv('DataTubes.csv')
df

df2

df.head()

df.describe()

df.isnull().sum()

df.duplicated().sum()

df.info

"""## 3. Exploratory Data Analysis (EDA)"""

Kelurahan34_152 = df.Jumlah_sasaran_ibu_hamil[(df.Jumlah_sasaran_ibu_hamil <= 152) & (df.Jumlah_sasaran_ibu_hamil >= 34)]
Kelurahan154_208 = df.Jumlah_sasaran_ibu_hamil[(df.Jumlah_sasaran_ibu_hamil <= 208) & (df.Jumlah_sasaran_ibu_hamil >= 154)]
Kelurahan211_316 = df.Jumlah_sasaran_ibu_hamil[(df.Jumlah_sasaran_ibu_hamil <= 316) & (df.Jumlah_sasaran_ibu_hamil >= 211)]
Kelurahan323_500 = df.Jumlah_sasaran_ibu_hamil[(df.Jumlah_sasaran_ibu_hamil <= 500) & (df.Jumlah_sasaran_ibu_hamil >= 323)]
Kelurahan500above = df.Jumlah_sasaran_ibu_hamil[df.Jumlah_sasaran_ibu_hamil >= 500]

x = ["0_152","152_208","208_316","316_500","500+"]
y = [len(Kelurahan34_152.values),len(Kelurahan154_208.values),len(Kelurahan211_316.values),len(Kelurahan323_500.values),len(Kelurahan500above.values)]

plt.figure(figsize=(10,6))
sns.barplot(x=x, y=y, palette="rocket")
plt.title("Sasaran Kehamilan per Kelurahan")
plt.xlabel("Jumlah sasaran ibu hamil")
plt.ylabel("Kelurahan")
plt.show()

plt.figure(figsize=(8,5))
plt.title("Jumlah sasaran ibu hamil",fontsize=16)
plt.xlabel ("Jumlah_sasaran_ibu_hamil",fontsize=14)
plt.hist(df['Jumlah_sasaran_ibu_hamil'],color='yellow',edgecolor='black')
plt.show()

#plt.figure(figsize=(8,5))
plt.title("Jumlah sasaran ibu Bersalin/Nifas",fontsize=16)
plt.xlabel ("Jumlah_sasaran_ibu_bersalin",fontsize=14)
plt.hist(df['Jumlah_sasaran_ibu_bersalin'],color='yellow',edgecolor='black')
plt.show()

#plt.figure(figsize=(8,5))
plt.title("Jumlah sasaran kelahiran hidup",fontsize=16)
plt.xlabel ("Jumlah_sasaran_kelahiran_hidup",fontsize=14)
plt.hist(df['Jumlah_sasaran_kelahiran_hidup'],color='yellow',edgecolor='black')
plt.show()

#plt.figure(figsize=(8,5))
plt.title("Jumlah sasaran Bayi",fontsize=16)
plt.xlabel ("Jumlah_sasaran_bayi",fontsize=14)
plt.hist(df['Jumlah_sasaran_bayi'],color='yellow',edgecolor='black')
plt.show()

#plt.figure(figsize=(8,5))
plt.title("Jumlah sasaran Balita",fontsize=16)
plt.xlabel ("Jumlah_sasaran_balita",fontsize=14)
plt.hist(df['Jumlah_sasaran_balita'],color='yellow',edgecolor='black')
plt.show()

plt.figure(figsize=(10,5))
plt.subplot(121)
sns.boxplot(y=df["Jumlah_sasaran_ibu_hamil"])
plt.figure(figsize=(10,100))
plt.subplot(122)
sns.boxplot(x=df['Jumlah_sasaran_ibu_hamil'],y=df["Kelurahan"])

plt.figure(figsize=(15,12))
plt.subplot(221)
sns.boxplot(x=df['Jumlah_sasaran_ibu_hamil'],y=df["Jumlah_sasaran_ibu_bersalin"])
plt.subplot(222)
sns.boxplot(x=df['Jumlah_sasaran_kelahiran_hidup'],y=df["Jumlah_sasaran_bayi"])
plt.show()

categorical_variabel = df.select_dtypes('object')
cat_subset = categorical_variabel.drop(['Kelurahan'],axis=1)

for col in cat_subset:
    plt.figure()
    sns.countplot(x=col, data=df)
    plt.tight_layout()

"""## 4. Preprocessing data"""

label_encoder = LabelEncoder() 
encoded_data = df2[cat_subset.columns]

encoded_data.head()

cluster_data = pd.concat([encoded_data, df2[["Kelurahan", "Total"]]], axis=1)

scaler = StandardScaler()
cluster_data["Total"] = scaler.fit_transform(cluster_data["Total"].values.reshape(-1, 1))

cluster_data.head()

"""## 5. Membangun K-means model"""

cluster = KMeans(n_clusters=3)
cluster.fit(cluster_data)

#membuat kolom baru untuk kelompok
segment = pd.Series(cluster.labels_, name="segment")

pd.concat([df2, segment], axis=1)

"""### 5.1 K optimum"""

wcss = []
K = range(2,10)
for k in K:
    km = KMeans(n_clusters=k)
    km = km.fit(cluster_data)
    wcss.append(km.inertia_)

plt.figure(figsize=(8,6))
plt.plot(K, wcss, 'bx-')
plt.xlabel('Jumlah Cluster')
plt.ylabel('WCSS')
plt.title('Elbow Method For Optimal k')
plt.show()

"""Kesimpulan Dengan memanfaatkan nilai WCSS maka kita bisa mengambil keputusan jumlah segmentasi optimal yang kita gunakan."""

#cluster = KMeans(n_clusters=3)
cluster.fit(cluster_data)

"""### Eksplorasi hasil segmentasi pelanggan"""

segment = pd.Series(cluster.labels_, name="segment")

results = pd.concat([df2, segment], axis=1)

#pd.concat([df2, segment], axis=1)
results[results["segment"]==0].head()

results[results["segment"]==1].head()

results[results["segment"]==2].head()

sns.scatterplot(x=results[results["segment"]==0].Kelurahan, y=results[results["segment"]==0].Total, color="green")
sns.scatterplot(x=results[results["segment"]==1].Kelurahan, y=results[results["segment"]==1].Total, color="red")
sns.scatterplot(x=results[results["segment"]==2].Kelurahan, y=results[results["segment"]==2].Total, color="blue")
plt.grid(True)

sns.boxplot(x=results['segment'],y=results["Total"])

sum_row = df.sum(axis=1)
print (sum_row)

df3.sort_values(["Total","Kelurahan"],axis=0, ascending=True,inplace=True,na_position='first')
df3.loc[:, :]
