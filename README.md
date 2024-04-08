**Выпускная квалификационная работа**

**Тема**: "Определение популярности геолокации для размещения банкомата".

Постановка задачи: Необходимо построить модель, которая по географическим координатам и адресу точки выдаст оценку индекса популярности банкомата в этой самой локации. Другими словами найти новые хорошие локации для банкоматов.

Автор работы - Ким Игорь (телеграм t.me/igorkimrb)

Научный руководитель - Гаврилова Елизавета (телеграм t.me/lizvladii)

**Описание данных**:

Датасет взят из соревнования: https://boosters.pro/championship/rosbank2/overview

Описание датасета:</br>
id – уникальный идентификатор банкомата;</br>
atm_group – принадлежность банкомата к какой-то группе;</br>
address – адрес на латинице;</br>
address_rus – адрес на кириллице;</br>
lat– широта;</br>
long –долгота;</br>
target -  индекс популярности банкомата.

Сам датасет лежит в папке data

**Примерный план проекта**:</br>
1. Написать скрипты для парсинга данных с OSM, Яндекс Geoсoder. Выбрать модель с наименьшим RMSE. (до 07.04)
2. Продумать ML-OPS (до 14.04)
3. Написать сервис и развернуть локально (до 28.04)
4. Развернуть сервис в облаке (до 12.05)

**Примерный технологический стек:**</br>
Python</br>
Pyrosm, Geopandas</br>
Flake8</br>
CatBoost, Scikit-learn</br>
MLflow</br>
Docker</br>
Telegram Bot API

**Описание сервиса**:</br>
Сервис представляет из себя телеграм бот, который получает от пользователя координаты и получает в ответ индекс популярности геолокации для размещения банкомата.
