from django.shortcuts import render
from django.http import JsonResponse
import openai

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
