UCU MlOps project 

by Vladyslav Kutsuruk

Project overview:
1. The main resource I'm using to run my code is Airflow on GCP Composer. To use it, one should enable Composer API and 
set up cluster with Airflow on it and then install composer_requirements.txt. All the code that lies in this repo should
be moved to Airflow's DAGs bucket to run Airflow data + model pipeline. NOTE: Composer supports well only Airflow <= v.2 (there
is some v.3 beta but I didnt dare to use it) so some operators are outdated.
2. We have some kind of data warehouse which is GCS bucket 'animals_all', where we store all the data. 
We are versioning this data with DVC, making backups in that bucket by configuring ['remote "storage"']. 
I also have buckets 'animals_to_predict' - for data sorting and validation and 'animals_predicted' for model performance checks. 
3. The main Fastai model 'resnet34' is also versioned by DVC and is stored directly on cluster where Airflow runs. There are separate 
train and inference code in two versions: one is used to run in docker container and the second is used in
Airflow tasks. I've also experimented with VertexAI on GCP to gain an auto-ml solution (task 1.7), but that model doesnt take part
in Airflow's pipeline 'cause it requires to create more complicated operators to call VertexAI API for retraining and so on. 
3. The local pipeline (task 1) is the following (look dockerfile, rest_api.py, training.py and inference.py):

    3.1. We create docker image and build container.
    
    3.2. There we can manually retrain model and receive its prediction OR we can follow the localhost:5000 and
    check the model's performance with the simple rest api which allows to do image prediction.
4. Airflow data + model pipeline (task 2) is the following (look dags/pipeline.py and dags/utils):

    4.1 First we are sorting the new-coming data in 'animals_all' by classes and then transferring into bucket
     'animals_to_predict'. This is also used for data validation, as we can manually check what data we have
     in that bucket and what are the new classes.
     
    4.2 Second Airflow task is model inference. We are using data from 'animals_to_predict' with known true labels and
    make prediction with existing model, saving that predictions to 'animals_predicted'. Then we can manually check
    the difference and compute an error.
    
    4.3 Next step in model retraining. We are using true labeled data in 'animals_to_predict', fit the data for one cycle
    and then replace existing model (it lies in dag/utils/model and is not versioned by DVC, as it is not inside any git repo
    by the fact) with the new one. NOTE: was experiencing some troubles with cluster resources at this step - had to
    increase its computational power which is the reason why there's no screenshots of Airflow here - there's no money
    left in GCP proj.
    
    4.4 Last step is deployment of new-trained model using KubernetesPodOperator and GKE (task 3.1).
     https://cloud.google.com/composer/docs/how-to/using/using-kubernetes-pod-operator - here's documentation how to do that
     with Composer.The repo image should be built with CloudBuild using cloudbuild.yaml first and then GCP will help you to assign it to the
     right pod on Airflow-worker.
     Idea was to make the last Airflow task
    run the same container as if it would be a local run in GKE and start the website with model deployment which have to
    be up until nex DAG's run. And this task was failed, because despite the fact that container itself attempted to run
    and I was able to see it on GKE cluster, it did not resolve the host and the rest api code failed, thus the website with 
    the deployment was never up.
    
5. The reproducibility (task 3.2) of the code is guaranteed by the containerizing approach and by proper setups of Composer in GCP.
All the code technically runs in containers, and all is needed is to install composer_requirements.txt for Airflow and 
requirements.txt for docker. Monitoring and tracking (task 3.3) is possible with Airflow logs and GKE pod logs (and Python
prints which are present there of course). CloudBuild is also included in validation step, as it allows to catch some errors
on the building step after the trigger (after push to repo).
 I did not integrated TensorBoard, unfortunately.

6. Please note that most of these tasks I was doing together with Volodymyr Prypeshnyuk in live on-call mode 
(I've already informed you about that on last study session, just fyi) 
I remember your concerns regarding that splitting job here is not right approach and I must ensure you that it didnt take place here.


    