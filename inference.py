from fastai.vision import *
import torch
import warnings
import os

warnings.filterwarnings('ignore')


def predict(path_to_image: str):

    learn = load_learner(path=f'./models/')
    img = open_image(path_to_image)

    pred_class, pred_idx, outputs = learn.predict(img)

    for name, _class in learn.data.c2i.items():
        if _class == pred_class.data.item():
            print('this is ', name, ' with ', round(torch.max(outputs).item(), 4)*100, '% ', 'probability')


if __name__ == '__main__':
    predict('images/test/Abyssinian_1.jpg')
