import os
import numpy as np
import re
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import pandas as pd

def calculate_mapping_length(artist):
    # Charger le fichier CSV correspondant à l'artiste
    data = pd.read_csv(f'./corpus/{artist}.csv')

    # Analyser les paroles
    wholelist = []
    for lyrics in data.lyrics:
        cleaned_lyrics = lyrics.lower()
        wholelist.append(cleaned_lyrics)

    wordlist = []
    for song in wholelist:
        songlist = song.split()
        wordlist.extend(songlist)

    # Analyser les titres
    wholelist2 = []
    for title in data.title:
        cleaned_title = title.lower()
        wholelist2.append(cleaned_title)

    wordlist2 = []
    for name in wholelist2:
        namelist = name.split()
        wordlist2.extend(namelist)

    # Fusionner les listes de mots
    finlist = wordlist2 + wordlist

    # Créer le mapping
    unique_chars = sorted(set(finlist))
    mapping = {w:i for i,w in enumerate(unique_chars)}
    reverse_mapping={i:w for w,i in mapping.items()}

    return mapping,reverse_mapping

def generate_title_features(title, mapping, max_title_length):
    title_seq = [mapping.get(char, 0) for char in title][:max_title_length]
    title_features = pad_sequences([title_seq], maxlen=max_title_length, padding='post', value=0)
    return title_features

def lyrics_generator(model, mapping, reverse_mapping, starter, title, ch, max_title_length, l_symb):
    generated = starter
    title_features = generate_title_features(title, mapping, max_title_length)

    seed = [mapping.get(char, 0) for char in starter[-40:]]  # Taking the last 40 characters as seed
    seed_padded = pad_sequences([seed], maxlen=40, padding='post', value=0)  # Ensuring fixed length for seed
    seed_padded = np.reshape(seed_padded, (1, 40, 1)) / float(l_symb)  # Normalizing

    for _ in range(ch):
        prediction = model.predict([title_features, seed_padded], verbose=0)[0]
        prediction = np.asarray(prediction).astype('float64')
        prediction = np.log(prediction + 1e-7)  # Avoiding log of 0
        exp_preds = np.exp(prediction)
        prediction = exp_preds / np.sum(exp_preds)
        next_index = np.argmax(np.random.multinomial(1, prediction, 1))
        next_char = reverse_mapping[next_index]

        generated += next_char
        generated+=' '
        new_seed = np.append(seed_padded[0, 1:, :], [[next_index / float(l_symb)]], axis=0)
        seed_padded = np.reshape(new_seed, (1, 40, 1))

    return generated

if __name__ == "__main__":
    import argparse

    # Setting up argument parser
    parser = argparse.ArgumentParser(description="Generate lyrics based on given parameters.")
    parser.add_argument("--artist", type=str, help="Name of the artist")
    parser.add_argument("--title", type=str, default="The Great Adventure", help="Title text")
    parser.add_argument("--starter", type=str, default="I am missing her <c> ", help="Starter text")
    parser.add_argument("--ch", type=int, default=200, help="Number of characters to generate")
    args = parser.parse_args()

    # Load the model
    model_path = os.path.join("../model", f"{args.artist}.h5")
    if os.path.exists(model_path):
        model=load_model(f'../model/{args.artist}.h5')
        print('Success : find your model.')
    else:
        raise FileNotFoundError(f"Model for artist {args.artist} not found")

    # Fixed values
    max_title_length = 20
    mapping,reverse_mapping =calculate_mapping_length(args.artist)
    l_symb=len(mapping)
    

    generated_text = lyrics_generator(model, mapping, reverse_mapping, args.starter+'<c>', args.title,
                                      args.ch, max_title_length, l_symb)

    # Printing generated lyrics
    generated_text = re.sub(r'<c>', '\n', generated_text)
    print(generated_text)
