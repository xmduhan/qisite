from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime


class WeChatReceive(models.Model):


    receiveTime = models.DateTimeField("接收时间", default=datetime.now)
