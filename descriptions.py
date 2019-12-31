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


@app.route("/descriptions/<track>/<user_name>",methods=['GET'])
def get_descbyuser(track,user_name):
	try:
		sqlQry = "select C.track_title,A.user_name,A.track_desc from descriptions A, users B, tracks C where a.user_name = b.user_name and c.track_id = a.track_id and c.track_title = '%s' and a.user_name = '%s'" %(track,user_name)
		db =  get_db()
		rs = db.execute(sqlQry)
		res = rs.fetchall()
		rs.close()

	except Exception as e:
        	return { 'error': str(e) }, status.HTTP_404_NOTFOUND
	
	return jsonify(list(res)), status.HTTP_200_OK


@app.route("/descriptions",methods=['POST'])
def create_trackdesc():
	mandatory_fields = ['track_title','user_name','track_description']

	if not all([field in request.data for field in mandatory_fields]):
        	raise exceptions.ParseError()
	try:
		track_title = request.data.get('track_title','')
		user_name   = request.data.get('user_name','')
		track_desc  = request.data.get('track_description','')
		
		sqlQry = "insert into descriptions(user_name,track_id,track_desc) values ('%s',(select track_id from tracks where track_title='%s'),'%s')" %(user_name,track_title,track_desc)	
		db = get_db()
		db.execute(sqlQry)
		db.commit()
		response  = Response(status=201)
		response.headers['location'] = '/descriptions/'+track_title+'/'+user_name
		response.headers['status'] = '201 Created'
	except Exception as e:
        	return { 'error': str(e) }, status.HTTP_404_NOTFOUND

	return response, status.HTTP_201_CREATED


if __name__ == "__main__":
	app.run(debug=True)
	