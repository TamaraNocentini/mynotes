from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.contrib.postgres.search import SearchVector

from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView,\
    DeleteView
from django.db.models import Q

from my_notes.models import Note


@login_required
def index(request):
    return HttpResponseRedirect(reverse('my_notes:list'))


class MyNotesListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        result = Note.objects.filter(
            added_by=self.request.user)
        if 'search_string' in self.request.GET:
            search_string = self.request.GET['search_string']
            result = result.annotate(
                search=SearchVector(
                    'title',
                    'content')
             )
            result = result.filter(
                Q(search=search_string) |
                Q(tags__overlap=search_string.split(',')))
        return result

    def get_context_data(self, *args, **kwargs):
        result = super().get_context_data(*args, **kwargs)
        if 'search_string' in self.request.GET:
            search_string = self.request.GET['search_string']
            result['search_string'] = search_string
        return result


class MyNotesDetailView(LoginRequiredMixin, DetailView):
    model = Note

    def get_queryset(self):
        return Note.objects.filter(
            added_by=self.request.user)


class MyNoteForm(ModelForm):
    class Meta:
        model = Note
        fields = [
            'title',
            'tags',
            'content'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.add_input(
            Submit(
                'submit',
                'Submit',
                css_class='button is-link'))
        self.helper.form_method = 'POST'


class MyNotesCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = MyNoteForm

    def form_valid(self, form):
        o = form.save(commit=False)
        o.added_by = self.request.user
        o.save()

        return redirect(o)


class MyNotesUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = MyNoteForm

    def get_queryset(self):
        return Note.objects.filter(
            added_by=self.request.user)

    def form_valid(self, form):
        o = form.save(commit=False)
        o.updated_by = self.request.user
        o.save()

        return redirect(o)


class MyNotesDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    success_url = reverse_lazy('my_notes:list')

    def get_queryset(self):
        return Note.objects.filter(
            added_by=self.request.user)


@login_required
def export_my_notes(request):
    result = serialize(
        'json',
        Note.objects.all().filter(added_by=request.user))
    return HttpResponse(result, content_type="application/json")
