"""
file parameter cheat sheet
model = new_model or load_model
save_model_to = path
data = generate or load | and the dataset number to replace or load
epoch = small epoch
"""
import sys
from models.utils import *
from models.music_nn import *
from datetime import datetime

dataset_dir = '../data_mining/database/classical/'


def main(args):
    models = MusicNN()
    train_data, test_data = None, None
    epoch = 30
    # big_epoch = 10
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
                train_data, test_data = load_train_data(n)
            elif ops == 'load':
                train_data, test_data = load_train_data(n)
        elif arg[0] == 'epoch':
            epoch = int(arg[1])
        # elif arg[0] == 'big_epoch':
        #     big_epoch = int(arg[1])
        else:
            raise ValueError

    i = 0
    while True:
        try:
            train(models, train_data, test_data, i, epoch)
            i += 1
        except KeyboardInterrupt:
            print('Terminating training')
            break
    return 0


def train(models, train_data, test_data, big_epoch, epoch):
    if not train_data or not test_data:
        print('No train or test data')
        raise ValueError
    model = models.train_model
    x = train_data[0]
    y_s = train_data[1]
    y = train_data[2]

    model.fit(x=[x, y_s],
              y=y,
              epochs=epoch,
              batch_size=50)

    # Evaluate Test Set
    x = test_data[0]
    y_s = test_data[1]
    y = test_data[2]
    score = models.train_model.evaluate(x=[x, y_s], y=y)[1]

    models.save_models()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    with open(models.path + '/train.log', 'a') as f:
        string = 'Big Epoch: ' + str(big_epoch)
        string += ' Model Score: %0.3f' % score
        string += ', Model saved at ' + current_time + '\n\n'
        f.write(string)
        print(string)


if __name__ == '__main__':
    main(sys.argv)
