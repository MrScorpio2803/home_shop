from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import CreateMessageForm
from .models import FeedbackMessage


class CreateFeedbackMessageView(View):

    def get(self, req):
        return redirect('/')

    def post(self, req):

        form = CreateMessageForm(data=req.POST)
        # print(form.cleaned_data)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = req.user
            feedback.save()
            messages.success(req, 'Ваше обращение успешно зарегистрировано!')
        else:
            print(form.errors)
        return redirect('main:about_contact')

# Create your views here.
