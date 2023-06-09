from django.db import models

class EcgData(models.Model):
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    height = models.FloatField()
    weight = models.FloatField()
    qrs_duration = models.IntegerField()
    p_r_interval = models.IntegerField()
    q_t_interval = models.IntegerField()
    t_interval = models.IntegerField()
    p_interval = models.IntegerField()
    qrs = models.IntegerField()
    t = models.IntegerField()
    p = models.IntegerField()
    qrst = models.IntegerField()
    heart_rate = models.IntegerField()
    q_wave = models.FloatField()
    r_wave = models.FloatField()
    s_wave = models.FloatField()
    diagnosis = models.CharField(max_length=10)
    label = models.CharField(max_length=80)