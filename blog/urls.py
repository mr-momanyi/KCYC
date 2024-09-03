from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .import views
from django.conf import settings
from django.conf.urls.static import static
from .views import search

app_name = 'blog'
# django admin customization
admin.site.site_header = "Kenya Climate Youth Corps"
admin.site.site_title = "Dashboard"
admin.site.index_title = "Kenya Climate Youth Corps Portal"
   
urlpatterns = [
    path('', views.post_home, name = 'post_home'),

    path('post/', views.post_list, name='post_list'),

    path('post/<slug:slug>/', views.post_detail, name='post_detail'),

    path('article/', views.article_list, 
          name = 'article_list'),

    path('article/<slug:slug>/', views.article_detail, name = 'article_detail'),
    

    path('updates/', views.post_updates, 
         name = 'post_updates'),

    path('about/', views.post_about, name = 'post_about'),

    path('contact/', views.post_contact, name = 'post_contact'),

    path('join/', views.join_us, name = 'join'),
    

    # path('login/', auth_views.LoginView.as_view(), name='login'),

    path('logout/', views.logout_confirmation_view, name = 'logout'),
    path('logout-success/', views.logout_success_view, name = 'logout_success'),
    # path('logout_success/', auth_views.LogoutView.as_view(next_page = 'post_home'), name = 'logout_success' ),


#  search query url
    path('search/', views.search, name='search'),
    
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
    
    #change password urls
    # path('password_change', auth_views.PasswordChangeView.as_view(), name = 'password_change'),
    # path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),
        #   name = 'password_change_done'),

    # reset password urls
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),


    path('', include('django.contrib.auth.urls')),
#     path('', views.dashboard, name = 'dashboard'),  this covered by home.html
    path('register/', views.register, name = 'register'),
    path('edit/', views.edit, name='edit'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:article_id>/share/', views.article_share, name='article_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('<int:article_id>/comment/', views.article_comment, name='article_comment'),
    path('library/', views.library, name = 'library'),
    path('courses/', views.courses, name = 'courses'),
    path('services/', views.services, name = 'services'),
    path('causes/', views.causes, name = 'causes'),
    path('effects/', views.effects, name = 'effects'),
    path('solutions/', views.solutions, name = 'solutions'),
    
]
 



