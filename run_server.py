from pymongo import MongoClient
from flask import Flask, request
from flask_restful import Api, Resource
import json , time , sys

class discoverUsers(Resource):

	def post(self):
		time_start = (time.time())
		list_of_emails_in_phonebook = json.loads(request.data)
		list_of_user_objects_in_server = self.get_users_from_server()
		matched_users = self.crossmatch_app_users(
			list_of_emails_in_phonebook , 
			list_of_user_objects_in_server
		)
		time_end = (time.time())
		return {
			"matched_users": matched_users,
			"time_taken": time_end - time_start,
			"num_of": {
				"emails_in_phonebook": len(list_of_emails_in_phonebook),
				"users_in_server": len(list_of_user_objects_in_server),
				"common_emails": len(matched_users)
			}
		} , 200


	def get_users_from_server(self):
		time_db_begin = (time.time())
		dbClient = MongoClient("mongodb://localhost:27017")
		db = dbClient.lantas_hackathon
		list_of_user_objects = []
		cursor = db.users.find({},{
			"_id":1 , "email":1
		})
		for document in cursor:
			list_of_user_objects.append({
				'id'   :    str(document['_id']),
				'email':    document['email']
			})
		dbClient.close()
		time_db_end = (time.time())
		print "--- %f seconds to get %d users from Database (sys-size: %d)" % (
			time_db_end-time_db_begin , 
			len(list_of_user_objects) , 
			sys.getsizeof(list_of_user_objects)
		)
		return list_of_user_objects


	def crossmatch_app_users(self, list_of_emails_in_phonebook , list_of_user_objects_in_server):
		# return self.crossmatch_app_users_by_nested_forloop_lookup(list_of_emails_in_phonebook , list_of_user_objects_in_server)
		return self.crossmatch_app_users_by_hashmap_lookup(list_of_emails_in_phonebook , list_of_user_objects_in_server)


	def crossmatch_app_users_by_nested_forloop_lookup(self , list_of_emails_in_phonebook , list_of_user_objects_in_server):
		list_of_common_users = []
		time_nestmatch_begin = (time.time())
		for phonebook_email in list_of_emails_in_phonebook:
			for user_object in list_of_user_objects_in_server:
				if user_object['email'] == phonebook_email:
					list_of_common_users.append({
						'uid': user_object['id']	,
						'email': user_object['email']
					})
		time_nestmatch_end = (time.time())
		print "--- %d seconds to compare %d contacts with %d users via nested for-loop lookup" % (
			time_nestmatch_end-time_nestmatch_begin , 
			len(list_of_emails_in_phonebook),
			len(list_of_user_objects_in_server)
		)
		return list_of_common_users


	def crossmatch_app_users_by_hashmap_lookup(self , list_of_emails_in_phonebook , list_of_user_objects_in_server):
		list_of_common_users = []
		user_map = {}

		time_usermap_begin = (time.time())*1000
		for a_user_object in list_of_user_objects_in_server:
			user_map[a_user_object['email']] = a_user_object['id']
		time_usermap_end = (time.time())*1000
		print "--- %f milliseconds to map out %d users to hashmap" % (
			time_usermap_end-time_usermap_begin , 
			len(user_map)
		)

		time_hashmatch_begin = (time.time())*1000*1000
		for phonebook_email in list_of_emails_in_phonebook:
			user_id = user_map.get(phonebook_email)
			if user_id is not None:
				list_of_common_users.append({
					'user_id': user_id,
					'email': phonebook_email
				})
		time_hashmatch_end = (time.time())*1000*1000
		print "--- %f microseconds to compare %d contacts with %d users via hashmap lookup" % (
			time_hashmatch_end-time_hashmatch_begin , 
			len(list_of_emails_in_phonebook),
			len(user_map)
		)

		return list_of_common_users


app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True

api = Api(app)
api.add_resource(discoverUsers, '/users/discover' , '/users/discover/')

if __name__ == '__main__':
	app.run(debug=True)