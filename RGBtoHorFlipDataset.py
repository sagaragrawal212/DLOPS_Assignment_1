import torch
from torchvision import datasets, transforms
from skimage import color
import os
from PIL import Image
import glob
import numpy as np
from torch.utils.data import Dataset, DataLoader, random_split
import matplotlib.pyplot as plt

# Define Batch size
batch_size = 32

# Define the percentage of data to be used for validation
validation_split = 0.2

class HorizontalFlip:
    def __call__(self, image):
        return image.transpose(Image.FLIP_LEFT_RIGHT)


class RGBtoHorFlipDataset(Dataset):
    def __init__(self, root, rgb_transform=None):

        self.root = root
        self.rgb_transform = rgb_transform
        self.Hflip = HorizontalFlip()
        self.pil_to_tensor = transforms.ToTensor()
        self.image_list = [img_path for img_path in glob.glob(f"{self.root}/*/*/*") if (img_path.endswith('.jpg') | img_path.endswith('.jpeg'))]

    def __len__(self):
        return len(self.image_list)

    def __getitem__(self, idx):

        image_path = self.image_list[idx]

        rgb_image = Image.open(image_path).convert('RGB')

        rgb_image_transformed = self.preprocess(rgb_image)

        hflip_image = self.Hflip(rgb_image_transformed)

        return {"input_image" : self.pil_to_tensor(rgb_image_transformed),
                "output_image" : self.pil_to_tensor(hflip_image)}

    def preprocess(self,rgb_image) :
      # Transformations on rgb image
      if self.rgb_transform :
        rgb_image_transformed = self.rgb_transform(rgb_image)
      return rgb_image_transformed
