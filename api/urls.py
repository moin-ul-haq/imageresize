from django.urls import path
from .views import UploadImageView,TaskStatusView,TaskResultView

urlpatterns = [
    path('upload/',UploadImageView.as_view(),name='upload'),
    path('status/<str:task_id>/',TaskStatusView.as_view(),name='check_status'),
    path('result/<str:task_id>/',TaskResultView.as_view(),name='check_result'),
]
