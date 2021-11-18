from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import CreateView, FormView

from beauty.models import Recode
from beauty.forms import RecordForm, TestForm

import torch
import torchvision
from PIL import Image
import requests
from facenet_pytorch import MTCNN
import time
from urllib import request
from io import BytesIO


class TestView(TemplateView):
    template_name = 'beauty/index.html'


class Test(FormView):
    form_class = TestForm
    template_name = 'beauty/create_record.html'

    def form_valid(self, form):
        current_user = self.request.user
        response = super(Test, self).form_valid(form)

        return redirect(reverse_lazy('beauty:result'))


class CreateRecord(CreateView):
    model = Recode
    form_class = RecordForm
    template_name = 'beauty/create_record.html'

    def form_valid(self, form):
        start = time.time()

        form.instance.score = 0.0
        form.instance.author = self.request.user
        new_recode = form.save()

        recode_save_time = time.time() - start

        start = time.time()

        model = self.get_resnet18()

        model_load_time = time.time() - start

        start = time.time()

        model.eval()

        with torch.no_grad():
            face, face_detection_time = self.get_image(new_recode.face.url)

            image_load_time = time.time() - start

            start = time.time()

            score = model(face)

        new_recode.score = score.item()

        predition_time = time.time() - start

        context_data = {
            "recode": new_recode,
            "form_raw_image": self.request.FILES['face'],

            "recode_save_time": recode_save_time,
            "image_load_time": image_load_time - face_detection_time,
            "face_detection_time": face_detection_time,
            "model_load_time": model_load_time,
            "predition_time": predition_time,
            "total_time": recode_save_time + image_load_time + model_load_time + predition_time
        }

        return render(self.request, template_name="beauty/index.html",
                      context=context_data)

    def get_resnet18(self):
        resnet18 = torchvision.models.resnet18()
        fc_in = resnet18.fc.in_features
        resnet18.fc = torch.nn.Linear(fc_in, 1)
        resnet18.load_state_dict(
            torch.load('beauty/static/beauty/weights/resnet18_weights_60.pth', map_location=torch.device('cpu')))

        resnet18.to(device=torch.device('cpu'))

        return resnet18

    def get_image(self, url):
        transform = torchvision.transforms.Compose([
            MTCNN(image_size=224),
        ])
        # path = requests.get(url, stream=True).raw
        # path = BytesIO(request.urlopen(url).read())
        path = BytesIO(requests.get(url).content)

        img = Image.open(path).convert('RGB')

        start = time.time()
        img = transform(img)
        face_detection_time = time.time() - start
        return img.unsqueeze(dim=0), face_detection_time
