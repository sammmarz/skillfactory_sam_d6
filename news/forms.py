from django.forms import ModelForm, BooleanField
from .models import Post,Category,PostCategory
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

# Создаём модельную форму
class NewsForm(ModelForm):
    class Meta:
        model = Post
        fields = ['header', 'textCategory', 'authorArticle', 'postText']


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user