import sys
import warnings
import argparse
import numpy as np
import pandas as pd
from model import model
from model_lstm import LSTMModel
from model_gru import GRUModel
from keras.models import Model
from keras.callbacks import EarlyStopping
from data.data import process_data, full_scale_process_data
warnings.filterwarnings("ignore")

def train_model(model, X_train, y_train, name, config, scats, scale):
    
    #X_train: ndarray(number, lags, scats), Input data for train.
    #y_train: ndarray(number, ), result data for train.
    #name: String, name of model.
    #config: Dict, parameter for train.
    #scats: gives the specific scats data to be used
    

    model.compile(loss="mse", optimizer="rmsprop", metrics=['mape'])
    # early = EarlyStopping(monitor='val_loss', patience=30, verbose=0, mode='auto')
    hist = model.fit(
        X_train, y_train,
        batch_size=config["batch"],
        epochs=config["epochs"],
        validation_split=0.05)

    if scale == "scat_scale":
        model.save('model/'+ str(scats) + '/' + name + '.h5')
        df = pd.DataFrame.from_dict(hist.history)
        df.to_csv('model/' + str(scats) + '/' + name + ' loss.csv', encoding='utf-8', index=False)
    else:
        model.save('model/full_scale/' + name + '.h5')
        df = pd.DataFrame.from_dict(hist.history)
        df.to_csv('model/full_scale/' + name + ' loss.csv', encoding='utf-8', index=False)

def model_trainer(argmodel, scats, scale, encodercount):
    lag = 12
    config = {"batch": 256, "epochs": 600}
    if scale == "scat_scale":
        #file1 = 'data/SCATS_Data/'+str(scats)+'/'+str(scats)+'.csv'
        #file2 = 'data/SCATS_Data/'+str(scats)+'/'+str(scats)+'_test.csv'
        X_train, y_train, _, _, _ = process_data(file1, file2, lag) #Needs to be fixed before testing

        models = ['lstm','gru']
        if argmodel == 'lstm':
            X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
            lstm = LSTMModel([lag, 64, 64, 1])
            m = lstm.return_model()
            train_model(m, X_train, y_train, argmodel, config, scats, scale)
        if argmodel == 'gru':
            X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
            gru = GRUModel([lag, 64, 64, 1])
            m = gru.return_model()
            train_model(m, X_train, y_train, argmodel, config, scats, scale)

        if argmodel == 'all':
            for amodel in models:
                model_trainer(amodel,scats)

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        default="lstm",
        help="Model to train.")
    parser.add_argument(
        "--scats",
        type=int,
        default=970,
        help="Specific Scat Value.")
    parser.add_argument(
        "--scale",
        default='scat_scale',
        help="Specify if you want a specific SCAT value, or the whole damn dataset. (scat_scale , full_scale)")
    args = parser.parse_args()
    cnt = 0
    scatslist = [2000,2200,2820,2825,2827,2846,3001,3002,3120,3122,3126,3127,3180,3662,3682,3685,3804, 3812, 4030, 4032, 4034, 4035, 4040, 4043, 4051, 4057, 4063, 4262, 4263, 4264, 4266, 4270, 4272, 4273, 4321, 4324, 4335, 4812, 4821]
    if args.scats != 0:
        model_trainer(args.model, args.scats, args.scale)
    else:
        for scatsite in scatslist:
            cnt+=1
            model_trainer(args.model, scatsite, args.scale)