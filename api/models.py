from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=200, default='')
    numPeopleNow = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class People(models.Model):
    name = models.CharField(max_length=200, default='')
    place = models.ForeignKey(Place, null=True, blank=True,  on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

