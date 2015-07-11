from django.db import models

class VMServer(models.Model):
    name = models.CharField(max_length=30)
    ip = models.CharField(max_length=30)
    mac = models.CharField(max_length=30)
    hostserverip = models.CharField(max_length=30)
    os = models.CharField(max_length=30)
    vmstatus = models.CharField(max_length=30)

    
    def __unicode__(self):
        return self.name
