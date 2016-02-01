from pymongo import MongoClient
import os

dbClient = MongoClient("mongodb://localhost:27017")
db = dbClient.lantas_hackathon
cursor = db.users.find({},{"_id":1 , "email":1})

target_file = open("users-dump.json" , 'w')
target_file.truncate()

dumped_users=0
for document in cursor:
	doc_to_write = {
		"_id":{"$oid":str(document["_id"])},
		"email":str(document["email"])
	}
	target_file.write("%s\n" % str(doc_to_write))
	
	dumped_users+=1
	if (dumped_users % 1000) == 0:
		print "dumped_users: %d" % dumped_users

target_file.close()
dbClient.close()