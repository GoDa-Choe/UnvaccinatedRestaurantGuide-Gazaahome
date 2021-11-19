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
        form.instance.author = self.request.user
        face = form.save()

        predictor = get_resnet18()

        with torch.no_grad():
            image = get_image(face.face.url)
            score = predictor(image).item()
            face.score = normalize_score(score)

        face.save()

        full_start, half_star, empty_star = get_star(score)

        context_data = {
            "face": face,
            "full_start": full_start,
            "half_star": half_star,
            "empty_star": empty_star,
        }

        return render(self.request, template_name="beauty/result.html",
                      context=context_data)


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


def get_star(score):
    integer = round(score)
    floating = score - integer

    full_star = integer
    half_star = 0

    if floating > 0.75:
        full_star += 1
    elif floating > 0.25:
        half_star += 1

    empty_star = 5 - (full_star + half_star)
    return full_star, half_star, empty_star
