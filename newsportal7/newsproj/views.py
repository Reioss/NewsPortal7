from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.decorators import login_required
from .models import New, Category, NewCategory, Author
from .filters import New_Filter, Search_Filter
from .forms import NewForm, UpdateProfileForm, BasicSignupForm, SocialSignupForm
from django.shortcuts import reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.signals import post_save
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from .models import BaseRegisterForm

class NewsList(ListView):
    model = New
    ordering = 'name'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10 # вот так мы можем указать количество записей на странице

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = New_Filter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        context['filterset'] = New_Filter (self.request.GET, queryset=self.get_queryset())
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписаны на категорию новостей'
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})


class NewDetail(DetailView):
    model = New
    template_name = 'new.html'
    context_object_name = 'new'

    def get_absolute_url(self):
        return f'/news/'


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        authors_group.user_set.add(user)
    return redirect('news/')


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'newsproj/upgrade.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

# Добавляем новое представление для создания товаров.
class NewCreate(CreateView):
    form_class = NewForm
    model = New
    template_name = 'news_create.html'
    permission_required = 'news.add_new, new.change_new'


    def create_new(request):
        form_class = NewForm()

        if request.method == 'POST':
            form_class = NewForm(request.POST)
            if form_class.is_valid():
                form_class.save()
                return HttpResponseRedirect('/news/')
        return render(request, 'news_create.html', {'form':form})


class NewSearch(ListView):
    model = New
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 2


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = Search_Filter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        context['filterset'] = Search_Filter (self.request.GET, queryset=self.get_queryset())
        return context


class NewDelete(DeleteView):
    model = New
    template_name = 'delete.html'
    success_url = reverse_lazy('news_list')

class NewUpdate(UpdateView):
    form_class = NewForm
    model = New
    template_name = 'news_create.html'
    success_url = reverse_lazy('home')

class ProfileUserUpdate(LoginRequiredMixin, UpdateView):
    form_class = UpdateProfileForm
    model = User
    template_name = 'profile_edit.html'
    success_url = reverse_lazy('home')

class CategoryListView(ListView):
    model = New
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category_new = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = New.objects.filter(category=self.category).order_by('-date_create')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category_new.subscribers.all()
        context['category_new'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category_new = Category.objects.get(id=pk)
    category_new.subscribers.add(user)

    message = 'Вы успешно подписаны на категорию новостей'
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})



