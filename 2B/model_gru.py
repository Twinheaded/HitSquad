from keras.models import Sequential
from keras.layers import GRU, Dense, Dropout

class GRUModel:
    def __init__(self, units, num_features=1, dropout_rate=0.2, output_activation='sigmoid'):

        #Parameters:
        #- units: List of 4 integers [timesteps, gru1_units, gru2_units, output_units]
        #- num_features: Integer, number of features per time step (Technically always 1, The only real feature we have is Flow)
        #- dropout_rate: Float, dropout rate before the output layer
        #- output_activation: Activation function for the output layer (default: 'sigmoid')

        if not isinstance(units, (list, tuple)) or len(units) != 4:
            raise ValueError("`units` must be a list or tuple of 4 integers: [timesteps, gru1_units, gru2_units, output_units]")

        self.units = units
        self.num_features = num_features #Only 1 feature in code (Flow)
        self.dropout_rate = dropout_rate #Not necessary to usually set
        self.output_activation = output_activation #Not necessary to set either
        self.model = self.build_model()

        def build_model(self):
            model = Sequential([
                GRU(self.units[1], input_shape=(self.units[0], self.num_features), return_sequences=True),
                GRU(self.units[2]),
                Dropout(self.dropout_rate),
                Dense(self.units[3], activation=self.output_activation)
            ])

        def return_model():
            return self.model