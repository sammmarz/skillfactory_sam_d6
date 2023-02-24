from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, UpdateView, CreateView, DetailView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Post,Category
from .filters import NewsFilter
from .forms import NewsForm
from django.contrib.auth.models import User
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail


class NewsList(ListView):
	model = Post
	template_name = 'news_list.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
	context_object_name = 'newsall'
	queryset = Post.objects.order_by('-creationTime')
	paginate_by = 5

	def post(self, request, *args, **kwargs):
		category_id = request.POST['cat']
		re = Post.objects.filter(textCategory=category_id)
		ca = Category.objects.all()
		cat_name = request.POST['btn']

		return render(request, 'news_list.html', {'posts': re, 'categ': ca, 'cat_name': cat_name})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categ'] = Category.objects.all()
		return context


class NewsSearch(ListView):
	model = Post
	template_name = 'search.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
	context_object_name = 'newsSearch'
	queryset = Post.objects.order_by('-creationTime')
	paginate_by = 1

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['filter'] = NewsFilter(self.request.GET,
		queryset=self.get_queryset())  # вписываем наш фильтр в контекст
		return context


# дженерик для получения деталей о товаре
class NewsDetailView(DetailView):
	template_name = 'news.html'
	context_object_name = 'news'
	queryset = Post.objects.all()



# дженерик для создания объекта. Надо указать только имя шаблона и класс формы который мы написали в прошлом юните. Остальное он сделает за вас
class NewsCreateView(PermissionRequiredMixin, CreateView):
	permission_required = ('news.add_post',)
	template_name = 'news_create.html'
	form_class = NewsForm


# дженерик для редактирования объекта
class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	permission_required = ('news.change_post',)
	template_name = 'news_create.html'
	form_class = NewsForm

	def get_object(self, **kwargs):
		id = self.kwargs.get('pk')
		return Post.objects.get(pk=id)


# дженерик для удаления товара
class NewsDeleteView(DeleteView):
	template_name = 'news_delete.html'
	queryset = Post.objects.all()
	success_url = '/news/'

class BaseRegisterView(CreateView):
	model = User
	form_class = BaseRegisterForm
	success_url = '/'

@login_required
def upgrade_me(request):
	user = request.user
	premium_group = Group.objects.get(name='authors')
	if not request.user.groups.filter(name='authors').exists():
		premium_group.user_set.add(user)
	return redirect('/')

@login_required
def Subscribers(request):
	user = request.user
	if request.POST['sub']:
		subs = request.POST['sub']
		category_sub = Category.objects.get(categoryName=subs)
		category_sub.subscribers.add(user.id)
		category_sub.save()
	return redirect('/')