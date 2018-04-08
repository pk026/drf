from django.http import HttpResponse
from drf_exercise.models.song import Song
from drf_exercise.models.song import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
import collections
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

# Endpoint to list all entities (done)
# Endpoint to list related songs for a given song, sorted accordingly
# Endpoint to list all songs for a given tag (done)
# Endpoint to search for songs (done)
# Endpoint to search for artist (done)
# Endpoint to list all songs for a given artist (done)



@cache_page(60 * 15)
def index(request):
	# print(Song.objects.filter(tag__tag_name="rock").count())
	# print(Song.objects.filter(tag__tag_name="rock").order_by('-tag__score').count())
	# print(Song.objects.filter(tag__tag_name="rock").order_by('-tag__score').distinct().count())
	all_songs = Song.objects.all()

	songs = paginate(all_songs, request.GET.get('page'))

	#song_output = collections.OrderedDict()
	#song_list = []
	# for song in songs:
	# 	song_output = {}
	# 	song_output["track_id"] = song.track_id
	# 	song_output["title"] = song.title
	# 	song_output["artist_name"] = song.artist_name
	# 	song_output["timestamp"] = song.timestamp
	# 	song_output["similars"] = [each for each in song.similars]
	# 	tag_list = []
	# 	for tag in song.tags.all():
	# 		if tag:
	# 			tag_list.append({
	# 				"tag_name" : tag.tag_name,
	# 				"tag_score" : tag.score
	# 			})
	# 	song_output["tags"] = tag_list
	# 	song_list.append(song_output)
	return render_to_response('songs.html', {'songs': songs, 'a':"3"})

def fetch_by_tag(request):
	song_search_term = request.GET.get("tag-search")
	song_by_tag = Song.objects.filter(tags__tag_name__iexact=song_search_term.strip())
	songs = paginate(song_by_tag, request.GET.get('page'))
	return render_to_response('songs.html', {'songs': songs})

def fetch_by_song(request):
	song_search_term = request.GET.get("song-search")
	song_by_name = Song.objects.filter(title__icontains=song_search_term.strip())
	songs = paginate(song_by_name, request.GET.get('page'))
	return render_to_response('songs.html', {'songs': songs})

def fetch_by_artist(request):
	song_search_term = request.GET.get("artist-search")
	songs_by_artist = Song.objects.filter(artist_name__icontains=song_search_term.strip())
	songs = paginate(songs_by_artist, request.GET.get('page'))
	return render_to_response('songs.html', {'songs': songs})

def show(request):
	song_id = request.GET.get("id")
	songs = Song.objects.filter(track_id=song_id)
	return render_to_response('show.html', {'songs': songs})

def fetch_similar_songs(request):
	song_search_term = request.GET.get("song-title")
	songs = Song.objects.filter(title__icontains=song_search_term.strip())
	return render_to_response('show.html', {'songs': songs})

def paginate(songs, page):
	paginator = Paginator(songs, 10)

	try:
		songs = paginator.get_page(page)
	except PageNotAnInteger:
		songs = paginator.get_page(1)
	except EmptyPage:
		songs = paginator.get_page(paginator.num_pages)
	return songs

