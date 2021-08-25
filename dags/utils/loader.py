from google.cloud import storage
from fastai.vision import *
from utils.train import train
import torch
import os
import warnings

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "sa.json"

storage_client = storage.Client()

bucket_to = storage_client.bucket("animals_all")

path = 'images2retrain/'

for i in storage_client.list_blobs("animals_all"):
    i.download_to_filename(path+i.name.split('/')[-1])





def perekiduvach():
    storage_client = storage.Client ()

    bucket_all = storage_client.bucket ("animals_all")
    bucket_to = storage_client.bucket ("animals_to_predict")

    list_classes = list (dict.fromkeys (
        [ i.name.replace (i.name.split ('_') [ -1 ], '') for i in storage_client.list_blobs ("animals_all") ]).keys ())
    list_classes = [ i [ :-1 ] for i in list_classes if len (i) > 2 ]

    for i in list_classes:
        for j in storage_client.list_blobs("animals_all"):
            if j.name.startswith(i):
                blob_copy = bucket_all.copy_blob (
                    j, bucket_to, f"{i}/{j.name}")

    return 0


def predictor(model='resnet34'):

    warnings.filterwarnings ('ignore')

    storage_client = storage.Client()
    bucket_from = storage_client.bucket ("animals_to_predict")
    bucket_to = storage_client.bucket ("animals_predicted")

    learn = load_learner('/home/airflow/gcs/dags/utils/model/', f'{model}.pkl')
    for i in storage_client.list_blobs("animals_to_predict"):

        i.download_to_filename(i.name.split('/')[-1])
        img = open_image(i.name.split('/')[-1])

        pred_class, pred_idx, outputs = learn.predict (img)
        pred_name = ''
        for name, _class in learn.data.c2i.items():
            if _class == pred_class.data.item():
                pred_name = name
                print ('this is ', name, ' with ', round (torch.max (outputs).item (), 4)*100, '% ', 'probability')

        new_blob = bucket_to.blob(f"{pred_name}/{i.name.split('/')[-1]}")
        new_blob.upload_from_filename(i.name.split('/')[-1])

        print (
            "File {} uploaded to {}.".format (
                i.name.split('/')[-1], f"{pred_name}/"
            )
        )

    return 0

def retrainer(model='resnet34'):
    batch_size = 64
    path_img = '/images2retrain/'

    storage_client = storage.Client()

    bucket = storage_client.bucket("images_to_retrain")

    for i in storage_client.list_blobs("animals_to_predict"):
        i.download_to_filename(path_img + i.name.split('/')[-1])

    fnames = get_image_files(path_img)
    np.random.seed(42)
    pat = r'/([^/]+)_\d+.jpg$'

    print('creating dataset...')
    data = ImageDataBunch.from_name_re(path_img, fnames, pat, ds_tfms=get_transforms(), size=224,
                                       bs=batch_size).normalize(imagenet_stats)
    learn = load_learner(path='model/model.pkl')
    train(data, learn)

    os.replace("../../data/models/export.pkl", "model/model.pkl")
    print('Retrain: Done.')