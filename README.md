Тестовое задание - "Баннерокрутилка"
====================================

Запуск приложения и тестов
--------------------------

Приложение не требует для запуска дополнительных библиотек.
Чтобы запустить приложение, выполните команду:
```
  > python banrot.py
```  
Для проверки работы зайдите по ссылке: http://localhost:5000/?category=cat2&category=cat4

Для запуска тестов требуется установить пакет mock.
Для сборки виртуальной среды и установки зависимостей запустите скрипт `make-env.sh`
Затем выполните команды:
```
  > source ve/bin/activate
  > python tests.py
```
  
Приложение не расчитано на работу в мульти-тредовой среде.
В принципе, реализацию не трудно сделать thread-safe используя локи, но большого смысла в этом не вижу, 
так как это не приведет к реальному распараллеливанию обработки запросов (опять же GIL).

Использовать какие-либо асинхронные решения (non-blocking IO) типа gevent так же не вижу смысла, 
поскольку ввода-ввывода никакого нет.

На продакшене я бы запустил несколько воркеров в связке nginx + uwsgi

Реализация алгоритма
--------------------

Для каждой категории отслеживается суммарное количество показов.
Когда приходит запрос с несколькими категориями, то выбирается одна категория N с наибольшим количеством показов.
Данные о всех баннерах хранятся в списке.
Делаем простой перебор с начала списка, пока не дойдем до баннера с категорией N.
Извлекаем этот баннер из списка, отдаем его наружу и если у него еще есть показы, то добавляем его в конец списка.
С одной стороны, простой перебор как бы не очень хорошо, но если распределение баннеров по категориям более-менее 
равновероятно, то это не должно приводить к большому количеству итераций.
И даже на нагрузочных тестах, когда в исходных данных присутсвуют "редкие" категории (один банер на категорию), 
то при общем количестве в 1000 записей разница совершенно не существенная.