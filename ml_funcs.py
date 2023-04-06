import logging
import os
import joblib


def train_model(model_instance,
                x_train,
                y_train,
                preffix: str,
                dir='./models'):

    model_name = f'{preffix}_model'
    model_path = os.path.join(dir, model_name)

    if not os.path.exists(dir):
        os.makedirs(dir)
        logging.info(f"criado o diretório [{os.path.relpath(dir)}] para armazenamento dos modelos treinados.")

    if os.path.isfile(model_path):
        with open(model_path, 'rb') as file:
            model = joblib.load(file)

        logging.info(f'model loaded from {model_path}')
        return model

    # Fit the classifier to the training data
    model = model_instance.fit(x_train, y_train)

    with open(model_path, 'wb') as file:
        joblib.dump(model, file, ('bz2', 4))

    logging.info(f'model trained and saved at {model_path}')

    return model