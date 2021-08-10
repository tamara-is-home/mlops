from fastai.vision import *
import torch
import warnings
import os

warnings.filterwarnings('ignore')


def predict(path_to_image: str, model: str = 'restnet34'):

    learn = load_learner(path=f'./models/{model}.pkl')
    img = open_image(path_to_image)

    pred_class, pred_idx, outputs = learn.predict(img)

    for name, _class in learn.data.c2i.items():
        if _class == pred_class.data.item():
            print('this is ', name, ' with ', round(torch.max(outputs).item(), 4)*100, '% ', 'probability')


if __name__ == '__main__':
    predict('data/test/Abyssinian_138.jpg')
