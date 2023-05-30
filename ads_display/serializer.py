from rest_framework import serializers
from ads_display import models

class DataSerializers(serializers.ModelSerializer):
       class Meta:
             model=models.humans
             fields="__all__"