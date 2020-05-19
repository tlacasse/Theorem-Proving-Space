from models import PC_Space_A
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

model = PC_Space_A(latent_dim=128, beta=1.0, encoder_layer_dim=256, 
                   decoder_layer_dims=[320, 256])

model.summary()
model.plot_model()
