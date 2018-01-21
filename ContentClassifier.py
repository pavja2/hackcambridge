from azure.cognitiveservices.vision.customvision.prediction import prediction_endpoint
from azure.cognitiveservices.vision.customvision.prediction.prediction_endpoint import models

training_key = "a0e93f4c04e1459282d6cbd265027b1a"
prediction_key = "e4aac43e14464c84bef9c0d2cc1ef298"

predictor = prediction_endpoint.PredictionEndpoint(prediction_key)


base_image_url = "https://raw.githubusercontent.com/Microsoft/Cognitive-CustomVision-Windows/master/Samples/"
test_img_url = base_image_url + "test.jpg"
results = predictor.predict_image_url(project.id, iteration.id, url=test_img_url)


# Display the results.
for prediction in results.predictions:
    print("\t" + prediction.tag + ": {0:.2f}%".format(prediction.probability * 100))
