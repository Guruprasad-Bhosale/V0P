import cv2
import os
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder

def load_images_from_folders(folders):
    images = []
    labels = []
    for folder in folders:
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
                        labels.append(plant_folder)  # Label is the folder name (plant name)
    return np.array(images), np.array(labels)

def train_model():
    # List of all plant folders
    PLANTDATA_FOLDERS = [
        'plantdata/alovera/',
        'plantdata/banana/',
        'plantdata/bilimbi/',
        'plantdata/cantaloupe/',
        'plantdata/cassava/',
        'plantdata/coconut/',
        'plantdata/corn/',
        'plantdata/cucumber/',
        'plantdata/curcuma/',
        'plantdata/eggplant/',
        'plantdata/galangal/',
        'plantdata/ginger/',
        'plantdata/guava/',
        'plantdata/kale/',
        'plantdata/longbeans/',
        'plantdata/mango/',
        'plantdata/melon/',
        'plantdata/orange/',
        'plantdata/paddy/',
        'plantdata/papaya/',
        'plantdata/pepper_chili/',
        'plantdata/pineapple/',
        'plantdata/pomelo/',
        'plantdata/shallot/',
        'plantdata/soyabean/',
        'plantdata/spinach/',
        'plantdata/sweet_potatoes/',
        'plantdata/waterapple/',
        'plantdata/watermelon/'
    ]
    
    # Load images and labels from all plant folders
    images, labels = load_images_from_folders(PLANTDATA_FOLDERS)
    
    # Encode labels (convert plant names to numeric format)
    le = LabelEncoder()
    labels_encoded = le.fit_transform(labels)
    
    # Train K-Nearest Neighbors classifier
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(images, labels_encoded)
    
    return knn, le

def recognize_plant(image_path):
    # Load the trained model and label encoder
    knn, le = train_model()
    
    # Load and preprocess the test image
    img = cv2.imread(image_path)
    img = cv2.resize(img, (100, 100))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_flattened = img.flatten().reshape(1, -1)
    
    # Predict the plant type
    prediction = knn.predict(img_flattened)
    plant_name = le.inverse_transform(prediction)[0]
    
    return plant_name
