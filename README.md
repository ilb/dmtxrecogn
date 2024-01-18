### Использование
Пример curl-запроса:
```sh
curl -X POST https://avclick.ru/dmtxrecogn/api/recognize/ \
  -H "Content-Type: multipart/form-data; boundary=WebAppBoundary" \
  -F 'params={"type": "IDENTICAL", "segment": {"x": 1, "y": 6}}' \
  -F 'files=@images/24.jpg'
```

### Установка и запуск
Для установки требуется Python 3.6+
Сборка пакета:
```sh
python3 setup.py sdist bdist_wheel
```
Установка:
```sh
pip install dmtxrecogn # or pipx install dmtxrecogn
```
Запуск:
```sh
python3 /usr/bin/dmtxrecogn
```
Сервис будет доступен по http://127.0.0.1:9000/dmtxrecogn

---
Если файла /usr/bin/dmtxrecogn не существует, то посмотреть куда python кладет собранные пакеты и использовать соответвующий путь:
```sh
python3 -m site --user-base
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
python3 setup.py run
```

Запуск скрипта для распознавания:
```sh
python3 test.py
```
