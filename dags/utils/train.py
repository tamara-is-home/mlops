from fastai.vision import *
from fastai.metrics import error_rate
import numpy as np
import warnings
warnings.filterwarnings('ignore')


def train(images=None, model=None, savedir='models/'):
    print('untaring data...')
    batch_size = 64
    # path = untar_data(URLs.PETS)


    path_img = 'data/images'
    print('geting files...')
    if images is None:
        fnames = get_image_files(path_img)
        np.random.seed(42)
        pat = r'/([^/]+)_\d+.jpg$'

        print('creating dataset...')
        data = ImageDataBunch.from_name_re(path_img, fnames, pat, ds_tfms=get_transforms(), size=224, bs=batch_size).normalize(imagenet_stats)
        print('learning...')
        learn = cnn_learner(data, models.resnet34, metrics=error_rate)
        learn.fit_one_cycle(1)
    else:
        learn = model
        learn.data = images
        learn.fit_one_cycle(1)

    name = 'model'

    print('saving ' + name + ' ...')

    learn.save(name)
    learn.export(savedir + 'model.pkl')
