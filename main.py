from flask import Flask, request, jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from functions import obtener_id


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)
URL_BASE = "https://t2-mfortiz3.herokuapp.com"


# 1. Hacemos los modelos

class Artist(db.Model):
  id = db.Column(db.String(22), primary_key=True)
  name = db.Column(db.String(200))
  age = db.Column(db.Integer)
  albums = db.Column(db.String(200))
  tracks = db.Column(db.String(200))
  self_url = db.Column(db.String(200))

  def __init__(self, name, age):
    self.id = obtener_id(name) 
    self.name = name
    self.age = int(age)
    self.albums = "%s/artists/%s/albums" % (URL_BASE, self.id)
    self.tracks = "%s/artists/%s/tracks" % (URL_BASE, self.id)
    self.self_url = "%s/artists/%s" % (URL_BASE, self.id)

class Album(db.Model):
  id = db.Column(db.String(22), primary_key=True)
  name = db.Column(db.String(50))
  genre = db.Column(db.String(50))
  artist = db.Column(db.String(200))
  tracks = db.Column(db.String(200))
  self_url = db.Column(db.String(200))

  def __init__(self, name, genre, artist_id):
    self.id = obtener_id(name, artist_id)
    self.name = name
    self.genre = genre
    self.artist = "%s/artists/%s" % (URL_BASE, artist_id)
    self.tracks = "%s/albums/%s/tracks" % (URL_BASE, self.id)
    self.self_url = "%s/albums/%s" % (URL_BASE, self.id)


class Track(db.Model):
  id = db.Column(db.String(22), primary_key=True)
  name = db.Column(db.String(200))
  duration = db.Column(db.Float)
  times_played = db.Column(db.Integer)
  artist = db.Column(db.String(200))
  album = db.Column(db.String(200))
  self_url = db.Column(db.String(200))

  def __init__(self, name, duration, album_id):
    self.id = obtener_id(name, album_id)
    self.name = name
    self.duration = float(duration)
    self.times_played = 0
    self.artist = Album.query.get(album_id).artist
    self.album = "%s/albums/%s" % (URL_BASE, album_id)
    self.self_url = "%s/tracks/%s" % (URL_BASE, self.id)

# 2. Hacemos los esquemas o tablas
class ArtistSchema(ma.Schema):
  class Meta:
    fields = ('name', 'age', 'albums', 'tracks', 'self')


class AlbumSchema(ma.Schema):
  class Meta:
    fields = ('name', 'genre', 'artist', 'tracks', 'self')


class TrackSchema(ma.Schema):
  class Meta:
    fields = ('name', 'duration', 'times_played', 'artist', 'album', 'self')

artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True)

album_schema = AlbumSchema()
albums_schema = AlbumSchema(many=True)

track_schema = TrackSchema()
tracks_schema = TrackSchema(many=True)

###class Post(db.Model):
###    id = db.Column(db.Integer,primary_key =True)
###    title = db.Column(db.String(100))
###    description = db.Column(db.String(200))
###    author = db.Column(db.String(50))
###
###    def __init__(self,title,description,author):
###        self.title = title
###        self.description = description
###        self.author = author
###
###class PostSchema(ma.Schema):
###    class Meta:
###        fields = ("title","autor", "description")
###
###post_schema = PostSchema()
###posts_schema = PostSchema(many=True)


# 3. Hacemos las rutas con los métodos
## Artistas

@app.route('/artists', methods=['GET'])
def obtener_artistas():
  artistas = Artist.query.all()
  lista = []
  for artist in artistas:
    query = {'name': artist.name, 'age': artist.age, 'albums': artist.albums, 'tracks': artist.tracks, 'self': artist.self_url}
    lista.append(query)
  return json.dumps(lista), 200

@app.route('/artists/<artist_id>', methods=['GET'])
def obtener_artista_por_id(artist_id):
  artista = Artist.query.get(artist_id)
  if artista:
    query = {'name': artista.name, 'age': artista.age, 'albums': artista.albums, 'tracks': artista.tracks, 'self': artista.self_url}
    return json.dumps(query), 200
  return '', 404

@app.route('/artists/<artist_id>/albums', methods=['GET'])
def obtener_album_por_id_artista(artist_id):
  artista = Artist.query.get(artist_id)
  if not artista: 
      return '', 404
  lista = []
  albums = Album.query.all()
  final = [album for album in albums if '%s/artists/%s' % (URL_BASE, artist_id) == album.artist]
  for album in final:
      query = {'name': album.name, 'genre': album.genre, 'artist': album.artist, 'tracks': album.tracks, 'self': album.self_url}
      lista.append(query)
  return json.dumps(lista), 200

@app.route('/artists/<artist_id>/tracks', methods=['GET'])
def obtener_tracks_por_id_artista(artist_id):
  artista = Artist.query.get(artist_id)
  if not artista: 
      return '', 404
  lista = []
  tracks = Track.query.all()
  final = [track for track in tracks if '%s/artists/%s' % (URL_BASE, artist_id) == track.artist]
  for track in final:
      query = {'name': track.name, 'duration': track.duration, 'times_played': track.times_played, 'artist': track.artist, 'album': track.album, 'self': track.self_url}
      lista.append(query)
  return json.dumps(lista), 200

@app.route('/artists/<artist_id>/albums/play', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def error_1(artist_id):
  return '', 405

@app.route('/artists/<artist_id>/tracks/play', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def error_2(artist_id):
  return '', 405

##Albums
@app.route('/albums', methods=['GET'])
def obtener_albums():
  albums = Album.query.all()
  lista = []
  for album in albums:
    query = {'name': album.name, 'genre': album.genre, 'artist': album.artist, 'tracks': album.tracks, 'self': album.self_url}
    lista.append(query)
  return json.dumps(lista), 200

@app.route('/albums/<album_id>', methods=['GET'])
def obtener_album_por_id(album_id):
  album = Album.query.get(album_id)
  if album:
    query = {'name': album.name, 'genre': album.genre, 'artist': album.artist, 'tracks': album.tracks, 'self': album.self_url}
    return json.dumps(query), 200
  return '', 404

@app.route('/albums/<album_id>/tracks', methods=['GET'])
def obtener_tracks_por_album(album_id):
  album = Album.query.get(album_id)
  if not album:
    return '', 404
  lista = []
  tracks = Track.query.all()
  final = [track for track in tracks if '%s/albums/%s' % (URL_BASE, album_id) == track.album]
  for track in final:
    query = {'name': track.name, 'duration': track.duration, 'times_played': track.times_played, 'artist': track.artist, 'album': track.album, 'self': track.self_url}
    lista.append(query)
  return json.dumps(lista), 200


## Tracks
@app.route('/tracks', methods=['GET'])
def obtener_tracks():
  tracks = Track.query.all()
  lista = []
  for track in tracks:
    query = {'name': track.name, 'duration': track.duration, 'times_played': track.times_played, 'artist': track.artist, 'album': track.album, 'self': track.self_url}
    lista.append(query)
  return json.dumps(lista), 200

@app.route('/tracks/<track_id>', methods=['GET'])
def obtener_track_por_id(track_id):
  track = Track.query.get(track_id)
  if not track:
      return '', 404
  if track:
    query = {'name': track.name, 'duration': track.duration, 'times_played': track.times_played, 'artist': track.artist, 'album': track.album, 'self': track.self_url}
    return json.dumps(query), 200

@app.route('/tracks/<track_id>/play', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def error_3(artist_id):
  return '', 405
  
# Post

## Artistas
@app.route('/artists', methods=['POST'])
def crear_artista():
  try:
    name = request.json['name']
    age = request.json['age']
    nuevo = Artist(name, age)
  except:
    return '', 400
  repetido = Artist.query.get(nuevo.id)
  if repetido:
    query = {'name': repetido.name, 'age': repetido.age, 'albums': repetido.albums, 'tracks': repetido.tracks, 'self': repetido.self_url}
    return json.dumps(query), 409
  db.session.add(nuevo)
  db.session.commit()
  query = {'name': nuevo.name, 'age': nuevo.age, 'albums': nuevo.albums, 'tracks': nuevo.tracks, 'self': nuevo.self_url}
  return json.dumps(query), 201

@app.route('/artists/<artist_id>', methods=['POST', 'PUT', 'PATCH'])
def error_4(artist_id):
  return '', 405

@app.route('/artists/<artist_id>/tracks', methods=['POST', 'PUT', 'PATCH', 'DELETE'])
def error_5(artist_id):
  return '', 405

## Albums
@app.route('/artists/<artist_id>/albums', methods=['POST'])
def crear_album(artist_id):
  artist = Artist.query.get(artist_id)
  if not artist:
    return '', 422
  try:
    name = request.json['name']
    genre = request.json['genre']
    nuevo = Album(name, genre, artist_id)
  except:
    return '', 400
  repetido = Album.query.get(nuevo.id)
  if repetido:
    query = {'name': repetido.name, 'genre': repetido.genre, 'artist': repetido.artist, 'tracks': repetido.tracks, 'self': repetido.self_url}
    return json.dumps(query), 409
  db.session.add(nuevo)
  db.session.commit()
  query = {'name': nuevo.name, 'genre': nuevo.genre, 'artist': nuevo.artist, 'tracks': nuevo.tracks, 'self': nuevo.self_url}
  return json.dumps(query), 201

@app.route('/albums', methods=['POST', 'PUT', 'PATCH', 'DELETE'])
def error_6():
  return '', 405

@app.route('/albums/<album_id>', methods=['POST', 'PUT', 'PATCH'])
def error_7(album_id):
  return '', 405

## Tracks 
@app.route('/albums/<album_id>/tracks', methods=['POST'])
def crear_track(album_id):
  album = Album.query.get(album_id)
  if not album:
    return '', 422
  try:
    name = request.json['name']
    duration = request.json['duration']
    nuevo = Track(name, duration, album_id)
  except:
    return '', 400
  repetido = Track.query.get(nuevo.id)
  if repetido:
    query = {'name': repetido.name, 'duration': repetido.duration, 'times_played': repetido.times_played, 'artist': repetido.artist, 'album': repetido.album, 'self': repetido.self_url}
    return json.dumps(query), 409
  db.session.add(nuevo)
  db.session.commit()
  query = {'name': nuevo.name, 'duration': nuevo.duration, 'times_played': nuevo.times_played, 'artist': nuevo.artist, 'album': nuevo.album, 'self': nuevo.self_url}
  return json.dumps(query), 201


@app.route('/tracks', methods=['POST', 'PUT', 'PATCH', 'DELETE'])
def error_8():
  return '', 405

@app.route('/tracks/<track_id>', methods=['POST', 'PUT', 'PATCH'])
def error_9(track_id):
  return '', 405

# Delete

## Artistas
@app.route('/artists/<artist_id>', methods=['DELETE'])
def borrar_artista(artist_id):
  artist = Artist.query.get(artist_id)
  if not artist:
    return '', 404
  db.session.delete(artist)
  albums = Album.query.all()
  final = [album for album in albums if '%s/artists/%s' % (URL_BASE, artist_id) == album.artist]
  for album in final:
    db.session.delete(album)
  tracks = Track.query.all()
  final = [track for track in tracks if '%s/artists/%s' % (URL_BASE, artist_id) == track.artist]
  for track in final:
    db.session.delete(track)
  db.session.commit()
  return '', 204

## Albums
@app.route('/albums/<album_id>', methods=['DELETE'])
def borrar_album(album_id):
  album = Album.query.get(album_id)
  if not album:
    return '', 404
  db.session.delete(album)
  tracks = Track.query.all()
  final = [track for track in tracks if '%s/albums/%s' % (URL_BASE, album_id) == track.album]
  for track in final:
    db.session.delete(track)
  db.session.commit()
  return '', 204

## Tracks
@app.route('/tracks/<track_id>', methods=['DELETE'])
def borrar_track(track_id):
  track = Track.query.get(track_id)
  if not track:
    return '', 404
  db.session.delete(track)
  db.session.commit()
  return '', 204


# Put 

## Artistas
@app.route('/artists/<artist_id>/albums/play', methods=['PUT'])
def play_tracks_artista(artist_id):
  artist = Artist.query.get(artist_id)
  if not artist:
    return '', 404
  tracks = Track.query.all()
  final = [track for track in tracks if '%s/artists/%s' % (URL_BASE, artist_id) == track.artist]
  for track in final:
    track.times_played += 1
  db.session.commit()
  return '', 200

@app.route('/artists', methods=['PUT', 'PATCH', 'DELETE'])
def error_10():
  return '', 405

@app.route('/artists/<artist_id>/albums', methods=['PUT', 'PATCH', 'DELETE'])
def error_11(artist_id):
  return '', 405

## Albums
@app.route('/albums/<album_id>/tracks/play', methods=['PUT'])
def play_tracks_album(album_id):
  album = Album.query.get(album_id)
  if not album:
    return '', 404
  tracks = Track.query.all()
  final = [track for track in tracks if '%s/albums/%s' % (URL_BASE, album_id) == track.album]
  for track in final:
    track.times_played += 1
  db.session.commit()
  return '', 200

@app.route('/albums/<album_id>/tracks', methods=['PUT', 'PATCH', 'DELETE'])
def error_12(album_id):
  return '', 405

## Tracks
@app.route('/tracks/<track_id>/play', methods=['PUT'])
def play_track(track_id):
  track = Track.query.get(track_id)
  if not track:
    return '', 404
  track.times_played += 1
  db.session.commit()
  return '', 200

##@app.route('/get', methods = ['GET'])
##def get_post():
##    return jsonify({"Hello":"World"})
##
##@app.route('/post', methods = ['POST'])
##def add_pos():
##    title = request.json['title']
##    description = request.json['description']
##    author = request.json['author']
##    my_posts = Post(title,description, author)
##
##    db.session.add(my_posts)
##    db.session.commit()
##    return post_schema.jsonify(my_posts)



db.create_all()

if __name__ == "__main__":
    app.run(debug=True)