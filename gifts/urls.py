from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView

app_name = 'gifts'

urlpatterns = [
    # ex: /hello/
    path('signup', views.signup, name='signup'),

    path('', views.MemberListView.as_view(), name='all'),

    path('gift/<int:pk>', views.GiftDetailView.as_view(), name='gift_detail'),

    path('gift/create',
        views.GiftCreateView.as_view(success_url=reverse_lazy('gifts:all')), name='gift_create'),

    path('gift/gift_link_create',
        views.GiftCreateFromLinkView.as_view(success_url=reverse_lazy('gifts:all')), name='gift_link_create'),

    path('gift/<int:pk>/update',
        views.GiftUpdateView.as_view(success_url=reverse_lazy('gifts:all')), name='gift_update'),

    path('gift/<int:pk>/delete',
        views.GiftDeleteView.as_view(success_url=reverse_lazy('gifts:all')), name='gift_delete'),

    path('gift_picture/<int:pk>', views.stream_file, name='gift_picture'),

    path('gift/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='gift_comment_create'),

    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(success_url=reverse_lazy('gifts:all')), name='gift_comment_delete'),

    path('gift/<int:pk>/favorite',
        views.AddFavoriteView.as_view(), name='gift_favorite'),

    path('gift/<int:pk>/unfavorite',
        views.DeleteFavoriteView.as_view(), name='gift_unfavorite'),

    path('user/<int:pk>', views.MemberGiftListView.as_view(), name ='member_gift_list'),
    path('users/', views.MemberListView.as_view(), name ='member_list'),

     path('jsondata',views.ReportJsonData,name = "jsondata"),

]

