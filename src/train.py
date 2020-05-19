import tensorflow as tf
try:
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
except Exception as e:
    print(e)

from argparse import ArgumentParser
from models import PATH, ConjectureTokenVAE, CTVAE_Trainer

def main(args):
    if args.local:
        PATH.prefix = '../data/local/'
    if args.modeltype.upper() == 'CTVAE':
        params = ConjectureTokenVAE.build_params(
                latent_dim=int(args.z),                        
                beta=int(args.b),
                hidden_dims=[int(d.strip()) for d in str(args.hd).split(',')], 
                batch_size=int(args.bs), 
                learning_rate=float(args.lr))
        model = ConjectureTokenVAE.build(params)
        
        trainer = CTVAE_Trainer()
        trainer.fit(model, epochs=int(args.e))

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('modeltype', help='[CTVAE]')
    parser.add_argument('--e', help='epochs [ALL]', default=10)
    parser.add_argument('--bs', help='batch size [ALL]', default=64)
    parser.add_argument('--lr', help='learning rate [ALL]', default=0.001)
    parser.add_argument('--z', help='latent dimension [ALL]', default=128)
    parser.add_argument('--b', help='KL beta [ALL]', default=1.0)
    parser.add_argument('--hd', help='comma separated hidden layer dims [CTVAE]', default='128')
    parser.add_argument('--local', action='store_true', help='use the "local" data, which is a smaller dataset')
    args = parser.parse_args()
    
    main(args)
