import torch
import torch.nn as nn 
from torchvision import models, transforms
from PIL import Image
import os

# initialise model once
_device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

# pretrained ResNet50 backbone (without classification head)
