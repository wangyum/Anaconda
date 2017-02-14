##Fetch data from hive with pyspark
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("spark_pandas_it").enableHiveSupport().getOrCreate()


df = spark.sql("select * from bic.usr_crm_label t where t.gender_woman_flg >= 0 limit 10000")
df_tot = df.toPandas()
df_tot = df_tot.fillna(0)

import numpy as np 
import pandas as pd 
from  cPickle import dump, load

select_x = df_tot.columns.isin(['credit_score', 'lostprob', 'family_group_type'])
X = df_tot.ix[:,select_x]
Y = df_tot.gender_woman_flg.values

##Logistic regression
from sklearn.cross_validation import train_test_split
train_X, test_X, train_y, test_y = train_test_split(X,Y,train_size=0.4,random_state=1)

from sklearn import linear_model, datasets  
logreg = linear_model.LogisticRegression(C=1e5, solver='lbfgs', multi_class='multinomial')
logreg.fit(train_X,train_y)

from sklearn import metrics
prediction = logreg.predict(test_X)  
print("accuracy score: ")  
print(metrics.accuracy_score(test_y, prediction))  
print(metrics.classification_report(test_y, prediction)) 
print metrics.confusion_matrix(test_y,prediction)

##AUC score
pre = logreg.predict_log_proba(test_X)
metrics.roc_auc_score(test_y,pre[:,1])

##GBDT
from sklearn.ensemble import GradientBoostingClassifier
Gradclf = GradientBoostingClassifier(subsample=0.8,n_estimators=10,verbose=1,warm_start = True)
Gradclf.fit(X,Y)
pre = Gradclf.predict_proba(test_X)
metrics.roc_auc_score(test_y,pre[:,1])

##Save model
dump(Gradclf,open('pyspark_learning_model.pickle','wb'))

##Export coefs
from pyspark.sql.types import *
from pyspark.sql import Row
coefvalue = Gradclf.feature_importances_
coefdf = pd.DataFrame({'name': df_tot.columns[select_x], 'value': coefvalue})

##Insert into hive tables

fields = [StructField("name", StringType(), True), StructField("value", DoubleType(), True)]
schema = StructType(fields)
coef_output = spark.createDataFrame(coefdf,schema)
coef_output.createOrReplaceTempView("pyspark_learning_output")
spark.sql("INSERT OVERWRITE TABLE tmp.kgl_output_test SELECT * FROM pyspark_learning_output")

