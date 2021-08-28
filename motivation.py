import numpy as np
import pandas as pd
import re
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
import pickle
from nltk.corpus import stopwords
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import RFE
from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()

#X=pd.read_csv("textFeatures.csv")
spreadsheet=pd.read_csv("ireMotivation2.csv")
X=spreadsheet['text']
X=X.astype(str).values.tolist()

#THIS IS REALLY IMPORTANT. Use top line for Y if you have students ordered by code (1, 2, 3, 4, 5) Use bottom line for Y if you have students ordered by MOOCIBL number (33, 35, 37)
#Y=[1,0,1,1,0,0,0,0,1,1,1,1,1,1,1,0,1,1,0,0,1,0,1,0,1,1,0,1]
Y=[0,0,1,1,1,0,1,0,0,1,0,0,0,0,1,1,1,1,1,1,0,1,1,1,1,1,0,1]




documents = []
documents_toPred=[]





from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
XToPred=X

X = vectorizer.fit_transform(X).toarray()
print(X.size)
from sklearn.metrics.pairwise import cosine_similarity
dist=1-cosine_similarity(X)
print(dist.size)

from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering

true_k=5
model=KMeans(n_clusters=true_k, init='k-means++', max_iter=1000, n_init=1)
model.fit(dist)



print("Top terms per cluster:")
order_centroids=model.cluster_centers_.argsort()[:, ::-1]
terms=vectorizer.get_feature_names()

df = pd.DataFrame(terms)
df.to_csv('featuresList.csv', index=False)

for i in range(true_k):
  print("Cluster %d:" % i),
  for ind in order_centroids[i,:100]:
    print(' %s' % terms [ind]),
  print

XToPred=vectorizer.transform(XToPred)

#for i in range(len(X)):
  #prediction=model.predict(XToPred[i])
  #print(prediction)

model=AgglomerativeClustering(n_clusters=5, affinity='euclidean', linkage='ward')
model.fit(dist)
labels=model.labels_
print(labels)


print(X.size)

#plt.scatter(X[labels==0, 50], X[labels==0, 53], s=50, marker='o', color='red')
#plt.scatter(X[labels==1, 50], X[labels==1, 53], s=50, marker='o', color='blue')
#plt.scatter(X[labels==2, 50], X[labels==2, 53], s=50, marker='o', color='green')
#plt.scatter(X[labels==3, 50], X[labels==3, 53], s=50, marker='o', color='purple')
#plt.scatter(X[labels==4, 50], X[labels==4, 53], s=50, marker='o', color='orange')
#plt.scatter(X[labels==5, 50], X[labels==5, 53], s=50, marker='o', color='yellow')
#plt.scatter(X[labels==6, 50], X[labels==6, 53], s=50, marker='o', color='pink')
#plt.scatter(X[labels==7, 50], X[labels==7, 53], s=50, marker='o', color='black')
#plt.savefig('Clusters.png')

#print(X[:,65])

from scipy.cluster.hierarchy import ward, dendrogram
import matplotlib.pyplot as plt

linkage_matrix = ward(dist) #define the linkage_matrix using ward clustering pre-computed distances
print(linkage_matrix)
#titles=('N1','N2','N3','N4','N5','N6','N7','N8','N9','N10','N11','N12','N13','N14','E1','E2','E3','E4','E5','E6','P1','P2','P3','P4','P5','P6','P7','P8','P9','P10','P11','P12','P13','P14','P15','P16','P17','P18','P19','P20','P21','P22','P23','P24')
titles=()
for i in range(27):
  titles=titles+('design'+str(i),'techcomp'+str(i),'teamwork'+str(i),'professionalism'+str(i),'general'+str(i),'future'+str(i))
#titles=('Josh G', 'Steven H', 'Evan G', 'Sri G', 'Michael S','Broderick N', 'Willy J', 'Mitchell O','Josh H', 'Obinna A', 'Rachel J', 'Kayla M', 'Davina K', 'Derek H', 'Vidura J', 'NathanR', 'Sam P','Colin B', 'Pranjal M', 'Kalleigh M', 'Joseph A','John C', 'Tyson D', 'Abby A', 'Parshuram A', 'Rabie F', 'Zach D','Bijay G')
#titles=('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28')
fig, ax = plt.subplots(figsize=(45, 50)) # set size
print(len(titles))
print(len(X))
ax = dendrogram(linkage_matrix, orientation="right", labels=titles);

plt.tick_params(\
    axis= 'x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')

plt.tight_layout() #show plot with tight layout

#uncomment below to save figure
plt.savefig('ward_clusters.png', dpi=200) #save figure as ward_clusters