from django.urls import path

from .views import index, BbByRubricView,nologin, BbDetailView,BbAddView,BbEditView,BbDeleteView,BbIndexView,search

app_name='bboard'
urlpatterns = [
    path('add/', BbAddView.as_view(), name='add'),
    path('bboard/nologin/', nologin, name='nologin'),
    # path('day/', BbIndexView.as_view(), name='day'),
    path('edit/<int:pk>/', BbEditView.as_view(), name='edit'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),
    path('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('bboard/search/', search, name='search'),


    path('', index, name='index'),
]
