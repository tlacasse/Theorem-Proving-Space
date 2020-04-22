import numpy as np
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Input, Dense, Dropout, Activation, Lambda, Layer, Add, Multiply
from tensorflow.keras.utils import plot_model
from tensorflow.keras import backend as K
from var import PREMISE_TOKEN_DIMENSION

class _PATH:
    
    def __init__(self):
        self.prefix = '..\\data\\'
        self.training = 'training\\'
        self.models = 'models\\'

PATH = _PATH()

TRAINING = lambda: (PATH.prefix + PATH.training)
MODELS = lambda: (PATH.prefix + PATH.models)

# http://louistiao.me/posts/implementing-variational-autoencoders-in-keras-beyond-the-quickstart-tutorial/

# only to affect loss
class KLDivergenceLayer(Layer):
    
    def __init__(self, beta, *args, **kwargs):
        self.beta = beta
        self.is_placeholder = True
        super(KLDivergenceLayer, self).__init__(*args, **kwargs)

    def call(self, inputs):
        mean, log_std = inputs
        kl_batch = - .5 * K.sum(1 + log_std - K.square(mean) - K.exp(log_std), axis=-1)
        self.add_loss(self.beta * K.mean(kl_batch), inputs=inputs)
        return inputs
    
def nll(y_true, y_pred):
    return K.sum(K.binary_crossentropy(y_true, y_pred), axis=-1)

class PC_Space_A:
    
    def __init__(self, latent_dim, beta, encoder_layer_dim, 
                 decoder_layer_dim_1, decoder_layer_dim_2):
        self.LATENT_DIM = latent_dim
        self.BETA = beta
        self.ENCODER_LAYER_DIM = encoder_layer_dim
        self.DECODER_LAYER_DIM_1 = decoder_layer_dim_1
        self.DECODER_LAYER_DIM_2 = decoder_layer_dim_2
        self.INPUT_DIM = PREMISE_TOKEN_DIMENSION
        self.OUTPUT_DIM = np.load(TRAINING() + 'PC_train_conjecture_token_bag.npy').shape[1]
        
        # recursive encoder
        token = Input(shape=(PREMISE_TOKEN_DIMENSION,), name='input_token')
        left = Input(shape=(PREMISE_TOKEN_DIMENSION,), name='input_left')
        right = Input(shape=(PREMISE_TOKEN_DIMENSION,), name='input_right')
        
        token_h = Dense(PREMISE_TOKEN_DIMENSION, activation='relu')(token)
        left_h = Dense(PREMISE_TOKEN_DIMENSION, activation='relu')(left)
        right_h = Dense(PREMISE_TOKEN_DIMENSION, activation='relu')(right)
        
        tree = Add()([token_h, left_h, right_h])
        tree = Activation('relu', name='tree_encoding')(tree)

        # build latent distribution
        h = Dense(self.ENCODER_LAYER_DIM, activation='relu')(tree)
        
        z_mean = Dense(self.LATENT_DIM)(h)
        z_log_std = Dense(self.LATENT_DIM)(h)
        z_mean, z_log_std = KLDivergenceLayer(beta=self.BETA)([z_mean, z_log_std])
        z_std = Lambda(lambda t: K.exp(.5*t))(z_log_std)
        
        # build dist encoder
        self.distencoder = Model(inputs=[token, left, right], outputs=z_mean, name='distencoder')
        
        # build distribution reparameterization (move noise out of gradient)
        noise = Input(tensor=K.random_normal(stddev=1.0, shape=(K.shape(token)[0], self.LATENT_DIM)))
        z_noise = Multiply()([z_std, noise])
        z = Add(name='latent_space')([z_mean, z_noise])
        
        # build decoder
        decoder = Sequential()
        decoder.add(Dense(self.DECODER_LAYER_DIM_1, input_dim=self.LATENT_DIM, activation='relu'))
        decoder.add(Dense(self.DECODER_LAYER_DIM_2, activation='relu'))
        decoder.add(Dense(self.OUTPUT_DIM, activation='softmax', name='classifier'))
        self.decoder = decoder
        
        # combine model
        self.model = Model(inputs=[token, left, right, noise], outputs=decoder(z), name='pc_space_a')
        self.model.compile(optimizer='rmsprop', loss=nll)
        
        # build encoder
        self.encoder = self.model.get_layer('tree_encoding').output
        
    def summary(self):
        self.model.summary()
        
    def plot_model(self):
        plot_model(self.model, to_file=(MODELS() + 'PC-Space-A.png'),
                   show_shapes=True, show_layer_names=True)
        plot_model(self.decoder, to_file=(MODELS() + 'PC-Space-A_decoder.png'),
                   show_shapes=True, show_layer_names=True)

