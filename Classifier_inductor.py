'''
This program generates classifiers based on the well known algorithms Logistic Regression, Decision Tree and KNN.

The sampling technique used is based on the Leave One Out and Monte Carlo algorithms. Leave one out is used because the data set we are dealing in the waiter problem is quite small (about a hundred samples).

The Tfidf algorithm lowers the impact from highly frequent features in the corpus (those give less information).

Some names are in portuguese because i did this program as an evaluation, from a college course, and i am too lazy to change it all.
'''

'''
Importing necessary libraries from sklearn.
'''
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import LeaveOneOut
from time import time
from scipy.stats import randint
from sklearn.model_selection import RandomizedSearchCV


loo = LeaveOneOut()



class Indutor:
	'''Based on a small training data set (because of the leave one out), this class looks for the best classifier possible in the molding of Logistic Regression, Decision Tree and KNN.'''
	vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,strip_accents='unicode')

	def __init__(self,treinamento = 'clienteTrain.txt'):
		'''Logistic Regression solver ='liblinear' is good for small datasets. 
The format is sample -> self.x ; sample class -> self.y'''

		corpus, classes = self.conjunto_dados(arg=treinamento)
		self.x = self.vectorizer.fit_transform(corpus)
		self.y = np.array(classes)
		self.knn_value = [0,0,0]
		self.logreg_value = [0,0,0]
		self.dtree_value = [0,0,0]
		self.model = KNeighborsClassifier()
		self.dtree = DecisionTreeClassifier()
		self.logisreg = LogisticRegression(solver ='liblinear',multi_class='auto')

	def melhor_classificador(self):
		'''Testing accuracy, precision score and recall score. Best value for these measures == 1, so the classifier with the highest sum should be chosen. Flag 'average' = 'micro', indicates that the metric calculation takes into account all true positives, false negatives and false positives. This method returns one of three strings: KNN; Regressao Logistica ( for Logistic Regression); Arvore de Decisao (for Decision Tree).'''

		#Parameters to adjust in training
		param_dist = {"max_depth": [4, None], "max_features": randint(1, 11), "min_samples_split": randint(2, 11), "criterion": ["gini", "entropy"]}
		param_knn = {"n_neighbors": randint(1, 11)}
		param_lreg = {"class_weight": ['balanced', None]}

		#knn and logistic regression only accept n_iter = 2 ... why? I have no idea
		random_search_dtree = RandomizedSearchCV(self.dtree, param_distributions=param_dist, n_iter=10, cv=3, iid=False, refit=True)
		random_search_knn = RandomizedSearchCV(self.model, param_distributions=param_knn, n_iter=2, cv=3, iid=False, refit=True)
		random_search_lreg = RandomizedSearchCV(self.logisreg, param_distributions=param_lreg, n_iter=2, cv=3, iid=False, refit=True)
		
		start = time()
		knn_pred = []
		logreg_pred = []
		tree_pred = []
		y_true = []

		#Since i like the monte carlo way, this will take a while so just say something so that the user knows it's ok
		print('Running Inductor, this may take a few minutes ...')

		for train_index, test_index in loo.split(self.x):

			x_train, x_test = self.x[train_index], self.x[test_index]
			y_train, y_test = self.y[train_index], self.y[test_index]
			y_true.append(y_test)
			crit_count = 0
			min_splits_s = 0
			max_feat_s =0
			depth4 = 0
			knn_neigh = 0
			lreg_pesos = 0

			#Adjusting the parameters with the training examples. Remember, you can never adjust using the test example!!
			for tun_index, val_index in loo.split(x_train):

				x_tuning = x_train[tun_index]
				y_tuning = y_train[tun_index]
				random_search_dtree.fit(x_tuning, y_tuning)
				random_search_knn.fit(x_tuning, y_tuning)
				random_search_lreg.fit(x_tuning, y_tuning)

				#Best parameters of this iteration
				m_dtree = random_search_dtree.best_params_
				min_splits_s += m_dtree['min_samples_split']
				max_feat_s += m_dtree['max_features']
				if m_dtree['criterion'] == 'entropy':
					crit_count += 1
				if m_dtree['max_depth'] == 4:
					depth4 += 1

				knn_neigh += random_search_knn.best_params_['n_neighbors']

				if random_search_lreg.best_params_['class_weight'] == 'balanced':
					lreg_pesos += 1

			#using the average value of the parameters found in the loop above
			if crit_count > loo.get_n_splits(x_train)-crit_count:
				criteria = 'entropy'
			else:
				criteria = 'gini'
			if depth4 > loo.get_n_splits(x_train)-depth4:
				depthdt = 4
			else:
				depthdt = None

			min_samples_split = int(min_splits_s/loo.get_n_splits(x_train))
			max_features = int(max_feat_s/loo.get_n_splits(x_train))

			if lreg_pesos > loo.get_n_splits(x_train)-lreg_pesos:
				lreg_peso = 'balanced'
			else:
				lreg_peso = None

			vizinhos_knn = int(knn_neigh/loo.get_n_splits(x_train))

			#building the objects with parameters that were adjusted in the training
			self.dtree = DecisionTreeClassifier(criterion=criteria, min_samples_split=min_samples_split, max_features=max_features, max_depth=depthdt)
			self.model = KNeighborsClassifier(n_neighbors=vizinhos_knn)
			self.logisreg = LogisticRegression(class_weight=lreg_peso,solver ='liblinear',multi_class='auto')

			#training of classification models.
			self.model.fit(x_train,y_train)
			self.dtree.fit(x_train,y_train)
			self.logisreg.fit(x_train,y_train)
			#salving the prediction of the test example
			knn_pred.append(self.model.predict(x_test))
			logreg_pred.append(self.logisreg.predict(x_test))
			tree_pred.append(self.dtree.predict(x_test))

		#Now, outside the loop we have the predictions and can thus verify accuracy, precision score and recall score in a monte carlo way. To avoid overfitting we can NOT use the model with the best prediction that was made in the loop above. We have to choose a random one from them, so i just saved the prediction values on each iteration and not the classiers, they were overwritten in the beginnig of each iteration. This way i "randomly" chose the last model made.
  
		#see line 61, here we are just checking how much time it took for this monte carlo sampling
		tempo = time() - start
		tempo_min = int(tempo/60)
		delta_T = tempo-tempo_min*60
		print("%d minutes and %.2f seconds for the Inductor to build the three classifiers" %(tempo_min,delta_T))
		self.knn_value = [accuracy_score(y_true, knn_pred),precision_score(y_true, knn_pred, average='micro'),recall_score(y_true, knn_pred, average='micro')]
		self.logreg_value = [accuracy_score(y_true, logreg_pred),precision_score(y_true, logreg_pred, average='micro'),recall_score(y_true, logreg_pred, average='micro')]
		self.dtree_value = [accuracy_score(y_true, tree_pred),precision_score(y_true, tree_pred, average='micro'),recall_score(y_true, tree_pred, average='micro')]

		#Here we are making a simple score to decide which to choose from Logistic Regression, Decision Tree and KNN.
		sk, sl, st = 0, 0, 0
		for i in self.logreg_value:
			sl += i
		for i in self.dtree_value:
			st += i
		for i in self.knn_value:
			sk += i
		if sk >= sl and sk >= st:
			return ['KNN',self.model]
		elif sl > sk and sl >= st:
			return ['Regressao Logistica',self.logisreg]
		else:
			return ['Arvore de Decisao',self.dtree]
	
	def print_classificador(self):
		'''As the name sugests, this will print the best classifier and its accuracy, precision score and recall score.  '''
		met = self.melhor_classificador()
		if met[0] == 'KNN':
			print('Chosen classifier: KNN (K=%d).'%self.k,'\nAccuracy = %f\nPrecision score = %f\nRecall score = %f\n'%(self.knn_value[0],self.knn_value[1],self.knn_value[2]))
		elif met[0] == 'Regressao Logistica':
			print('Chosen classifier: Logistic Regression.\nAccuracy = %f\nPrecision score = %f\nRecall score = %f\n'%(self.logreg_value[0],self.logreg_value[1],self.logreg_value[2]))
		else:
			print('Chosen classifier: Decision Tree.\nAccuracy = %f\nPrecision score = %f\nRecall score = %f\n'%(self.dtree_value[0],self.dtree_value[1],self.dtree_value[2]))
		return met

	def user_test(self):
		'''This is for you to test 3 intentions (i say intention because i was building a chatbot for a restaurant). As simple as that (can be used to best prepare the dataset).'''
		metod = self.print_classificador()
		print('Test three intentions (if you are using my trainning file, you need to test in portuguese!): (If you\'d be kind, inform quantity as \'one\', \'two\', \'three\',...since 1,2,3,... are also used to indicate a menu order.)\n')
		for i in range(3):
			text = input().lower()
			inst_text = self.vectorizer.transform([text])
			print(metod[1].predict(inst_text))
		
	def cardapio(self,sem_estoque=None):
		'''Menu.

Parameters
----------
sem_estoque: An order that is temporarily out of stock.'''
		f = open('cardapio.txt','r')
		f.seek(0)
		temp = f.readlines()
		if sem_estoque != None:
			for i in temp:
				if sem_estoque not in i.lower():
					print(i)
		else:
			for i in temp:
				print(i)

	def conjunto_dados(self,arg='clienteTrain.txt'):
		'''This method takes the format of the dataset (class-example) and retrieves the information in two separate lists.'''
		f = open(arg,'r')
		f.seek(0)
		#"a" receives all the training text, however with the '\n' at the end of each line
		a = f.readlines()
		f.close()
		exemplos = []
		classes = []
		for i in a:
			#i[:-1] is the string without the last position (without the '\n')
			#"sep" determines where the class ends and where the example starts
			# lower() for the examples to be case insensitives
			sep = i.find('-',0,len(i))
			classes.append(i[:sep].lower())
			exemplos.append(i[sep+1:-1].lower())
		return (exemplos,classes)

if __name__ == "__main__":
	import sys
	if len(sys.argv) == 1:
		roger = Indutor()
		roger.user_test()
	elif len(sys.argv) == 2:
		roger = Indutor(treinamento=sys.argv[1])
		roger.user_test()
	else:
		print("It is necessary to inform the training examples as an argument and no other files!\nEx: $ python3 Classifier_inductor.py clienteTrain.txt")
