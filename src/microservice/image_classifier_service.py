from io import BytesIO

import requests
import torch
from PIL import Image
from flask import Flask, request
from torchvision import transforms

app = Flask(__name__)

CIFAR_LABELS = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']


@app.route('/')
def index():
    return 'API Works!'


@app.route('/classify', methods=['POST'])
def classify():
    img_url = request.get_json()
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    model = torch.hub.load("chenyaofo/pytorch-cifar-models", "cifar10_resnet20", pretrained=True)
    model.eval()
    convert_tensor = transforms.ToTensor()
    img_tensor = convert_tensor(img).unsqueeze(0)
    response = model(img_tensor)
    top10 = torch.topk(response, 10)
    scores = {CIFAR_LABELS[idx]: top10.values.tolist()[0][idx] for idx in top10.indices.tolist()[0]}
    return scores
