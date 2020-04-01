"""/**
 * Models definition file for exchanges app
 *
 * @summary Models definition file for exchanges app
 * @author Zeppelin17 <elzeppelin17@gmail.com>
 *
 * Created at     : 2020-04-01 06:43:26 
 * Last modified  : 2020-04-01 06:44:15
 */"""

from django.db import models
from django.utils import timezone

class Exchange(models.Model):
    name = models.CharField(max_length=50)
    api_endpoint = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    """def updatePairs(self):
        #Código para hacer nueva llamada API y guardar nuevos datos
        return"""
    
    def __str__(self):
        return self.name