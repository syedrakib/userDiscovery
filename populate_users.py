from pymongo import MongoClient
dbClient = MongoClient("mongodb://localhost:27017")
db = dbClient.lantas_hackathon
time_to_populate_users_in_server = 0


def make_a_random_email():
	import random
	providers = ['gtail' , 'yakoo' , 'dotmail' , 'outbook' , 'solmail' , 'lsn']
	TLDs = ['co.uk' , 'com' , 'net' , 'org' , 'co.in' , 'co.fr' , 'info' , 'com.bd' , 'pk']
	possible_username_lengths = [8,12]
	username = ''.join(random.choice("0123456789abcdefghijklmnopqrstuvwxyz-_.") for i in range(1,random.choice(possible_username_lengths)))
	a_new_random_email = "%s@%s.%s" % (username , random.choice(providers) , random.choice(TLDs))
	return a_new_random_email


def make_a_user_object(email=None):
	import random
	if not email:
		email = make_a_random_email()
	user_object = {
		"email": 		email ,
		"password": 	"".join(random.choice("0123456789abcdefghijklmnopqrstuvwxyz-_.") for i in range(1,24)) ,
		"username": 	"".join(random.choice("0123456789abcdefghijklmnopqrstuvwxyz-_.") for i in range(1,random.choice([6,8,10,12,14]))) ,
		"first_name":	"".join(random.choice("0123456789abcdefghijklmnopqrstuvwxyz-_.") for i in range(1,random.choice([4,6,8,10,12,14]))) ,
		"last_name": 	"".join(random.choice("0123456789abcdefghijklmnopqrstuvwxyz-_.") for i in range(1,random.choice([4,6,8,10,12,14]))) ,
	}
	return user_object


def populate_users_in_server():
	import time
	time_start = time.time()
	db.users.drop()
	num_of_users_to_populate_in_server = 10000
	print "populating %d users in server..." % num_of_users_to_populate_in_server
	for i in range(num_of_users_to_populate_in_server):
		db.users.insert_one(make_a_user_object())	
		if (i>1) and ((i%10000)==0):
			print "..... %d users inserted" % db.users.count()
	db.users.insert_one(make_a_user_object("shatil@gmail.com"))
	db.users.insert_one(make_a_user_object("saurav@gmail.com"))
	db.users.insert_one(make_a_user_object("rezwan@gmail.com"))
	db.users.insert_one(make_a_user_object("simanto@gmail.com"))
	db.users.insert_one(make_a_user_object("raihan@gmail.com"))
	db.users.insert_one(make_a_user_object("dibosh@gmail.com"))
	time_end = time.time()
	global time_to_populate_users_in_server
	time_to_populate_users_in_server = time_end - time_start


def pretty_print_all_users_in_server():
	return
	import pprint
	list_of_user_objects = []
	cursor = db.users.find()
	for document in cursor:
		pprint.pprint(document)


def get_number_of_users_in_server():
	return db.users.count()


populate_users_in_server()
pretty_print_all_users_in_server()
num_of_users_in_server = get_number_of_users_in_server()


dbClient.close()


print "%f seconds to populate %d users in server" % (time_to_populate_users_in_server , num_of_users_in_server)


