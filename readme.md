UserDiscovery
-
_**experimenting with user discovery algorithms for a social app in LantasHackathon on 30th January 2016 - ensuring stable & quick response for discovering users from among a user's phonebook contacts against an evergrowing directory of millions of app users in the application's database

[ClickHere][1] to see benchmarking results of the experiment.**_

Install the following python packages first:

    pip install pymongo
    pip install flask
    pip install flask_restful

install `MongoDB` and have it running on `localhost:27017` - no initial databases needed to be created for this exercise

Configure number of users you want to simulate in the MongoDB server by altering the `num_of_users_to_populate_in_server` variable in the `populate_users.py` file

    python populate_users.py 

----- allow some time for the python script to populate the selected number of dummy users into the MongoDB server

    python run_server.py

----- flask_restful app will run on `localhost:5000`

Copy entire contents of the file `phonebook.json` and make a `POST` request to `http://localhost:5000/users/discover/` by pasting the copied contents into the raw message body of the POST request. ----- note the value of the `time_taken` field inside the JSON response.

You may change the cross-matching algorithm by choosing between `nested_forloop_lookup()` or `hashmap_lookup()` by uncommenting the function call written inside the `crossmatch_app_users()` function in the `run_server.py` file. Repeat the `POST` request to retry with the chosen algorithm.

Recommended tools:
-
- Python VirtualEnv - to maitain an isolated virtual environment for this python exercise
- POSTMan REST Client - a standalone chrome app to make standard POST requests


  [1]: https://docs.google.com/spreadsheets/d/1xbuMt9X8IezyohmXNtIAot1oH5Ql2Hx4EWoLOm1MUqw/pubhtml?gid=0&single=true