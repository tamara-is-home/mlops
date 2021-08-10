from fastai.vision import *
from fastai.metrics import *
import warnings


warnings.filterwarnings('ignore')

def train(batch_size:int=16, model=models.resnet34, metric=error_rate, data_size:int=224):
    path = untar_data(URLs.PETS)
    path_img = path/'images'
    fnames = get_image_files(path_img)
    pat = r'/([^/]+)_\d+.jpg$'
    data = ImageDataBunch.from_name_re(path_img, fnames, pat, ds_tfms=get_transforms(), size=data_size, bs=batch_size)\
        .normalize(imagenet_stats)
    print('dataset has been created!')

    learn = cnn_learner(data, model, metrics=metric)
    learn.fit_one_cycle(1)
    print('one training cycle passed')

    name = model.__name__
    learn.save(name)
    learn.export(f'models/export.pkl')


if __name__ == '__main__':
    train()
