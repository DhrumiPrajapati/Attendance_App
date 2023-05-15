from django import urls
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

# from .views import activate  

urlpatterns = [
    path('home/',views.home,name='home'),
    path('tlupdate/<int:pk>/', views.TLUpdate, name='TLUpdate'),
    path('tasklist/',views.tasklist,name='tasklist'),
    path('userdata',views.userdata,name='userdata'),

    path('ClientForm/',views.ClientForm,name='ClientForm'),
    path('cliupdate/<int:pk>', views.CliUpdate, name='CliUpdate'),
    path('ClientEntry/',views.ClientEntry,name='ClientEntry'),
    path('clidelete/<int:pk>/',views.ClientDelete, name='ClientDelete'),

    path('EmpForm',views.EmpForm,name='EmpForm'),
    path('empupdate/<int:pk>', views.EmpUpdate, name='EmpUpdate'),
    path('EmpEntry/',views.EmpEntry,name='EmpEntry'),
    path('empdelete/<int:pk>/',views.EmpDelete, name='EmpDelete'),

    path('CompanyDetail/',views.CompanyDetail,name='CompanyDetail'),
    path('companyupdate/<int:pk>', views.CompUpdate, name='CompUpdate'),
    path('CompanyEntry/',views.CompanyEntry,name='CompanyEntry'),
    path('compdelete/<int:pk>',views.CompDelete,name='CompDelete'),

    path('ProjectForm/',views.ProjectForm,name='ProjectForm'),
    path('prjupdate/<int:pk>', views.PrjUpdate, name='PrjUpdate'),
    path('ProjectEntry/',views.ProjectEntry,name='ProjectEntry'),
    path('prjdelete/<int:pk>/',views.ProjectDelete, name='ProjectDelete'),

    path('SrjrMapFormView/',views.SrjrMapFormView,name='SrjrMapFormView'),
    # path('mapupdate/<int:pk>', views.MapUpdate, name='MapUpdate'),
    path('SrjrEntry/',views.SrjrEntry,name='SrjrEntry'),
    path('mapdelete/<int:pk>',views.MapDelete,name='MapDelete'),

    # path('AttFormView/', views.AttFormView.as_view(), name='AttFormView'),
    path('AttFormView/',views.AttFormView,name='AttFormView'),
    path('AttEntry/',views.AttEntry,name='AttEntry'),


    # path('signin/',views.signin,name='signin'),
    path('',views.loginview,name='loginview'),
    path('loginview/',views.loginview,name='loginview'),
    # path('',login_required(views.loginview.as_view()), name='loginview'),
    path('logoutview/',views.logoutview,name='logoutview'),
    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'),  
    # path('activate/<uidb64>/<token>', views.activate, name='activate'),
    # path('change_password/',auth_views.PasswordChangeView.as_view(),name='change_password'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="reset_password.html"),name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"),name='password_reset_complete'),
    path('emp_home/',views.emp_home,name='emp_home'),
    # path('empupdateform/<int:pk>', views.EmpUpdateForm, name='EmpUpdateForm'),
    # path('',views.EmpList, name='EmpList'),
    # path('',views.ClientList, name='ClientList'),
    # path('',views.ProjectList, name='ProjectList'),
    # path('mapdelete/<int:pk>/',views.MapDelete, name='MapDelete'),
    # path('',views.MapList, name='MapList'),
]