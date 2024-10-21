import pandas as pd

def get_plant_data(plant_name):
    df = pd.read_csv('plants_data.csv')
    plant_data = df[df['name'] == plant_name].to_dict('records')[0]
    return plant_data