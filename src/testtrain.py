from train import main

class Args:
    
    def __init__(self):
        self.modeltype = 'ctvae'
        self.e = 10
        self.bs = 64
        self.lr = 0.001
        self.z = 2
        self.b = 4.0
        self.hd = '1024,512,256'
        self.local = False

main(Args())
