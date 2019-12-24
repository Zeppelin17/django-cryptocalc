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