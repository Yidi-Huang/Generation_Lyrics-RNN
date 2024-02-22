import csv
import re

def clean_csv(input_file):
    to_remove = ['{', '}', '~', '©', 'à', 'á', 'ã', 'ä', 'ç', 'è', 'ê', 'ë', 'í', 'ñ', 'ó', 'ö', 'ü', 'ŏ',
             'е', 'ا', 'س', 'ل', 'م', 'و', '\u2005', '\u200a', '\u200b', '–', '—', '‘', '’', '‚', '“', '”',
             '…', '\u205f', '\ufeff', '!', '&', '(', ')', '*', '-',  '/','"' ,'',"'",'[',']']
    rows = []
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            rows.append(row)
    wl=[]
    for row in rows:
        text=row[2]
        text = text.lower()
        text = re.sub(r'(\w+)\n\n',r'\1\n',text)
        text = re.sub(r'\s\n',r'\n',text)
        text = re.sub(r'^\n', '', text)
        text = re.sub(r'\n\n\n',r'\n',text)
        text = re.sub(r'(\W)\n(\w)', r'\1<c> \2', text)
        text = re.sub(r'(\w+)\n(\w+)', r'\1<c> \2', text)
        for char in to_remove:
            text=text.replace(char,'')
        
        wl.append(text)
    
    tl=[]
    for row in rows:
        title=row[1]
        title = title.lower()
        for char2 in to_remove:
            title=title.replace(char2,'')
        tl.append(title)

    for j in range(len(wl)):
        rows[j][2]=wl[j]

    for i in range(len(tl)):
        rows[i][1]=tl[i]

    with open(input_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)  


# Example usage:
clean_csv('nicki-minaj.csv')


