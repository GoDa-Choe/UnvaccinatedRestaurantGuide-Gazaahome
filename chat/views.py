from django.shortcuts import render
from django.views.generic import TemplateView
import random
import requests


# Create your views here.
class TestChatView(TemplateView):
    template_name = 'chat/test.html'

    def get_context_data(self, **kwargs):
        context = super(TestChatView, self).get_context_data()

        if self.request.user.is_superuser:
            user = {
                'id': "123456",
                'name': "goda",
                'email': "goda.soft.studio@gmail.com",
                'phto_url': "https://res.cloudinary.com/hyzq6bxmk/image/upload/v1641144411/static/goda%20soft%20studio/logo_godo_kftbb0.png",
                'welcomeMessage': "라이브 채팅 테스트입니다.",
                'role': "admin"
            }
            context['is_superuser'] = True
        else:
            user = {
                'id': f"{random.randint(1, 100_000)}",
                'name': "익명",
                'role': "general"
            }
            context['is_superuser'] = False

        context.update(user)
        return context


def leave(request, id):
    url = f'https://api.talkjs.com/v1/tsLI8nZv/conversations/TEST004/participants/{id}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer sk_test_QR6RsbOJ3A8rW1ZnNlGrZui7a8D5OZ4S'
    }
    reponse = requests.delete(url=url, headers=headers)

    context = {
        'reponse': reponse.content
    }

    return render(
        request,
        'chat/leave.html',
        context
    )
