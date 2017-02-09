import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression

data = np.reshape(np.random.randn(20),(10,2)) # 10 training examples
labels = np.random.randint(2, size=10) # 10 labels

X = pd.DataFrame(data)
y = pd.Series(labels)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

model = LogisticRegression()
model = model.fit(X_train, y_train)

df_coefs = pd.DataFrame(model.coef_[0], index=X.columns, columns = ['Coefficient'])
print df_coefs
