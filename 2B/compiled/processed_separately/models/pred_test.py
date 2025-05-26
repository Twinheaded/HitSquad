import math
import warnings
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from keras.models import load_model
from keras.losses import mean_squared_error as mse
from keras.utils import plot_model
import sklearn.metrics as metrics

from src.data.data import process_data

warnings.filterwarnings("ignore")


def calculate_mape(y_true, y_pred):
    y_true_filtered = [x for x in y_true if x > 0]
    y_pred_filtered = [y_pred[i] for i in range(len(y_true)) if y_true[i] > 0]
    num = len(y_pred_filtered)
    total_error = sum(abs(y_true_filtered[i] - y_pred_filtered[i]) / y_true_filtered[i] for i in range(num))
    return total_error * (100 / num)


def evaluate_regression(y_true, y_pred):
    mape = calculate_mape(y_true, y_pred)
    evs = metrics.explained_variance_score(y_true, y_pred)
    mae = metrics.mean_absolute_error(y_true, y_pred)
    mse_val = metrics.mean_squared_error(y_true, y_pred)
    r2 = metrics.r2_score(y_true, y_pred)

    print(f'Explained Variance Score: {evs:.6f}')
    print(f'MAPE: {mape:.6f}%')
    print(f'MAE: {mae:.6f}')
    print(f'MSE: {mse_val:.6f}')
    print(f'RMSE: {math.sqrt(mse_val):.6f}')
    print(f'R2 Score: {r2:.6f}')


def plot_predictions(y_true, y_preds, model_names):
    x = pd.date_range('2006-10-01 00:00', periods=96, freq='15min')
    fig, ax = plt.subplots()
    ax.plot(x, y_true, label='True Data')
    for name, y_pred in zip(model_names, y_preds):
        ax.plot(x, y_pred, label=name)
    ax.set_xlabel('Time of Day')
    ax.set_ylabel('Flow')
    ax.grid(True)
    ax.legend()
    date_format = mpl.dates.DateFormatter("%H:%M")
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()
    plt.show()


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scats",
        type=int,
        default=970,
        help="SCATS site ID to load model and data for.")
    args = parser.parse_args()

    model_dir = f'model/{args.scats}'
    model_paths = {
        'LSTM': f'{model_dir}/lstm.h5',
        'GRU': f'{model_dir}/gru.h5',
        'SIMPLE_RNN': f'{model_dir}/rnn.h5',
    }

    models = {name: load_model(path, custom_objects={'mse': mse}) for name, path in model_paths.items()}
    model_names = list(models.keys())

    lag = 4
    file_train = f'src/data/SCATS_Data/{args.scats}/{args.scats}.csv'
    file_test = f'src/data/SCATS_Data/{args.scats}/{args.scats}_test.csv'

    _, _, X_test, y_test, scaler = process_data(file_train, file_test, lag)
    y_test = scaler.inverse_transform(y_test.reshape(-1, 1)).reshape(1, -1)[0]

    y_preds = []

    for name, model in models.items():
        X_input = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        plot_model(model, show_shapes=True)

        y_pred = model.predict(X_input)
        y_pred = scaler.inverse_transform(y_pred.reshape(-1, 1)).reshape(1, -1)[0]

        y_preds.append(y_pred[:96])
        print(f"\n{name} Model Evaluation:")
        evaluate_regression(y_test, y_pred)

    plot_predictions(y_test[:96], y_preds, model_names)


if __name__ == '__main__':
    main(sys.argv)
