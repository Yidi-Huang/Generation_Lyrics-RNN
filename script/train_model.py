# -*- coding: utf-8 -*-
import argparse
import pandas as pd
import numpy as np
import re
from keras.models import Model
from keras.layers import Input, LSTM, Dense, Embedding, concatenate
from keras.optimizers import Adamax
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import seaborn as sns

def preprocess_data(filepath):
   
    data = pd.read_csv(filepath)
    print("Size of Dataset:", data.shape)

    # pretraitement
    wholelist = [lyrics.lower() for lyrics in data.lyrics]
    wholelist2 = [title.lower() for title in data.title]

    wordlist = []
    lyricslist = []
    for song in wholelist:
        songlist = song.split()
        wordlist.extend(songlist)
        lyricslist.append(songlist)

    wordlist2 = []
    titlelist = []
    for name in wholelist2:
        namelist = name.split()
        wordlist2.extend(namelist)
        titlelist.append(namelist)

    finlist = wordlist2 + wordlist

    print(len(titlelist), len(lyricslist))
    unique_chars = sorted(set(finlist))
    print(unique_chars)

    mapping = {w: i for i, w in enumerate(unique_chars)}
    reverse_mapping = {i: w for w, i in mapping.items()}

    
    features = []
    targets = []
    title_features_expanded = []
    length = 40  # longuer du séquence
    max_title_length = 15  # max longueur titre

    for i in range(len(lyricslist)):
        title_seq = [mapping.get(w, 0) for w in titlelist[i]][:max_title_length]
        title_seq_padded = pad_sequences([title_seq], maxlen=20, padding='post', value=0)[0]

        for j in range(0, len(lyricslist[i]) - length, 1):
            feature_seq = lyricslist[i][j:j+length]
            if j+length < len(lyricslist[i]):  # vérification du target_w
                target_w = lyricslist[i][j+length]
                features.append([mapping.get(w, 0) for w in feature_seq])
                targets.append(mapping.get(target_w, 0))
                title_features_expanded.append(title_seq_padded)  # Ajoutez un titre à chaque caractéristique
    features = pad_sequences(features, maxlen=length, padding='post', value=0)
    features = np.reshape(features, (len(features), length, 1)) / float(len(mapping))
    targets = to_categorical(targets, num_classes=len(mapping))
    
    title_features_expanded = np.array(title_features_expanded)

    return features, targets, title_features_expanded, len(mapping)

def define_and_compile_model(input_dim, vocab_size):
    # définition du modèle
    lyrics_input = Input(shape=(input_dim, 1), name='lyrics_input')
    title_input = Input(shape=(20,), name='title_input')  # longuer du titre 20

    title_embedding = Embedding(input_dim=vocab_size, output_dim=50, input_length=20)(title_input)
    title_lstm = LSTM(128)(title_embedding)

    lyrics_lstm = LSTM(256)(lyrics_input)

    combined = concatenate([title_lstm, lyrics_lstm])
    output = Dense(vocab_size, activation='softmax')(combined)

    model = Model(inputs=[title_input, lyrics_input], outputs=output)
    model.compile(optimizer=Adamax(learning_rate=0.005), loss='categorical_crossentropy')

    return model

def plot_learning_curves(history):
    history_df = pd.DataFrame(history.history)
    plt.figure(figsize=(15,4))
    sns.lineplot(data=history_df['loss'], label="Loss")
    plt.title("Model Loss Over Epochs")
    plt.ylabel("Loss")
    plt.xlabel("Epoch")
    plt.show()


def main(csv_filepath):
    features, targets, title_features_expanded, vocab_size = preprocess_data(csv_filepath)
    model = define_and_compile_model(features.shape[1], vocab_size)
    model.summary()

    #trainer model
    history = model.fit([title_features_expanded, features], targets, batch_size=128, epochs=100)
    
    # garder model
    model.save("lana-delrey-model.h5")
    print("Model saved to lana-delrey-model.h5")

    # La courbe d'apprentissage
    plot_learning_curves(history)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train a model on the given dataset.')
    parser.add_argument('csv_filepath', type=str, help='The filepath to the csv file containing the dataset.')
    
    args = parser.parse_args()
    main(args.csv_filepath)
