from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
#def index(request):
  # return render(request, 'ecgpt/index.html')

import openai
from django.http import JsonResponse
openai.api_key = "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"
model_engine = "text-davinci-002"


def index(request):
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
        return render(request, 'ecgpt/index.html', {'question': prompt, 'answer': reply})
    return render(request, 'ecgpt/index.html')






