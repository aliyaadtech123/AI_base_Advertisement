from django.db import models

# Create your models here.
class humans(models.Model):
    Time=models.TimeField()
    Date=models.DateField()
    Total_Females=models.IntegerField(null=False)    
    Total_Males=models.IntegerField(null=False)    
    Total_attracted_humans=models.IntegerField(null=False)
    Total_present_humans=models.IntegerField(null=False) 
       