from rest_framework import viewsets
from ads_display import serializer
from .models import humans
from django.shortcuts import render
from rest_framework.response import Response

class data(viewsets.ModelViewSet):
    queryset = humans.objects.all()
    serializer_class = serializer.DataSerializers
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = {'Result': serializer.data}
        return Response(data)
# class stude(APIView):
#        def delete(self,request,key=None):
#         data=humans.objects.get(pk=key)
#         data.delete()
#         return Response({'msg':'Data detete'})       
 