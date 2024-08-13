from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import tensorflow as tf
import numpy as np
import librosa
import json
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
@csrf_exempt
@api_view(['POST'])
def detect_audio(request):
    if request.method == 'POST':
        # Save the uploaded file
        audio_file = request.FILES['file']
        file_path = default_storage.save('temp.wav', ContentFile(audio_file.read()))
        
        # Load the TFLite model
        model = tf.lite.Interpreter(model_path=os.path.join("./models/model.tflite"))
        classes = [ "Axe", "BirdChirping", "Chainsaw", "Clapping", "Fire", "Firework", "Footsteps", "Frog", "Generator", "Gunshot", "Handsaw", "Helicopter", "Insect", "Lion", "Rain", "Silence", "Speaking", "Squirrel", "Thunderstorm", "TreeFalling", "VehicleEngine", "WaterDrops", "Whistling", "Wind", "WingFlaping", "WolfHowl", "WoodChop" ]

        # Load the audio file
        waveform, sr = librosa.load(file_path, sr=16000)

        if waveform.shape[0] % 16000 != 0:
            waveform = np.concatenate([waveform, np.zeros(16000 - waveform.shape[0] % 16000)])

        # Prepare the model input
        input_details = model.get_input_details()
        output_details = model.get_output_details()

        model.resize_tensor_input(input_details[0]['index'], (1, len(waveform))) 
        model.allocate_tensors()

        model.set_tensor(input_details[0]['index'], waveform[None].astype('float32'))
        model.invoke()

        class_scores = model.get_tensor(output_details[0]['index'])
        predicted_class = classes[class_scores.argmax()]

        # Clean up the temporary file
        default_storage.delete(file_path)

        return Response({'class': predicted_class, 'scores': class_scores.tolist()}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid request method'}, status=status.HTTP_404_NOT_FOUND)
