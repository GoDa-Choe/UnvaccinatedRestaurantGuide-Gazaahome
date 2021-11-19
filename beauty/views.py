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

from collections import Counter

from bisect import bisect_left


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

        grade = get_grade(face.score, face.gender)
        full_start, half_star, empty_star = get_star(score)

        # for chart
        rank_obj = Rank(face.score)
        my_rank, counter, length = rank_obj.get_rank_and_counter_length()

        chart_data, colors = generate_chart_data(counter, length, face.score)

        context_data = {
            "face": face,

            "full_start": full_start,
            "half_star": half_star,
            "empty_star": empty_star,

            "grade": grade,

            "rank": my_rank,
            "length": length,
            "percent": round(my_rank / length, 2),

            "chart_data": chart_data,

            "colors": colors,
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


def get_grade(norm_score, gender):
    if gender == "m":
        if norm_score >= 4:
            grade = "존잘"
        elif norm_score >= 3.5:
            grade = "훈남"
        elif norm_score >= 3.0:
            grade = "흔남"
        else:
            grade = " "
    else:
        if norm_score >= 4:
            grade = "존예"
        elif norm_score >= 3.5:
            grade = "훈녀"
        elif norm_score >= 3.0:
            grade = "흔녀"
        else:
            grade = " "

    return grade


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


class Rank:
    def __init__(self, my_score):
        self.my_score = my_score

    @staticmethod
    def get_scores():
        faces_iter = Face.objects.all()

        scores = [face.score for face in faces_iter]

        return scores

    @staticmethod
    def rank(counter, my_score):
        unrepeated_sorted_scores = sorted(counter.keys(), reverse=True)
        for i in range(len(unrepeated_sorted_scores)):
            if my_score == unrepeated_sorted_scores[i]:
                return i + 1

        return 10

    def get_rank_and_counter_length(self):
        scores = self.get_scores()
        counter = Counter(scores)

        my_rank = self.rank(counter, self.my_score)

        return my_rank, counter, len(scores)


def generate_chart_data(counter, length, my_score):
    for score in counter.keys():
        counter[score] = round(counter[score] / length * 100, 2)

    x_data = [score for score in counter.keys()]
    y_data = [percent for percent in counter.values()]
    r_data = generate_r_data(y_data)
    colors = generate_colors(x_data, my_score)

    chart_data = [{"x": x_data[i], "y": y_data[i], "r": r_data[i]} for i in range(len(x_data))]

    return chart_data, colors


def generate_colors(x_data, my_score):
    others_color = 'rgb(255, 99, 132)'
    my_color = 'rgb(51,144,205)'

    colors = [others_color] * len(x_data)

    my_index = 0
    for i in range(len(x_data)):
        if my_score == x_data[i]:
            my_index = i
            break

    colors[my_index] = my_color

    return colors


def generate_r_data(y_data):
    min_val = min(y_data)
    max_val = max(y_data)

    r = [normalization(percent, min_val, max_val, 3, 12) for percent in y_data]

    return r


def normalization(x, min_val, max_val, min_target, max_target):
    return (x - min_val) / (max_val - min_val) * (max_target - min_target) + min_target
