import json

if __name__ == '__main__':
    with open('genres.txt', 'r', encoding='utf-8') as f:
        line = f.readline()
        genres = {}
        while line:
            genre_text, name = line.split('=')
            # genre_ids = genre_text.split('|')
            genres[genre_text] = name.replace('\n', '')
            line = f.readline()

        print(json.dumps(genres, ensure_ascii=False))
