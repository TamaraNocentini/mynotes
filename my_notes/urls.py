from django.urls import path

from my_notes.views import MyNotesListView, index, MyNotesCreateView, \
    MyNotesDetailView, MyNotesUpdateView, MyNotesDeleteView, export_my_notes

app_name = 'my_notes'

urlpatterns = [
    path('', index, name='index'),
    path('list/', MyNotesListView.as_view(), name='list'),
    path('new/', MyNotesCreateView.as_view(), name='new'),
    path('<int:pk>/view/', MyNotesDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', MyNotesUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', MyNotesDeleteView.as_view(), name='delete'),
    path('export/', export_my_notes, name='export'),
]
