import os
import pandas as pd
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from plant_recognition import recognize_plant  # Import your plant recognition logic

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
PLANTDATA_FOLDER = 'plantdata/'
CSV_FILE = 'plants_data.csv'

# Allow only image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Pass image to recognition model
        plant_name = recognize_plant(file_path)  # This should return plant name

        if plant_name:
            # Retrieve plant information from CSV
            plant_info = get_plant_info(plant_name)
            if plant_info:
                return jsonify({'plant': plant_name, 'info': plant_info})
            else:
                return jsonify({'error': 'Plant information not found'})
        else:
            return jsonify({'error': 'Plant not recognized'})
    else:
        return jsonify({'error': 'Invalid file type'})

def get_plant_info(plant_name):
    # Load the CSV file
    df = pd.read_csv(CSV_FILE)
    
    # Find the plant information
    plant_data = df[df['PlantName'].str.lower() == plant_name.lower()]
    
    if not plant_data.empty:
        return plant_data.to_dict('records')[0]  # Convert to dictionary
    return None

if __name__ == '__main__':
    app.run(debug=True)
