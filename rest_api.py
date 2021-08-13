from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from inference import predict
import uvicorn
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")
UPLOAD_FOLDER = 'images/test/'


@app.get("/", response_class=HTMLResponse)
def home_page():
    return templates.TemplateResponse("index.html")

@app.post("/")
async def predict_form(request: Request, file: UploadFile = File(...)):
    file_name = "image_to_predict.jpg"
    file_location = os.path.join(
        UPLOAD_FOLDER,
        file_name
    )
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    prediction, proba = predict()
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "image_loc": file_location,
                                                     "prediction": prediction,
                                                     "proba": proba})


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000)