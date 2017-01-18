import sys, getopt
import itertools
import numpy as np
from errno import EEXIST
from os import makedirs, path
from numpy import genfromtxt

import matplotlib.pyplot as plt

from sklearn.multiclass import OneVsOneClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier



def classifiers(X, y, filename, kingdom):
	np.set_printoptions(precision=2)
	#Need to read in target names from counts preferably, and in order
	if kingdom == 'mammal':
		target_names = ['Nucleus', 'Cytoplasm', 'Endoplasmic', 'Secreted', 'Mitochodria', 'Cellmembrane', 'Golgi App', 'Membrane']
	elif kingdom == 'fungi':
		target_names = ['Nucleus', 'Cytoplasm', 'Endoplasmic', 'Secreted', 'Mitochodria', 'Cellmembrane', 'Golgi App', 'Vacuole', 'Membrane']
	elif kingdom == 'human':
		target_names = ['Nucleus', 'Cytoplasm', 'Endoplasmic', 'Secreted', 'Mitochodria', 'Cellmembrane', 'Golgi App', 'Membrane']
	elif kingdom == 'plants':
		target_names = ['Nucleus', 'Cytoplasm', 'Endoplasmic', 'Secreted', 'Mitochodria', 'Cellmembrane', 'Golgi App', 'Chloroplast', 'Vacuole', 'Membrane']
	elif kingdom == 'rodent':
		target_names = ['Nucleus', 'Cytoplasm', 'Endoplasmic', 'Secreted', 'Mitochodria', 'Cellmembrane', 'Golgi App', 'Membrane']
	else:
		target_names = ['Nucleus', 'Cytoplasm', 'Endoplasmic', 'Secreted', 'Mitochodria', 'Cellmembrane', 'Golgi App', 'Membrane']
	feature_names = ['3Xmin', '3Xmax', '3Xmean', '3Xstd', '2Xmin', '2Xmax', '2Xmean', '2Xstd', '1Xmin', '1Xmax', '1Xmean', '1Xstd', '3Ymin', '3Ymax', '3Ymean', '3Ystd', '2Ymin', '2Ymax'
					, '2Ymean', '2Ystd', '1Ymin', '1Ymax', '1Ymean', '1Ystd']

	#split into training and test, should keep classes proportionate
	sss = StratifiedShuffleSplit(n_splits=1, test_size=0.3, random_state=0)

	names = ["Nearest Neighbors", "Linear SVM", "RBF SVM",
         "Decision Tree", "Random Forest", "Neural Net",
		 "AdaBoost",
         "Naive Bayes", "QDA"]
	names = ["Nearest Neighbors", "Neural Net", "AdaBoost", "QDA"]

	# Classifier models
	models = [
		KNeighborsClassifier(len(target_names)),
    	#SVC(kernel="linear", C=0.025),
    	#SVC(gamma=2, C=1),
    	#DecisionTreeClassifier(max_depth=5),
    	#RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    	MLPClassifier(),
    	AdaBoostClassifier(),
    	#GaussianNB(),
    	QuadraticDiscriminantAnalysis(),
		]

	#Could function this and set OvO as an option
	for train_index, test_index in sss.split(X, y):
		for name, clf in zip(names, models):
			#OneVsOneClassifier(Put next line in here if wanted)
			clf.fit(X[train_index], y[train_index])
			#save this all to same file
			outputdir = 'scores/' + kingdom + '/'
			mkdir_p(outputdir)
			f = open(outputdir + 'scores.txt','a')
			f.write(filename + ' ' + name + ',' + str(clf.score(X[test_index], y[test_index])) + '\n')
			cnf_matrix = confusion_matrix(y[test_index], clf.predict(X[test_index]))
			# Plot normalized confusion matrix
			fig = plt.figure()
			fig.set_tight_layout(False)
			print name
			print(accuracy_score(y[test_index], clf.predict(X[test_index])))
			print(classification_report(y[test_index], clf.predict(X[test_index])))#, target_names=target_names))
			plot_confusion_matrix(cnf_matrix, classes=target_names, normalize=False,
			                      title='Confusion matrix')
			outputdir = 'plots/' + filename + '/'
			mkdir_p(outputdir)
			#fig.show()
			fig.savefig(outputdir + name + 'plot.png')
	#explore class_weight


	#OneVsOneClassifier(svm).fit(data, target).predict(data)
	#OVOrf = OneVsOneClassifier(rf).fit(data, target).predict(data)
	#OVOrf = OneVsOneClassifier(rf).fit(x_train, y_train).predict(x_test)
	#table = confusion_matrix(y_test,OVOrf)
	#print table

	#print(classification_report(y_test, OVOrf, target_names=target_names))


	#output = open(outputfile, 'w')
	#score = outputfile + ', ' + str(rf.score(x_test, y_test)) + '\n'
	#output.write(score)
	#output.close()

	#table = confusion_matrix(y_test, predict)
	#print table[0]


# Overfitting, do not record accuracy here
def featureExtraction(data, target):
	#rf = RandomForestClassifier(n_jobs=-1)
	#svm = SVC()

	#rf.fit(data, target)
	#svm.fit(data, target)

	#importances = rf.feature_importances_


	std = np.std([tree.feature_importances_ for tree in rf.estimators_], axis=0)
	indices = np.argsort(importances)[::-1]
	print("Feature ranking:")
	for f in range(data.shape[1]):
		print("%d feature, %d, %f" % (f + 1, indices[f], importances[indices[f]]))

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

#np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
#plt.figure()
#plot_confusion_matrix(cnf_matrix, classes=class_names,
#                      title='Confusion matrix, without normalization')

def mkdir_p(mypath):
    #Creates a directory. equivalent to using mkdir -p on the command line

    try:
        makedirs(mypath)
    except OSError as exc: # Python >2.5
        if exc.errno == EEXIST and path.isdir(mypath):
            pass
        else: raise

def main(argv):
	try:
		opts, args = getopt.getopt(argv,"hd:t:",["datafile=","targetfile="])
	except getopt.GetoptError:
		print 'classification.py -d <datafile> -t <targetfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'classification.py -d <datafile> -t <targetfile>'
			sys.exit()
		elif opt in ("-d", "--datafile"):
			dfile = arg
		elif opt in ("-t", "--targetfile"):
			tfile = arg

	data = genfromtxt(dfile, delimiter=',')
	target = genfromtxt(tfile, delimiter=',')
	library, kingdom, prope = str(dfile).split("/")
	prop, scrap = prope.split("_")
	filename = kingdom + '/' + prop
	classifiers(data, target, filename, kingdom)
	# featureExtraction(data, target)

main(sys.argv[1:])
