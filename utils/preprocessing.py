import pandas as pd

def load_data(path):
    data = pd.read_csv(path)

    data['Delay'] = (data['Days for shipping (real)'] > data['Days for shipment (scheduled)']).astype(int)

    return data

def get_features(data):
    features = [
        'Days for shipping (real)',
        'Days for shipment (scheduled)',
        'Order Item Quantity',
        'Sales'
    ]

    X = data[features]
    y = data['Delay']

    return X, y