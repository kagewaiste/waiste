import os
import io
import datetime
import sys
import time
import subprocess
import RPi.GPIO as GPIO
import threading
import base64
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
from adafruit_servokit import ServoKit
from gpiozero import DistanceSensor 


# === Object Detection Start ===

# PIR
GPIO_PIR = 14
# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_PIR, GPIO.IN)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'

motion_detect = False

def image_detection():
    global motion_detect
    filename = "img/capture.jpg"
    while True:
        signal = GPIO.input(GPIO_PIR)
        if motion_detect != signal:
            motion_detect = signal
            if signal == True:
                print("Motion detected, processing object detection")
                capture_webcam()
                predict_image_classification_sample(
                    project="481928581448",
                    endpoint_id="3923833743113977856",
                    location="us-central1",
                    filename=filename
                )
                #os.remove(filename)

def capture_webcam():
    os.system('./webcam.sh')

def predict_image_classification_sample(
    project: str,
    endpoint_id: str,
    filename: str,
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    with open(filename, "rb") as f:
        file_content = f.read()

    # The format of each instance should conform to the deployed model's prediction input schema.
    encoded_content = base64.b64encode(file_content).decode("utf-8")
    instance = predict.instance.ImageClassificationPredictionInstance(
        content=encoded_content,
    ).to_value()
    instances = [instance]
    # See gs://google-cloud-aiplatform/schema/predict/params/image_classification_1.0.0.yaml for the format of the parameters.
    parameters = predict.params.ImageClassificationPredictionParams(
        confidence_threshold=0.5,
        max_predictions=5,
    ).to_value()
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    # See gs://google-cloud-aiplatform/schema/predict/prediction/image_classification_1.0.0.yaml for the format of the predictions.
    predictions = response.predictions
    res = []
    for prediction in predictions:
        pred_dict = dict(prediction)
        print(pred_dict)
        #res.append({"name": pred_dict["displayNames"][0], "conf": pred_dict["confidences"][0]})
        #print("Name: {}, Confidence: {}".format(pred_dict["displayNames"][0], pred_dict["confidences"][0]))
        #for item in prediction:
         #   print(f"Item: {item}")

    return res

if __name__ == '__main__':
    try:
        image_thread = threading.Thread(target=image_detection)
        image_thread.start()
        while True:
            # Do other tasks
            pass

    # try:
    #     while True:
    #         print(GPIO.input(GPIO_PIR))
    #         time.sleep(1)

    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Application stopped by User")
        GPIO.cleanup() 

# === Object Detection End ===


# === Servo Start ===

min_duty = 500
max_duty = 2500

kit = ServoKit(channels=16)
kit.frequency = 60

kit.servo[0].set_pulse_width_range(min_duty, max_duty)
kit.servo[1].set_pulse_width_range(min_duty, max_duty)
kit.servo[2].set_pulse_width_range(min_duty, max_duty)
kit.servo[3].set_pulse_width_range(min_duty, max_duty)
kit.servo[4].set_pulse_width_range(min_duty, max_duty)
kit.servo[5].set_pulse_width_range(min_duty, max_duty)

while True:
    jenis_sampah = input("Jenis Sampah : ")

    if jenis_sampah == "plastik":
        kit.servo[0].angle = 50     #plat1
        kit.servo[1].angle = 130
        time.sleep(3)
        kit.servo[0].angle = 90
        kit.servo[1].angle = 90
        time.sleep(3)

        kit.servo[2].angle = 50     #plat2
        kit.servo[3].angle = 130
        time.sleep(3)
        kit.servo[2].angle = 90
        kit.servo[3].angle = 90
        time.sleep(3)

        kit.servo[4].angle = 50     #plat3
        kit.servo[5].angle = 130
        time.sleep(3)
        kit.servo[4].angle = 90
        kit.servo[5].angle = 90
        time.sleep(3)
        break

    elif jenis_sampah == "kertas":
        kit.servo[0].angle = 50
        kit.servo[1].angle = 130
        time.sleep(3)
        kit.servo[0].angle = 90
        kit.servo[1].angle = 90
        time.sleep(3)

        kit.servo[2].angle = 50
        kit.servo[3].angle = 130
        time.sleep(3)
        kit.servo[2].angle = 90
        kit.servo[3].angle = 90
        time.sleep(3)

        kit.servo[4].angle = 130
        kit.servo[5].angle = 50
        time.sleep(3)
        kit.servo[4].angle = 90
        kit.servo[5].angle = 90
        time.sleep(3)
        break

    elif jenis_sampah == "besi":
        kit.servo[0].angle = 50
        kit.servo[1].angle = 130
        time.sleep(3)
        kit.servo[0].angle = 90
        kit.servo[1].angle = 90
        time.sleep(3)

        kit.servo[2].angle = 130
        kit.servo[3].angle = 50
        time.sleep(3)
        kit.servo[2].angle = 90
        kit.servo[3].angle = 90
        time.sleep(3)

        kit.servo[4].angle = 130
        kit.servo[5].angle = 50
        time.sleep(3)
        kit.servo[4].angle = 90
        kit.servo[5].angle = 90
        time.sleep(3)
        break

    elif jenis_sampah == "others":
        kit.servo[0].angle = 50
        kit.servo[1].angle = 130
        time.sleep(3)
        kit.servo[0].angle = 90
        kit.servo[1].angle = 90
        time.sleep(3)
        
        kit.servo[2].angle = 130
        kit.servo[3].angle = 50
        time.sleep(3)
        kit.servo[2].angle = 90
        kit.servo[3].angle = 90
        time.sleep(3)

        kit.servo[4].angle = 50
        kit.servo[5].angle = 130
        time.sleep(3)
        kit.servo[4].angle = 90
        kit.servo[5].angle = 90
        time.sleep(3)
        break

    else:
        kit.servo[0].angle = 50
        kit.servo[1].angle = 130
        time.sleep(3)
        kit.servo[0].angle = 90
        kit.servo[1].angle = 90
        time.sleep(3)
        
        kit.servo[2].angle = 130
        kit.servo[3].angle = 50
        time.sleep(3)
        kit.servo[2].angle = 90
        kit.servo[3].angle = 90
        time.sleep(3)

        kit.servo[4].angle = 50
        kit.servo[5].angle = 130
        time.sleep(3)
        kit.servo[4].angle = 90
        kit.servo[5].angle = 90
        time.sleep(3)
        break

# === Servo End ===


#  === Ultrasonic Start ===

ultrasonic_plastik = DistanceSensor(16, 12) 
ultrasonic_metal = DistanceSensor(21, 20) 
ultrasonic_kertas = DistanceSensor(1, 7) 
ultrasonic_other = DistanceSensor(8, 25) 

def persen(jarak) : 
    if(jarak >= 37) :
        persen = 0
    elif(jarak <= 8) :
        persen = 100
    else :
        persen = 115 - (jarak * 100 / 37)
    return persen

while True:
    jarak_plastik = round(ultrasonic_plastik.distance * 100)
    jarak_metal = round(ultrasonic_metal.distance * 100)
    jarak_kertas = round(ultrasonic_kertas.distance * 100)
    jarak_other = round(ultrasonic_other.distance * 100)

    persen_plastik = persen(jarak_plastik)
    persen_metal = persen(jarak_metal)
    persen_kertas = persen(jarak_kertas)
    persen_other = persen(jarak_other)
    
    print("sampah plastik", persen_plastik, "% terisi!")
    print("sampah metal", persen_metal, "% terisi!")
    print("sampah kertas", persen_kertas, "% terisi!")
    print("sampah lainnya", persen_other, "% terisi!")
    time.sleep(2.5)

# === Ultrasonic End ===

# === Loadcell Start ===

EMULATE_HX711=False

referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

hx1 = HX711(26, 19)
hx2 = HX711(13, 6)
hx3 = HX711(5, 0)
hx4 = HX711(11, 9)

hx1.reset()
hx1.tare_A()
hx1.tare_B()

hx2.reset()
hx2.tare_A()
hx2.tare_B()

hx3.reset()
hx3.tare_A()
hx3.tare_B()

hx4.reset()
hx4.tare_A()
hx4.tare_B()

while True:
    try:
        val1 = round(hx1.get_weight(5), 3)
        val2 = round(hx2.get_weight(5), 3)
        val3 = round(hx3.get_weight(5), 3)
        val4 = round(hx4.get_weight(5), 3)

        print("Berat Sampah Plastik:", val1)
        print("Berat Sampah Kertas:", val2)
        print("Berat Sampah Besi:", val3)
        print("Berat Sampah Lainnya:", val4)

        time.sleep(5)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()


# === Loadcell End ===