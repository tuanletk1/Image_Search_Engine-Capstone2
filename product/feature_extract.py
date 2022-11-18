import os

from tensorflow import keras
from keras.applications.vgg19 import VGG19, preprocess_input
from keras.models import Model

from PIL import Image
import pickle
import numpy as np

from ISE.settings import DATA_DIR


class FeatureExtract:

  def extract_model(self):
    vgg19_model = VGG19(weights='imagenet')
    extract_model = Model(
      inputs=vgg19_model.inputs,
      outputs=vgg19_model.get_layer('fc1').output,
    )
    return extract_model

  def image_preprocess(self, img):
    img = img.resize((224, 224))
    img = img.convert("RGB")
    result = keras.preprocessing.image.img_to_array(img)
    result = np.expand_dims(result, axis=0)
    result = preprocess_input(result)
    return result

  def extract_vector(self, model, image_path):
    img = Image.open(image_path)
    img_tensor = self.image_preprocess(img)

    vector = model.predict(img_tensor)[0]
    vector = vector / np.linalg.norm(vector)
    return vector

  def vector_handle(self, data_folder, model, vectors, paths):
    for image_path in os.listdir(data_folder):
      print(image_path)
      image_full_path = os.path.join(DATA_DIR / data_folder, image_path)
      image_vector = self.extract_vector(model, image_full_path)
      vectors.append(image_vector)
      paths.append(image_full_path)

  def store(self):
    model = self.extract_model()
    paths = []
    vectors = []
    for shop in os.listdir(DATA_DIR):
      data_folder = DATA_DIR / shop
      for folder in os.listdir(data_folder):
        self.vector_handle(data_folder / folder, model, vectors, paths)
        vectors_file = "static/training/" + folder + "_vectors.pkl"
        paths_file = "static/training/" + folder + "_paths.pkl"
        pickle.dump(vectors, open(vectors_file, 'wb'))
        pickle.dump(paths, open(paths_file, 'wb'))
        vectors.clear()
        paths.clear()
    self.merge_training()

  def merge_training(self):
    training_data_path = "static/training/"
    vectors = []
    paths = []
    for file in os.listdir(training_data_path):
      if "_paths" not in file:
        with open(training_data_path + file, 'rb') as f:
          vectors = vectors + pickle.load(f)
        continue
      with open(training_data_path + file, 'rb') as f:
        paths = paths + pickle.load(f)
    pickle.dump(paths, open('static/search/paths.pkl', 'wb'))
    pickle.dump(vectors, open('static/search/vectors.pkl', 'wb'))

  def search(self, search_image):
    model = self.extract_model()
    search_vector = self.extract_vector(model, search_image)
    vectors = pickle.load(open("static/search/vectors.pkl", 'rb'))
    paths = pickle.load(open("static/search/paths.pkl", 'rb'))
    print(search_vector)
    distance = np.linalg.norm(vectors - search_vector, axis=1)
    samples = 20
    ids = np.argsort(distance)[:samples]
    results = [(paths[id].split('\\')[-1].split('.')[0], distance[id]) for id in ids]
    return results
