from django.urls import path
from . import views

urlpatterns = [
    path('', views.view),
    path('new', views.new),
    path('edit/<int:wish_id>', views.edit),
    path('remove/<int:wish_id>', views.remove),
    path('update/<int:wish_id>', views.update),
    path('grant/<int:wish_id>', views.grant),
    path('like/<int:wish_id>', views.like),
    path('create', views.create),
    path('stats', views.stats),
]