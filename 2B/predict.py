import math
import warnings
import numpy as np
import pandas as pd
import os
from src.data.data import process_data
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import plot_model
import sklearn.metrics as metrics
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys
import argparse
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from keras.api.losses import MeanSquaredError

warnings.filterwarnings("ignore")

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="lstm", help="Model to use for prediction.")
    #parser.add_argument("--scats", type=int, default=970, help="Specific SCATS site number.") Commented out because predictions are batch wise
    args = parser.parse_args()

    scatslist = [
        970, 2000, 2200, 2820, 2825, 2827, 2846, 3001, 3002, 3120, 3122, 3126, 3127, 3180,
        3662, 3682, 3685, 3804, 3812, 4030, 4032, 4034, 4035, 4040, 4043, 4051, 4057, 4063,
        4262, 4263, 4264, 4266, 4270, 4272, 4273, 4321, 4324, 4335, 4812, 4821
    ]

    for scat in scatslist:
        lag = 4
        attr = 'Values'

        # Generate necessary file paths
        file1 = f'src/data/SCATS_Data/{scat}/{scat}.csv'
        file2 = f'src/data/SCATS_Data/{scat}/{scat}_test.csv'
        model_path = f'model/{scat}/{args.model}.h5'
        predictions_dir = f'predictions/{scat}'
        prediction_file = f'{predictions_dir}/{args.model}_{scat}.csv'
        os.makedirs(predictions_dir, exist_ok=True)
        # Load and preprocess
        x_train, x_test, y_train, y_test, scaler = process_data(file1, file2, lag)
        df = pd.read_csv(file1)[-lag:]
        dft = pd.read_csv(file2)
        flow_x = scaler.transform(df[attr].values.reshape(-1, 1)).reshape(1, -1)[0]
        flow_y = scaler.transform(dft[attr].values.reshape(-1, 1)).reshape(1, -1)[0]
        mdl = load_model(model_path, custom_objects={'mse': MeanSquaredError()})
        i = 0
        y_pred = []

        while (i < 2880):
            flow_x = np.array(flow_x).reshape((1, lag, 1))
            val = mdl.predict(flow_x, verbose=0)
            flow_x = flow_x.reshape(lag,)
            new_value = val[0][0]
            flow_x = np.append(flow_x[1:], flow_y[i])
            val = scaler.inverse_transform(val.reshape(-1, 1)).reshape(1, -1)[0]

            # ======= Terminal prints (Testing Only)=======
            print(f"[{scat}] Step {i} Prediction: {val[0]}")
            print(f"[{scat}] Appending actual value from test set: {flow_y[i]}")
            print("-" * 50)
            # ==============================================

            y_pred.append(val)
            i += 1

        y_test = scaler.inverse_transform(y_test.reshape(-1, 1)).reshape(1, -1)[0]
        df_pred = pd.DataFrame(y_pred, columns=["Values"])
        df_pred.to_csv(prediction_file, index=False)


if __name__ == '__main__':
    main(sys.argv)
