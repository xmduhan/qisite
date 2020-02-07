

```shell
virtualenv env
source env/bin/activate
pip install git+git://github.com/ojii/pymaging.git#egg=pymaging
pip install git+git://github.com/ojii/pymaging-png.git#egg=pymaging-png
pip install -r env/requirements.txt
```

```shell
cp config.py.sample config.py
```

```shell
python manage.py syncdb
python manage.py migrate
```
