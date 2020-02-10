from imdb import IMDb, IMDbError

db = IMDb()

file = open('movies_to_watch.txt')
lines = file.readlines()
movies_dict = {}

for line in lines:
    try:
        matching_movies = db.search_movie(line)
        movie = matching_movies[0]
        id = movie.movieID
        movie = db.get_movie(id, info=['main'])
        title = movie['title']
        genres = movie['genres']
        genres_len = len(genres)
        for i in range(genres_len):
            if genres[i] not in ['Biography', 'Adventure', 'Mystery']:
                genre = genres[i]
                break
        year = movie['year']
        directors = movie['directors']
        director = directors[0]
        cast = movie['cast']
        stars = cast[:2]
        if genre not in movies_dict.keys():
            movies_dict[genre] = [[title, year, director, stars]]
        else:
            movies_dict[genre].append([title, year, director, stars])
    except (KeyError, IndexError, IMDbError) as e:
        print(e)
        print(title)

output = open('test_suggested.txt', 'a')

sorted_dict = dict(sorted(movies_dict.items(), key=lambda x: x[0].lower()))

for key, value in sorted_dict.items():
    first_entry = True
    if first_entry:
        output.write(f'{key}:\n')
        first_entry = False
    value.sort(key=lambda x: x[0])
    for v in value:
        try:
            output.writelines(f'{v[0]} ({v[1]}) directed by {v[2]} starring {v[3][0]} and {v[3][1]}\n')
        except (KeyError, IndexError, IMDbError) as e:
            print(e)
            print(v[0])
    output.write('\n')
