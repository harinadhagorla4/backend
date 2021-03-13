from django.db import models


class Ifsc(models.Model):
    bank_name = models.CharField(max_length=50)
    ifsc = models.CharField(max_length=30, unique=True)
    micr_code = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    std_code = models.IntegerField()
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=30)
    state = models.CharField(max_length=40)

    def __str__(self):
        return self.bank_name


class IfscSearchTrack(models.Model):
    ifsc = models.ForeignKey(Ifsc, on_delete=models.CASCADE)
    search_time = models.DateTimeField(auto_now=True)
