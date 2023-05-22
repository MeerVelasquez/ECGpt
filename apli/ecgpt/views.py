from json import dumps
import json
from django.shortcuts import render
from django.core.paginator import Paginator
from ecgpt.models import EcgData
import joblib
import openai
import numpy as np

openai.api_key = "#"
model_engine = "davinci"
models = joblib.load('ecgpt/modelos/ecgpt/models.joblib')



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
    paginator = Paginator(info_patients, 15)  # Muestra 10 pacientes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'ecgpt/patients.html', {'data': info_patients, 'columns': columns, 'page_obj': page_obj})

def testModelo(request):
    if request.method == 'POST':
        selected_model = request.POST.get('model')
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
        print(selected_model)
        
        # Load the trained model and use it to make a prediction
        if selected_model == 'dtc_model':
            model1 = models[0]  
            result = model1.predict(inputs)
            model_name = 'Decision Tree Classifier'
            if result[0] in label_names:
                result = label_names[result[0]]
            else:
                result = "Unknown"
            
        elif selected_model == 'svm_model':
            model2 = models[1]  
            result = model2.predict(inputs)
            model_name = 'Support vector machine'
            if result[0] in label_names:
                result = label_names[result[0]]
            else:
                result = "Unknown"
            # Resto del código para model2...
        elif selected_model == 'rf_model':
            model3 = models[2]  
            result = model3.predict(inputs)
            model_name = 'Random Forest'
            if result[0] in label_names:
                result = label_names[result[0]]
            else:
                result = "Unknown"

        Ecg_data_new = EcgData()
        Ecg_data_new.age = input1
        Ecg_data_new.sex = input2
        Ecg_data_new.height = 60
        Ecg_data_new.weight = input3
        Ecg_data_new.qrs_duration = input4
        Ecg_data_new.p_r_interval = input5
        Ecg_data_new.q_t_interval = input6
        Ecg_data_new.t_interval = input7
        Ecg_data_new.p_interval = input8
        Ecg_data_new.qrs = input9
        Ecg_data_new.t = input10
        Ecg_data_new.p = input11
        Ecg_data_new.qrst = input12
        Ecg_data_new.heart_rate = input13
        Ecg_data_new.q_wave = input14
        Ecg_data_new.r_wave = input15
        Ecg_data_new.s_wave = input16
        Ecg_data_new.label = result

        Ecg_data_new.save()

        return render(request, 'ecgpt/testModelo.html', {'result': result, 'model_name': model_name})
    # Render the initial form
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
