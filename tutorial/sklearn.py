# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division

'''
scikit-learn 예제

scikit-learn이란?
- machine learning 패키지
- classification, regression, clustering을 모두 지원

패키지 설치
!conda install -y scikit-learn
'''

from sklearn import datasets, svm, tree
import pandas as pd
import numpy as np

#%%
'''
iris 데이터셋: 총 150개, 4개 컬럼
'''
iris = pd.read_csv('data/iris.csv')
iris['type'] = iris['type'].astype('category')

#%%
'''
SVM 학습
- gamma와 C는 임의의 값임.
- 총 150개 가운데 142개에 대해 정확한 값이 나옴
'''
clf = svm.SVC(gamma=0.0001, C=100.)
clf.fit(iris.iloc[:, 0:4], iris['type'].values.codes)

pred = clf.predict(iris.iloc[:, 0:4])
sum(iris['type'].values.codes == pred)

#%%
'''
위의 결과는 training set을 그대로 test set으로 사용한 결과. (일종의 cheating)
training set과 test set을 8:2로 분할하여 다시 훈련

- 정확도 계산은 accuracy_score()를 사용
'''
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

iris_train, iris_test = train_test_split(iris, test_size=.2)
     
clf.fit(iris_train.iloc[:, 0:4], iris_train['type'].values.codes)

pred = clf.predict(iris_train.iloc[:, 0:4])
print(sum(iris_train['type'].values.codes == pred) / iris_train.shape[0])
print(accuracy_score(iris_train['type'].values.codes, pred))

pred = clf.predict(iris_test.iloc[:, 0:4])
print(accuracy_score(iris_test['type'].values.codes, pred))

#%%
'''
CART(Classification and Regression Tree) 학습
'''
clf = tree.DecisionTreeClassifier()
clf.fit(iris_train.iloc[:, 0:4], iris_train['type'].values.codes)

pred = clf.predict(iris_train.iloc[:, 0:4])
print(accuracy_score(iris_train['type'].values.codes, pred))

pred = clf.predict(iris_test.iloc[:, 0:4])
print(accuracy_score(iris_test['type'].values.codes, pred))

#%%
'''
트리 시각화

!conda install -c conda-forge -y pydotplus
!conda install -y graphviz
'''
import pydotplus
from IPython.display import Image

tree_dot = tree.export_graphviz(clf, out_file=None,
                                feature_names=iris.columns.values,
                                class_names=iris['type'].values.categories.values)
tree_graph = pydotplus.graph_from_dot_data(tree_dot)
Image(tree_graph.create_png())