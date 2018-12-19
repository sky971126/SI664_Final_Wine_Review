from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('wine/', views.WineListView.as_view(), name='wine'),
    path('wine/<int:pk>/', views.WineDetailView.as_view(), name='wine_detail'),
    path('review/', views.ReviewListView.as_view(), name='review'),
    path('review/<int:pk>/', views.ReviewDetailView.as_view(), name='review_detail'),
    path('wine/new/', views.WineCreateView.as_view(), name='wine_new'),
    path('wine/<int:pk>/delete/', views.WineDeleteView.as_view(), name='wine_delete'),
    path('wine/<int:pk>/update/', views.WineUpdateView.as_view(), name='wine_update'),
    path('wine/filter', views.WineFilterView.as_view(), name='filter'),
]
