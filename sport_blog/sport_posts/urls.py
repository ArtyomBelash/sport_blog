from django.urls import path
from .views import *

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('post/<slug:slug>/', PostDetail.as_view(), name='detail'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('add/', AddPostView.as_view(template_name='spot_posts/add_post.html'), name='add_post'),
    path('search', SearchView.as_view(), name='search'),
    path('authors/<int:authors_id>/', AuthorPostView.as_view(), name='authors'),
    path('add_bookmark/<slug:post_slug>/', AddBookmark.as_view(), name='add_bookmark'),
    path('remove_bookmark/<slug:post_slug>/', RemoveBookmark.as_view(), name='remove_bookmark'),
    path('bookmarks/', BookmarksView.as_view(), name='bookmarks'),

]
