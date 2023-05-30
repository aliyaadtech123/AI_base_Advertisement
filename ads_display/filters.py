# import django_filters
# from ads_display import models
# from django_filters import rest_framework as filters

# class Humanfilter(django_filters.FilterSet):
#     Date = django_filters.DateFilter(
#         label="Date",
#         method="filter_by_date",
#     )
#     def filter_by_date(self,queryset,name,value):
#         print(value)
#         return queryset.filter(Date=value)
        
#     class Meta:
#         model = models.humans
#         fields = ["Date"]