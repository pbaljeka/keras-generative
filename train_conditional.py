import os
import sys
import math
import argparse

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
import matplotlib
matplotlib.use('Agg')

from models import CVAE, CVAEGAN
from basics import *

models = {
    'cvae': CVAE,
    'cvaegan': CVAEGAN
}

def main():
    # Parsing arguments
    parser = argparse.ArgumentParser(description='Training GANs or VAEs')
    parser.add_argument('--model', type=str, required=True)
    parser.add_argument('--epoch', type=int, default=200)
    parser.add_argument('--batchsize', type=int, default=50)
    parser.add_argument('--output', default='output')
    parser.add_argument('--zdims', type=int, default=256)

    args = parser.parse_args()

    # Make output direcotiry if not exists
    if not os.path.isdir(args.output):
        os.mkdir(args.output)

    # Construct model
    if args.model not in models:
        raise Exception('Unknown model:', args.model)

    model = models[args.model](z_dims=args.zdims, output=args.output)

    datasets = load_celebA('datasets/celebA.hdf5')

    # Training loop
    samples = np.random.normal(size=(10, args.zdims)).astype(np.float32)
    model.main_loop(datasets, samples, datasets.names,
        epochs=args.epoch,
        batchsize=args.batchsize,
        reporter=['loss', 'g_loss', 'd_loss', 'c_loss', 'ae_loss'])

if __name__ == '__main__':
    main()
