from django.shortcuts import render
from django.views.generic import FormView

from beauty.models import Face
from beauty.forms import FaceForm

import torch
import torchvision
from PIL import Image
import requests
from facenet_pytorch import MTCNN
from io import BytesIO


class PredictView(FormView):
    model = Face
    form_class = FaceForm
    template_name = 'beauty/prediction.html'

    def form_valid(self, form):
        predictor = get_resnet18()
        form.instance.author = self.request.user
        face = form.save()

        with torch.no_grad():
            image = get_image(face.face.url)
            score = predictor(image)
            face.score = normalize_score(score.item())

        face.save()

        return render(self.request, template_name="beauty/result.html",
                      context={"face": face, })


def get_resnet18():
    resnet18 = torchvision.models.resnet18()
    fc_in = resnet18.fc.in_features
    resnet18.fc = torch.nn.Linear(fc_in, 1)
    resnet18.load_state_dict(
        torch.load('beauty/static/beauty/weights/resnet18_weights_60.pth', map_location=torch.device('cpu')))

    resnet18.to(device=torch.device('cpu'))
    resnet18.eval()

    return resnet18


def get_image(url):
    transform = torchvision.transforms.Compose([
        MTCNN(image_size=224),
    ])

    # path = requests.get(url, stream=True).raw
    # path = BytesIO(request.urlopen(url).read())
    path = BytesIO(requests.get(url).content)
    img = Image.open(path).convert('RGB')
    img = transform(img)

    return img.unsqueeze(dim=0)


def normalize_score(score):
    score = round(score, 1)

    if score > 5.0:
        score = 5.0
    elif score < 1.0:
        score = 1.0

    return score
