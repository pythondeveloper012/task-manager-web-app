from django.urls import path
from .views import Get_Post_Users_Data, User_Update_and_Delete_view, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'tasks'

urlpatterns = [
    path('', Get_Post_Users_Data.as_view(), name='task-list'),
    path('<int:pk>/', User_Update_and_Delete_view.as_view(), name='task-detail'),

    # register
    path("register/", RegisterView.as_view(), name="register"),

    # JWT login
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # JWT refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
