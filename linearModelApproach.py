import pandas as pd
import numpy as np

from dataProcessing import loadData, dataProcess
from plotting import TrainingPlot
from Models import createLinearModel

train, test, submission, items, itemCategory, shops = loadData()

dataset = dataProcess(train, test)

# split into training set and test set
X = np.expand_dims(dataset.values[:,:-1], axis=2)
y = dataset.values[:,-1:]

X_test = np.expand_dims(dataset.values[:,1:], axis=2)

filename = 'output/training_plot.jpg'
plot_losses = TrainingPlot()

model = createLinearModel()
model.summary()
model.fit(X[:,:,0], y, batch_size=4096, epochs=10, callbacks=[plot_losses])

submission=model.predict(X_test[:,:,0])
submission=submission.clip(0,20)
submission=pd.DataFrame({'ID':test['ID'], 'item_cnt_month':submission.ravel()})
submission.to_csv('result/linear_predicts.csv',index=False)