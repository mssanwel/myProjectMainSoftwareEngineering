from django.urls import path

from . import views
app_name='polls'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),

    # ex: /polls/5/results/
    path('getData/', views.getData, name='getData'),

    #ex: /polls/5/
    path('searchData/', views.searchData, name='searchData'),

    # ex: /polls/5/results/
    path('addData/', views.addData, name='addData'),

    # ex: /polls/5/vote/
    path('saveLocation/', views.saveLocation, name='saveLocation'),
]
