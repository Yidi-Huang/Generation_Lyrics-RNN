from lyricsgenius import Genius
import re
import os

token = "DHuxUejky4cCFT0T8hX8s3WzcPL_uC8X3A-PePrGU2JAjq5o2YlwUI8MJEQu79Xg"
genius = Genius(token,timeout=20)



artist_name = "Ariana Grande"

# Créer un répertoire nommé d'après le nom de l'artiste, en veillant à formater correctement le nom de l'artiste
artist_dir_name = re.sub(r'[\\/*?:"<>|]', "", artist_name)  # Supprimer les caractères non autorisés par le système dans les noms de fichiers
lyrics_dir = os.path.join(os.getcwd(), artist_dir_name)

if not os.path.exists(lyrics_dir):
    os.makedirs(lyrics_dir)

try:
    artist = genius.search_artist(artist_name, max_songs=53, sort='popularity')
    if artist:
        for song in artist.songs:
            # Formater le titre de la chanson en supprimant les caractères spéciaux
            song_title_clean = re.sub(r'[\\/*?:"<>|]', "", song.title)
            filepath = os.path.join(lyrics_dir, f"{song_title_clean}.txt")
            
            # Vérifier si les paroles ont été récupérées avec succès
            if song.lyrics:
                # Prétraitement des paroles de la chanson
                content = song.lyrics.split('\n', 1)[1] if '\n' in song.lyrics else ""  # Supprimer la première ligne
                content = re.sub(r'\[.*?\]', '', content)  # Supprimer [] et son contenu
                content = re.sub(r'\d+Embed+\b', '', content)  # Supprimer le mot 'Embed' et le nombre qui le précède
                content = re.sub(r'\(.*?\)', '', content)  #Supprimer les parenthèses et leur contenu
                content = re.sub(r'You might also like', '', content)  # Supprimer“You might also like”
                
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Lyric saved to：{filepath}")
            else:
                print(f"Not found lyric {song.title} ")
    else:
        print(f"Artiste non found：{artist_name}")
except Exception as e:
    print(f "An error has occurred during processing：{e}")