import cv2
import os
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder

def load_images_from_folder(folder):
    images = []
    labels = []
    for plant_folder in os.listdir(folder):
        plant_path = os.path.join(folder, plant_folder)
        if os.path.isdir(plant_path):
            for filename in os.listdir(plant_path):
                img_path = os.path.join(plant_path, filename)
                img = cv2.imread(img_path)
                if img is not None:
                    img = cv2.resize(img, (100, 100))
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    images.append(img.flatten())
                    labels.append(plant_folder)
    return np.array(images), np.array(labels)

def train_model():
    images, labels = load_images_from_folder('plantdata/alovera')
    le = LabelEncoder()
    labels_encoded = le.fit_transform(labels)
    
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(images, labels_encoded)
    
    return knn, le

def recognize_plant(image_path):
    knn, le = train_model()
    
    img = cv2.imread(image_path)
    img = cv2.resize(img, (100, 100))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_flattened = img.flatten().reshape(1, -1)
    
    prediction = knn.predict(img_flattened)
    plant_name = le.inverse_transform(prediction)[0]
    
    return plant_name