from json import dumps
import json
from django.shortcuts import render
from django.http import JsonResponse
from ecgpt.models import EcgData
import joblib
import openai
import numpy as np

openai.api_key = "#"
model_engine = "davinci"
model = joblib.load('ecgpt/modelos/ecgpt/dt.joblib')


label_names = {
    1: "Normal",
    2: "Ischemic changes (Coronary Artery Disease) ",
    3: "Old Anterior Myocardial Infarction",
    4: "Old Inferior Myocardial Infarction",
    5: "Sinus tachycardy",
    6: "Sinus bradycardy",
    7: "Ventricular Premature Contraction",
    8: "Supraventricular Premature Contraction",
    9: "Left bundle branch block",
    10: "Right bundle branch block",
    11: "degree AtrioVentricular block ",
    12: "degree AV block",
    13: "Ischemic changes (Coronary Artery Disease)",
    14: "Left ventricule hypertrophy",
    15: "Atrial Fibrillation",
    16: "Others"
}

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
    queryset = EcgData.objects.all()
    data = list(queryset.values())
    json_data = json.dumps(data)
    return render(request, 'ecgpt/dashboard.html', {'data': json_data})


def patients(request):
    info_patients = EcgData.objects.all().values()
    excluded_column = 'diagnosis'
    columns = [
        field.verbose_name for field in EcgData._meta.fields if field.name != excluded_column]
    return render(request, 'ecgpt/patients.html', {'data': info_patients, 'columns': columns})

def testModelo(request):
    if request.method == 'POST':
        input1 = float(request.POST.get('input1'))
        input2 = float(request.POST.get('input2'))
        input3 = float(request.POST.get('input3'))
        input4 = float(request.POST.get('input4'))
        input5 = float(request.POST.get('input5'))
        input6 = float(request.POST.get('input6'))
        input7 = float(request.POST.get('input7'))
        input8 = float(request.POST.get('input8'))
        input9 = float(request.POST.get('input9'))
        input10 = float(request.POST.get('input10'))
        input11 = float(request.POST.get('input11'))
        input12 = float(request.POST.get('input12'))
        input13 = float(request.POST.get('input13'))
        input14 = float(request.POST.get('input14'))
        input15 = float(request.POST.get('input15'))
        input16 = float(request.POST.get('input16'))

        # Convert the inputs to a numpy array and reshape it
        inputs = np.array([input1, input2, input3, input4, input5, input6, input7, input8,
                          input9, input10, input11, input12, input13, input14, input15, input16]).reshape(1, -1)
        print(inputs)

        # Load the trained model and use it to make a prediction
        result = model.predict(inputs)
        print(result)

        if result[0] in label_names:
            result = label_names[result[0]]
        else:
            result = "Unknown"

        print(result)

        # Render the result on the same page
        return render(request, 'ecgpt/testModelo.html', {'result': result})

    return render(request, 'ecgpt/testModelo.html', {})


def preprocess(input_data):
    # Convert the input string to a numpy array
    input_array = np.array(input_data)

    # Perform any required preprocessing steps, such as scaling or encoding
    processed_array = some_preprocessing_function(input_array)

    return processed_array


def some_preprocessing_function(input_array):
    # convert the string array to int array
    input_array = input_array.astype(int)
    return input_array
