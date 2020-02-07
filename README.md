

```shell
virtualenv env
source env/bin/activate
pip install -r env/requirements.txt
```

```shell
cp config.py.sample config.py
```

```shell
python manage.py syncdb
python manage.py migrate
```
