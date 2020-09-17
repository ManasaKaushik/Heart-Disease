
# coding: utf-8

# In[2]:


from numpy import genfromtxt
import numpy as np
from numpy import *
import matplotlib


import matplotlib.pyplot as plt


from sklearn.svm import LinearSVC
from sklearn.decomposition import PCA
import pylab as pl
from itertools import cycle
from sklearn import cross_validation
from sklearn.svm import SVC


# Loading data to DF and pruning
dataset = genfromtxt('Desktop/Heart/data.csv',delimiter=',')

# Printing feature and label set attributes
X = dataset[:,0:12] # Feature set
Y = dataset[:,13]  # Label Set

# Binarization of label output
for index, item in enumerate(Y):   # Last row gives 4 diff types of output , so convert them to 0  or 1 
	if not (item == 0.0):       # that is either Yes or No
		Y[index] = 1
print(Y)
target_names = ['0','1']


# Plotting and Dimensionality Reduction

# Method to plot the graph for reduced dimensions
def plot_2D(data,target,target_names):
	colors = cycle('rgbcmykw')
	target_ids = range(len(target_names))
	plt.figure()
	for i,c, label in zip(target_ids, colors, target_names):
		plt.scatter(data[target == i, 0], data[target == i, 1], c=c, label=label)
	plt.legend()
	plt.savefig('Problem 2 Graph')


# Classifying the data using a linear SVM and perdicting the probabilities of disease belonging to a particular class

modelSVM = LinearSVC(C=0.1)
pca = PCA(n_components=2, whiten=True).fit(X)   # n - the number of components retained after Dimensionality Reduction
X_new = pca.transform(X)

# Plotting graph depicting features and labels
plot_2D(X_new, Y, target_names)

# Performing cross validation on train and test sets for validating the linear SVM model
X_train,X_test,Y_train,Y_test = cross_validation.train_test_split(X_new, Y, test_size = 0.2, train_size=0.8, random_state=0)
modelSVM = modelSVM.fit(X_train,Y_train)
print("Linear SVC values with Split")
print(modelSVM.score(X_test, Y_test))



modelSVMRaw = LinearSVC(C = 0.1)
modelSVMRaw = modelSVMRaw.fit(X_new, Y)
cnt = 0
for i in modelSVMRaw.predict(X_new):
	if(i == Y[1]):
		cnt = cnt+1
print("Linear SVC score without split")
print(float(cnt)/101)

# Applying the PCA on the feature set
modelSVM2 = SVC(C = 0.1,kernel='rbf')

# Applying the cross validation on training and the test set for validating the linear SVM model
X_train1,X_test1,Y_train1,Y_test1 = cross_validation.train_test_split(X_new, Y, test_size = 0.2, train_size=0.1, random_state=0)
modelSVM2 = modelSVM2.fit(X_train1,Y_train1)
print("RBF score with split")
print(modelSVM2.score(X_test1,Y_test1))


modelSVMRaw2 = SVC(C=0.1, kernel='rbf')
modelSVMRaw2 = modelSVMRaw2.fit(X_new,Y)
cnt1 = 0
for i in modelSVMRaw2.predict(X_new):
	if i == Y[1]:
		cnt1 = cnt1 + 1
print("RBF score without split")
print(float(cnt1)/298)





# Generating the mesh plots
X_min, X_max = X_new[:,0].min() - 1, X_new[:,0].max() + 1
Y_min, Y_max = X_new[:,1].min() - 1, X_new[:,1].max() + 1
xx, yy = np.meshgrid(np.arange(X_min, X_max,0.2),
	                 np.arange(Y_min, Y_max,0.2))

# Axis titles for the plot
titles = "SVC ( RBF kernel) - Plotting highest varied 2 PCA values"

# Plotting decision boundaries using contrast coloring
# for each point in the mesh
plt .subplot(2,2, i + 1)
plt.subplots_adjust(wspace = 0.4, hspace=0.4)
Z = modelSVM2.predict(np.c_[xx.ravel(), yy.ravel()])


# Convert the obtained result into a color plot
Z = Z.reshape(xx.shape)
plt.contourf(xx,yy,Z,cmap=plt.cm.Paired, alpha=0.1)

# Plot the color points to show classified segments
plt.scatter(X_new[:,0], X_new[:,1], c=Y, cmap = plt.cm.Paired)
plt.xlabel("PCA1")
plt.ylabel("PCA2")
plt.xlim(xx.min(),xx.max())
plt.ylim(yy.min(),yy.max())
plt.xticks(())
plt.yticks(())
plt.title(titles)
plt.show()

