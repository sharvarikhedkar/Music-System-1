import sys
import flask_api
from flask import request, g, jsonify, Response
from flask_api import FlaskAPI,status, exceptions
import sqlite3

app = FlaskAPI(__name__) 

def get_db():
	db = getattr(g,'_database', None)
	if db is None:
		db = g._database = sqlite3.connect('music.db')
	return db


# To get all plalists
@app.route("/playlists",methods=['GET'])
def get_all_playlists():
	try:
		sqlQry = "select playlist_id,playlist_title,user_name,created_date from playlists"		
		db =  get_db()
		rs = db.execute(sqlQry)
		
		res = rs.fetchall()
		rs.close()
	except Exception as e:
        	return { 'error': str(e) }, status.HTTP_404_NOTFOUND
	
	return jsonify(list(res)), status.HTTP_200_OK


#To get particular playlist info
@app.route("/playlists/<playlist_id>",methods=['GET'])
def get_playlist(playlist_id):
	try:
		sqlQry = "select user_name,playlist_title,created_date from playlists where playlist_id = '%s'" %playlist_id
		db =  get_db()
		rs = db.execute(sqlQry)
		res = rs.fetchall()
		rs.close()
	except Exception as e:
        	return { 'error': str(e) }, status.HTTP_404_NOTFOUND

	return jsonify(list(res)), status.HTTP_200_OK


#To get all playlist by a user 
@app.route("/playlistsbyuser/<user_name>",methods=['GET'])
def get_user_playlists(user_name):
	try:
		sqlQry = "select A.playlist_id,A.playlist_title,A.description,A.created_date from playlists A, users B where a.user_name = b.user_name and a.user_name = '%s'" %user_name		
		db =  get_db()
		rs = db.execute(sqlQry)
		res = rs.fetchall()
		rs.close()
	except Exception as e:
        	return { 'error': str(e) }, status.HTTP_404_NOTFOUND

	return jsonify(list(res)), status.HTTP_200_OK


#To create playlists of a user
@app.route("/playlists",methods=['POST'])
def create_playlists():
	mandatory_fields = ['playlist_title','user_name','track_title']

	if not all([field in request.data for field in mandatory_fields]):
        	raise exceptions.ParseError()

	playlist_title = request.data.get('playlist_title','')
	user_name = request.data.get('user_name','')
	description = request.data.get('description','')
	track_title = request.data.get('track_title','')
	
	db = get_db()
	try:
		sqlQry1 = "insert into playlists(user_name,playlist_title,description) values ('%s','%s','%s')" %(user_name,playlist_title,description)
		db.execute(sqlQry1)
		
		sqlQry2 = "insert into playlist_tracks(playlist_id,track_id) values ((select max(playlist_id) from playlists ),(select track_id from tracks where track_title ='%s'))" %track_title
		db.execute(sqlQry2)
		db.commit()
		response  = Response(status=201)
		response.headers['location'] = '/playlistsbyuser/'+user_name
		response.headers['status'] = '201 Created'

	except Exception as e:
        	return { 'error': str(e) }, status.HTTP_409_CONFLICT

	
	return response, status.HTTP_201_CREATED

#To delete a playlist
@app.route("/playlists/<playlist_title>",methods=['DELETE'])
def delete_playlist(playlist_title):
	try:
		db = get_db()
		sqlQry = "delete from playlist_tracks where playlist_id = (select playlist_id from playlists where playlist_title ='%s')" %playlist_title
		rs = db.execute(sqlQry)
		
		sqlQry = "delete from playlists where playlist_title ='%s'" %playlist_title
		rs = db.execute(sqlQry)
		
	except Exception as e:
        	return { 'error': str(e) }, status.HTTP_404_NOTFOUND

	db.commit()
	return "Playlist deleted successfully", status.HTTP_200_OK


if __name__ == "__main__":
	app.run(debug=True)
	