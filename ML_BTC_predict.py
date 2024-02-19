#предсказываем цену BTC используя машинное обучение модель LSTM 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import yfinance as yf 

start = '2014-09-17'
end = '2024-02-13'
stock = 'BTC-USD'

data = yf.download(stock, start, end)
data.reset_index(inplace=True)
# print(data)

#скользящая средняя, с помощью функции смещения(rolling) за последине 100 периодов
ma_100_days = data.Close.rolling(100).mean()
plt.figure(figsize=(8,6))
plt.plot(ma_100_days, 'r') # на графике нанаосим красной
plt.plot(data.Close, 'g') # цену закрытия наносим зелёной 
# plt.show()


ma_200_days = data.Close.rolling(200).mean()
plt.figure(figsize=(16,8))
plt.plot(ma_100_days, 'r')
plt.plot(ma_200_days, 'b')
plt.plot(data.Close, 'g') 
# plt.show()

#удаляем пустые значения, если актив не торгуется в выходные, к примеру
data.dropna(inplace=True)

#разделим данные на обучающую и тестовую выборку
data_train = pd.DataFrame(data.Close[0: int(len(data)*0.80)])#в обучающей выборке 80% срез от 0, 20% - на тестовую выборку
data_test = pd.DataFrame(data.Close[int(len(data)*0.80): len(data)])#в тестовой выборке тест от прошлого значения и до конца
print(data_train.shape)
# print(data_test.shape)

#из библиотеки ML импортируем MinMaxScaler для масштабирования в диапазоне от 0 до 1
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0,1))

#масштабируем обучающие данные и отправляем в обучающую выборку 
data_train_scale = scaler.fit_transform(data_train)

#создадим два пустых списка, которые будет отправлять в нейронную сеть 
x = []
y = []

#пройдём все данные обучающего набора начиная с 100го элемента, 
#чтобы создать последовательность для обучения. модель LSTM 
for i in range(100, data_train_scale.shape[0]):
    x.append(data_train_scale[i-100:i])#добавляем последовательность из 100 предыдущих 
    y.append(data_train_scale[i,0])

#преобразование x и y в массивы numpy для более эффективной обработки 
x, y = np.array(x), np.array(y)

#импорты для построения нейронной сети 
from keras.layers import Dense, Dropout, LSTM
from keras.models import Sequential 

#создаём модель
# и добавляем слои нейронной сети
model = Sequential()
model.add(LSTM(units=50, activation='relu', return_sequences=True,
               input_shape=(x.shape[1], 1)))
model.add(Dropout(0.2))#слой отсева для переобучения сети 

# добавляем ещё несколько слоёв 
model.add(LSTM(units = 60, activation= 'relu', return_sequences=True))
model.add(Dropout(0.3))

model.add(LSTM(units = 80, activation= 'relu', return_sequences=True))
model.add(Dropout(0.4))

model.add(LSTM(units = 120, activation= 'relu'))
model.add(Dropout(0.5))

model.add(Dense(units =1))#этот слой выдаёт прогнозируемое значение в прогнозе покупать или подавать 

model.compile(optimizer = 'adam', loss = 'mean_squared_error')#компилируется модель, 
#используется оптимизатор adam, функция потерь = минимизатор квадратичной ошибки 

model.fit(x, y, epochs=50, batch_size= 32, verbose= 1)#обучаем модель, в течение 50 эпох 

#берём последине 100 дней в обучающем наборе
pas_100_days = data_train.tail(100)
data_test = pd.concat([pas_100_days, data_test], ignore_index=True)
data_test_scale = scaler.fit_transform(data_test )

#повторяем уже с нашими новыми данными 
x = []
y = []

#пройдём все данные обучающего набора начиная с 100го элемента, 
#чтобы создать последовательность для обучения. модель LSTM 
for i in range(100, data_test_scale.shape[0]):
    x.append(data_test_scale[i-100:i])#добавляем последовательность из 100 предыдущих 
    y.append(data_test_scale[i,0])

#преобразование x и y в массивы numpy для более эффективной обработки 
x, y = np.array(x), np.array(y)

#проверяем как модель делает предсказания
y_predict = model.predict(x)

scale = 1/scaler.scale_

y_predict = y_predict * scale
y = y * scale

#создаём новый график под модель 
plt.figure(figsize=(10,8))
plt.plot(y_predict, 'r', label = 'Predicted Price')
plt.plot(y, 'g', label = 'Original Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend
plt.show()

#сохраняем модель
model.save('BTC_pred.keras')