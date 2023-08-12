from django.urls import path
from .views import MainPageView, QuestionPageView, CreateQuestionView, CategoriesPageView, UserPageView, edit_record, \
    delete_record, CreatePostView, PostPageView, PostAllPageView

urlpatterns = [
    path('', MainPageView.as_view()),
    path('question/<int:pk>', QuestionPageView.as_view()),
    path('ask-question/', CreateQuestionView.as_view()),
    path('categories/', CategoriesPageView.as_view()),
    path('profile/', UserPageView.as_view()),
    path('edit/<record>/<int:record_id>', edit_record),
    path('delete/<record>/<int:record_id>', delete_record),
    path('create-post/', CreatePostView.as_view()),
    path('posts', PostAllPageView.as_view()),
    path('post/<int:pk>', PostPageView.as_view())
]
