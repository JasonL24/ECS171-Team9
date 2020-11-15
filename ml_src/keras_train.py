import sys
from models.utils import *
from models.music_nn import *
from datetime import datetime

BIG_EPOCH = 10
dataset_dir = '../data_mining/database/classical/'


# TODO: features to do
# Music Theory
# Reinforcement Learning


def main(args):
    models = MusicNN()
    data = list()
    for arg in args[1:]:
        arg = arg.split('=')
        if arg[0] == 'model':
            if arg[1] == 'load':
                pass
        elif arg[0] == 'save_model_to':
            if not os.path.exists(arg[1]):
                os.makedirs(arg[1] + '/inf_enc')
                os.makedirs(arg[1] + '/inf_dec')
                os.makedirs(arg[1] + '/train_model')
            models.set_path(arg[1])
        elif arg[0] == 'data':
            ops, n = arg[1].split('|')
            if ops == 'generate':
                generate_data(dataset_dir, 'Piano right', n)
                data = load_train_data(n)
            elif ops == 'load':
                data = load_train_data(n)
        else:
            raise ValueError

    for i in range(BIG_EPOCH):
        train(models, data, i)

    return 0


def train(models, data, big_epoch):
    model = models.train_model
    x = data[0]
    y_s = data[1]
    y = data[2]

    model.fit(x=[x, y_s],
              y=y,
              epochs=100,
              batch_size=30)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    models.save_models()
    with open('./training.log', 'a') as f:
        f.write('Big Epoch: ' + str(big_epoch) +
                '\nModel saved at ' + current_time + '\n\n')


if __name__ == '__main__':
    main(sys.argv)
