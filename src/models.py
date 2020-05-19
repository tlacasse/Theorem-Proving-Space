import numpy as np
import os
import glob
import datetime
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Input, Dense, Activation, Lambda, Layer, Add, Multiply
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.utils import plot_model
from tensorflow.keras import backend as K

from var import PREMISE_TOKEN_DIMENSION
from data import dump_data, load_data

class _PATH:
    
    def __init__(self):
        self.prefix = '../data/'
        self.training = 'training/'
        self.models = 'models/'

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
        mean, log_var = inputs
        kl_batch = - .5 * K.sum(1 + log_var - K.square(mean) - K.exp(log_var), axis=-1)
        self.add_loss(self.beta * K.mean(kl_batch), inputs=inputs)
        return inputs
    
def nll(y_true, y_pred):
    return K.sum(K.binary_crossentropy(y_true, y_pred), axis=-1)

class BaseModel:
    
    def __init__(self, name, filepath):
        self.name = name
        self.filepath = filepath
        self.model = None
        self.decoder = None
        self.encoder = None
        self.params = load_data(MODELS() + filepath + '.params')
        
    def loadweights(self):
        wpath = MODELS() + self.filepath + '.h5'
        if os.path.isfile(wpath):
            self.model.load_weights(wpath)
        
    def summary(self):
        self.model.summary()
 
    def save(self, desc, history):
        BaseModel.savemodel(self.model, self.name, self.params, 
                            desc, history, withnowstring=True)
        
    def plot_model(self):
        filename = BaseModel.getfilename(self.name, self.params)
        plot_model(self.model, to_file=(MODELS() + '{}.png'.format(filename)),
                   show_shapes=True, show_layer_names=True)
        plot_model(self.decoder, to_file=(MODELS() + '{}_decoder.png'.format(filename)),
                   show_shapes=True, show_layer_names=True)
        
    @staticmethod
    def savemodel(model, name, params, desc='', history=None, withnowstring=False):
        file = '{}_{}'.format(
                BaseModel.getfilename(name, params), 
                desc)
        if withnowstring:
            file += '_{}'.format(BaseModel.nowstring())
        if history is not None:
            model.save_weights(MODELS() + file + '.h5')
            dump_data(MODELS() + file + '.history', history.history)
            dump_data(MODELS() + file + '.params', params)
        return file
        
    @staticmethod
    def getfilename(name, params):
        return '{}_{}'.format(name, BaseModel.getparamstring(params))
        
    @staticmethod
    def getparamstring(params):
        return '-'.join(['{}{}'.format(k, v) for k, v in params.items()])
        
    @staticmethod
    def nowstring():
        return datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') 
    
    @staticmethod
    def build_z_dist(inlayer, layer, latent_dim, beta=1.0):
        z_mean = Dense(latent_dim)(layer)
        z_log_var = Dense(latent_dim)(layer)
        z_mean, z_log_var = KLDivergenceLayer(beta=beta)([z_mean, z_log_var])
        z_std = Lambda(lambda t: K.exp(.5*t))(z_log_var)
        
        innoise = Input(tensor=K.random_normal(stddev=1.0, shape=(K.shape(inlayer)[0], latent_dim)), 
                        name='inputnoise')
        z_noise = Multiply()([z_std, innoise])
        z = Add(name='latent_space')([z_mean, z_noise])
        
        return z_mean, z_std, z, innoise
    
class BaseTrainer:
    
    def __init__(self):
        pass
    
    @staticmethod
    def shuffle(arrays):
        state = np.random.get_state()
        for a in arrays:
            np.random.set_state(state)
            np.random.shuffle(a)

class ConjectureTokenVAE(BaseModel):
    
    @staticmethod
    def _name():
        return 'CTVAE'
    
    def __init__(self, filepath):
        super().__init__(ConjectureTokenVAE._name(), filepath)
        
        self.model, self.decoder = ConjectureTokenVAE.build_model(self.params)
        self.loadweights()
        self.model.compile(optimizer=RMSprop(lr=self.params['lr']), loss='binary_crossentropy', metrics=['mse'])
        
        self.encoder = Model(inputs=[self.model.get_layer('encoder').input,
                                     self.model.get_layer('inputnoise').input], 
                             outputs=self.model.get_layer('latent_space').output)
    
    @classmethod
    def build(cls, params):
        model, _ = ConjectureTokenVAE.build_model(params)
        path = BaseModel.savemodel(model, ConjectureTokenVAE._name(), params)
        dump_data(MODELS() + path + '.params', params)
        return cls(path)
    
    @staticmethod
    def build_params(latent_dim, beta, hidden_dims, batch_size, learning_rate):
        params = dict()
        params['z'] = latent_dim
        params['b'] = beta
        for i, d in enumerate(hidden_dims):
            params[str(i) + 'hd'] = d
        params['bs'] = batch_size
        params['lr'] = learning_rate
        return params
    
    @staticmethod
    def build_model(params):
        data_dim = np.load(TRAINING() + 'PC_train_conjecture_token_bag.npy').shape[1]
        hidden_dims = [k for k, v in params.items() if k.endswith('hd')]
        hidden_dims.sort()
        hidden_dims = [params[k] for k in hidden_dims]
        
        # build encoder
        inlayer = Input(shape=(data_dim,), name='encoder')
        layer = inlayer
        for dim in hidden_dims:
            layer = Dense(dim, activation='relu')(layer)
        
        # build latent distribution
        z_mean, z_std, z, innoise = BaseModel.build_z_dist(inlayer, layer, params['z'], params['b'])
        
        # build decoder
        hidden_dims = hidden_dims[::-1]
        decoder = Sequential()
        decoder.add(Dense(hidden_dims[0], input_dim=params['z'], activation='relu', name='decoder'))
        for dim in hidden_dims[1:]:
            decoder.add(Dense(dim, activation='relu'))
        decoder.add(Dense(data_dim, name='classifier'))
        
        return Model(inputs=[inlayer, innoise], outputs=decoder(z), name='model'), decoder
    
class CTVAE_Trainer:
    
    def __init__(self):
        self.conjecture_tokens = np.load(TRAINING() + 'PC_train_conjecture_token_bag.npy')
        self.n = self.conjecture_tokens.shape[0]
        self.m = self.conjecture_tokens.shape[1]
        print('CONJECTURES: {}'.format(self.n))
        print('CONJECTURE TOKENS: {}'.format(self.m))
        
    def fit(self, ctvaemodel, epochs):
        batch_size = ctvaemodel.params['bs']
        history = ctvaemodel.model.fit_generator(self.get_batches(batch_size),
                steps_per_epoch=int(self.n/batch_size), epochs=epochs, verbose=2)
        ctvaemodel.save('', history)
        
    def get_batches(self, batch_size):
        arr = self.conjecture_tokens
        while True:
            BaseTrainer.shuffle((arr,))
            num = int(np.ceil(arr.shape[0] / batch_size))
            for n in range(num):
                a = n * batch_size
                b = (n + 1) * batch_size
                batch = arr[a:b,:]
                yield (batch, batch)

class PC_Space_A(BaseModel):
    
    def __init__(self, latent_dim, beta, 
                 encoder_layer_dim, decoder_layer_dims):
        self.LATENT_DIM = latent_dim
        self.BETA = beta
        self.ENCODER_LAYER_DIM = encoder_layer_dim
        self.DECODER_LAYER_DIMS = decoder_layer_dims
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
        decoder.add(Dense(self.DECODER_LAYER_DIMS[0], input_dim=self.LATENT_DIM, activation='relu'))
        for dim in self.DECODER_LAYER_DIMS[1:]:
            decoder.add(Dense(dim, activation='relu'))
        decoder.add(Dense(self.OUTPUT_DIM, activation='softmax', name='classifier'))
        self.decoder = decoder
        
        # combine model
        self.model = Model(inputs=[token, left, right, noise], outputs=decoder(z), name='pc_space_a')
        self.model.compile(optimizer='rmsprop', loss=nll)
        
        # build encoder
        self.encoder = self.model.get_layer('tree_encoding').output

class PC_Space_A_Trainer:
    
    def __init__(self):
        self.conjecture_tokens = np.load(TRAINING() + 'PC_train_conjecture_token_bag.npy')
        self.tokens = np.load(TRAINING() + 'PC_initial_token_encoding.npy')
        self.subtrees = np.load(MODELS() + 'PC_subtree_encoding.npy')
        print('CONJECTURES: {}'.format(self.conjecture_tokens.shape[0]))
        print('CONJECTURE TOKENS: {}'.format(self.conjecture_tokens.shape[1]))
        print('PREMISE TOKENS: {}'.format(self.tokens.shape[0]))
        print('PREMISE SUBTREES: {}'.format(self.subtrees.shape[0]))
        self.layer_groups = ['002', '003', '004', '005', '006', '007', '008', '009', '010',
                    '11-15', '16-30', 'g t30', 'whole']
        
    def fit(self, pc_space_a, epochs, batch_size, repeats):
        history = pc_space_a.model.fit_generator(
                self.get_training_data('002', batch_size, repeats),
                steps_per_epoch=int(1000000/batch_size), epochs=epochs, verbose=2)
        pc_space_a.save('002', history)
        
    def get_training_data(self, layer_group, batch_size, repeats):
        for p, c in self.get_layer_files(layer_group):
            token, left, right = self.build_X(np.load(p))
            conjecture = self.build_Y(np.load(c))
            for _ in range(repeats):
                self.shuffle((token, left, right, conjecture))
                num = int(np.ceil(conjecture.shape[0] / batch_size))
                for n in range(num):
                    a = n * batch_size
                    b = (n + 1) * batch_size
                    yield ((token[a:b,:], left[a:b,:], right[a:b,:]), conjecture[a:b,:])

    def build_X(self, premise_map):
        n = premise_map.shape[0]
        m = PREMISE_TOKEN_DIMENSION
        
        token = np.empty((n, m), dtype='double')
        left = np.empty((n, m), dtype='double')
        right = np.empty((n, m), dtype='double')
        for i, x in enumerate(premise_map):
            token[i, :] = self.tokens[x[1], :]
            left[i, :] = self.subtrees[x[2], :]
            right[i, :] = self.subtrees[x[3], :]
        return token, left, right
        
    def build_Y(self, conjecture_ids):
        n = conjecture_ids.shape[0]
        m = self.conjecture_tokens.shape[1]
        result = np.empty((n, m), dtype='double')
        for i, cid in enumerate(conjecture_ids):
            result[i, :] = self.conjecture_tokens[cid]
        return result
    
    def get_layer_files(self, layer_group):
        ps = glob.glob(TRAINING() + 'points/PC_{}_premise_map_*'.format(layer_group))
        cs = glob.glob(TRAINING() + 'points/PC-A_{}_conjecture_ids_*'.format(layer_group))
        for p, c in zip(ps, cs):
            print(p)
            yield p, c
            
    def shuffle(self, arrays):
        state = np.random.get_state()
        for a in arrays:
            np.random.set_state(state)
            np.random.shuffle(a)
