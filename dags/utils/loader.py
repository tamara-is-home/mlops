from google.cloud import storage
#from fastai.vision import *
#import torch
import os
import warnings

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "sa.json"

storage_client = storage.Client()

bucket_to = storage_client.bucket("animals_to_predict")

[print(i) for i in storage_client.list_blobs("animals_to_predict")]



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

    learn = load_learner ('/home/airflow/gcs/dags/utils/model/', f'{model}.pkl')
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
    #1. take data from bucket("animals to predict")
    #2. retrain model
    #3. replace old model with new one, old model lies in dags/utils/model/
    pass
