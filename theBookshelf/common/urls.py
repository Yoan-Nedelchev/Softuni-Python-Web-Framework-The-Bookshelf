from django.urls import path

from theBookshelf.common.views import index, search, CreateFeedbackView, about_us, statistics

urlpatterns = (
    path('home', index, name='index'),
    path('search/', search, name='search'),
    path('feedback/', CreateFeedbackView.as_view(), name='feedback'),
    path('about/', about_us, name='about'),
    path('statistics/', statistics, name='statistics'),
)
