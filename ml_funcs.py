import logging
import os
import pickle


def train_model(model_instance,
                x_train,
                y_train,
                preffix: str,
                dir='./models'):

    model_name = f'{preffix}_model'
    model_path = os.path.join(dir, model_name)

    if os.path.isfile(model_path):
        with open(model_path, 'rb') as file:
            model = pickle.load(file)

        logging.info(f'MODEL LOADED FROM {model_path}')

    else:
        # Fit the classifier to the training data
        model = model_instance.fit(x_train, y_train)

        with open(model_path, 'wb') as file:
            pickle.dump(model, file)

        logging.info(f'MODEL TRAINED AND SAVED AT {model_path}')

    return model