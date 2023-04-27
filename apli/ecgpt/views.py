from django.shortcuts import render
from django.http import JsonResponse
import openai


openai.api_key = "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"
model_engine = "davinci"


def index(request):
    return render(request, 'ecgpt/index.html')


def chatbot(request):
    if request.method == 'POST':
        prompt = request.POST.get('question')
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        reply = response.choices[0].text.strip()
        return render(request, 'ecgpt/chatbot.html', {'question': prompt, 'answer': reply})
    return render(request, 'ecgpt/chatbot.html')


def dashboard(request):
    return render(request, 'ecgpt/dashboard.html')
