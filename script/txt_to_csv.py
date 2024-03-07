import csv
import os


lyrics_folder_path = 'Ariana Grande'

artist_name = os.path.basename(lyrics_folder_path)
# Le chemin complet du fichier CSV
csv_file_path = os.path.join(lyrics_folder_path, f"{artist_name}.csv")

# titre de csv
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Artist', 'Title', 'Lyrics'])

   
    for filename in os.listdir(lyrics_folder_path):
        if filename.endswith('.txt'):
            
            title = filename.replace('.txt', '')
            
            with open(os.path.join(lyrics_folder_path, filename), 'r', encoding='utf-8') as file:
                lyrics = file.read()
            
            csvwriter.writerow([artist_name, title, lyrics])

print(f"Le fichier CSV a été généré：{csv_file_path}")
