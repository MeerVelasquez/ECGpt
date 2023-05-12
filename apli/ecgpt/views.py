from json import dumps
import json
from django.shortcuts import render
from django.http import JsonResponse
from ecgpt.models import EcgData
from django.http import HttpResponse
from django.template import loader
from django.db.models import Count
from django.core import serializers
import openai

openai.api_key = "#"


def home(request):
    return render(request, 'ecgpt/index.html')


def chatbot(request):
    if request.method == 'POST':
        input_text = request.POST.get('input_text')

        # Send the user's input to the GPT-3.5-Turbo API
        response = openai.Completion.create(
            engine="davinci",
            prompt=input_text,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # Get the response text from the API response
        response_text = response.choices[0].text.strip()

        # Return the response as a JSON object
        return JsonResponse({'response_text': response_text})

    return render(request, 'ecgpt/chatbot.html')

def dashboard(request):
    queryset = EcgData.objects.all()
    data = list(queryset.values())
    json_data = json.dumps(data)
    return render(request, 'ecgpt/dashboard.html', {'data': json_data})

def patients(request):
    info_patients = EcgData.objects.all().values()
    excluded_column = 'diagnosis'
    columns = [field.verbose_name for field in EcgData._meta.fields if field.name != excluded_column]
    return render(request, 'ecgpt/patients.html', {'data': info_patients, 'columns': columns})
