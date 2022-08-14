from django.urls import path
from places import views
from places.views import RequestPasswordResetEmail, SetNewPasswordView

urlpatterns = [
    path('', views.PlaceView.as_view()),
    path('<int:id>', views.PlaceSingleView.as_view()),
    path('agregarComentario/', views.ComentarioView.as_view()),
    path('eliminarComentario/<int:id>', views.EliminarComentarioView.as_view()),
    path('registrar/', views.UserSignUpView.as_view()),
    path('obtener/', views.UsersListView.as_view()),
    path('editar/<int:id>', views.UpdatePerfilView.as_view()),
    path('restablecer-password/', views.RequestPasswordResetEmail.as_view(), name="restablecer-password"),
	path('restablecimiento-completo/', views.SetNewPasswordView.as_view(), name="restablecimiento-completo"),
    path('login/', views.LoginView.as_view()),

]