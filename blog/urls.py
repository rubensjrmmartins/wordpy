from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('blog/', views.PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:slug>/', views.CategoryPostListView.as_view(), name='category'),
    path('tag/<slug:slug>/', views.TagPostListView.as_view(), name='tag'),
    path('page/<slug:slug>/', views.PageDetailView.as_view(), name='page_detail'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('theme.css', views.theme_css_view, name='theme_css'),
]
