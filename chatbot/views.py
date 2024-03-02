from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User

# Create your views here.

openai_api_key = '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'
openai.api_key = openai_api_key

def ask_openai(message):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    print(response)
    answer = response.choices[0].message.content.strip()
    return answer

def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                login(request, user)
                return redirect('chatbot')
            except Exception as e:
                print(e)
                error_message = "Error creating account"
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = "Passwords don't match"
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout_user(request):
    return logout(request)