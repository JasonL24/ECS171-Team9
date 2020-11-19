"""
file parameter cheat sheet
model = new_model or load_model
save_model_to = path
data = generate or load | and the dataset number to replace or load
epoch = small epoch
big_epoch = how many times the model fits
"""
import sys
from models.utils import *
from models.music_nn import *
from datetime import datetime

dataset_dir = '../data_mining/database/classical/'


def main(args):
    models = MusicNN()
    data = list()
    epoch = 30
    big_epoch = 10
    for arg in args[1:]:
        arg = arg.split('=')
        if arg[0] == 'model':
            if arg[1][0:4] == 'load':
                print('Loading Model')
                _, path = arg[1].split('@')
                models.load_weights(path)
        elif arg[0] == 'save_model_to':
            models.set_path(arg[1])
        elif arg[0] == 'data':
            ops, n = arg[1].split('@')
            if ops == 'generate':
                generate_data(dataset_dir, 'Piano right', n)
                data = load_train_data(n)
            elif ops == 'load':
                data = load_train_data(n)
        elif arg[0] == 'epoch':
            epoch = int(arg[1])
        elif arg[0] == 'big_epoch':
            big_epoch = int(arg[1])
        else:
            raise ValueError

    for i in range(big_epoch):
        train(models, data, i, epoch)

    return 0


def train(models, data, big_epoch, epoch):
    model = models.train_model
    x = data[0]
    y_s = data[1]
    y = data[2]

    model.fit(x=[x, y_s],
              y=y,
              epochs=epoch,
              batch_size=50)

    models.save_models()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    with open('./training.log', 'a') as f:
        string = 'Big Epoch: ' + str(big_epoch) + ', Model saved at ' + current_time + '\n\n'
        f.write(string)
        print(string)


if __name__ == '__main__':
    main(sys.argv)
