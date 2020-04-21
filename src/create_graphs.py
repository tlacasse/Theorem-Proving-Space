from models import PC_Space_A
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

model = PC_Space_A(latent_dim=256, beta=1.0, encoder_layer_dim=256, 
                   decoder_layer_dim_1=480, decoder_layer_dim_2=512)

model.summary()
model.plot_model()
