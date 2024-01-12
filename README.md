### Установка и запуск:
Для установки требуется Python 3.6+
Сборка пакета:
```sh
python setup.py sdist bdist_wheel
```
Установка:
```sh
pip install dmtxrecogn
```
Запуск:
```sh
python /usr/bin/dmtxrecogn
```
Сервис будет доступен по http://127.0.0.1:9000/dmtxrecogn

---
Если файла /usr/bin/dmtxrecogn не существует, то посмотреть куда python кладет собранные пакеты и использовать соответвующий путь:
```sh
python -m site --user-base
```
Возможно, в таком случае, еще потребуется указать путь к каталогу:
```sh
export PYTHONPATH=$PYTHONPATH:/путь/к/вашему/каталогу/bin
```

### Разработка

Установка окружения для разработки:
```sh
pip install .["test"]
```
Запуск:
```sh
python setup.py run
```

Запуск скрипта для распознавания:
```sh
python3 test.py
```