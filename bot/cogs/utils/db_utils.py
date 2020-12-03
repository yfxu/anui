import pymongo

# create document for user if they do not exist in 'stats' database
def ensure_stats_user_exists(mongo_client, user):
	try:
		client = mongo_client['stats']['users']
		if client.find_one({'user': user.id}) == None:
			client.insert_one({'user': user.id})
	except Exception as e:
		print(f"{e}: could not create user in db")


# increment a stats field for any user
def stats_increment(mongo_client, user, field, value=1):
	ensure_stats_user_exists(mongo_client=mongo_client, user=user)
	try:
		client = mongo_client['stats']['users']
		client.update_one({'user': user.id}, {'$inc': {field: value}})
	except Exception as e:
		print(f"{e}: could not increment {field} for {user} in db")


# get a user's profile stats
def get_user(mongo_client, user):
	profile_template = {
		'sneks': {
			'send_count': 0,
			'recv_count': 0
		},
		'smaks': {
			'send_count': 0,
			'recv_count': 0	
		},
		'xd': {
			'count': 0
		}
	}

	client  = mongo_client['stats']['users']
	profile = client.find_one({'user': user.id}, {'_id': False, 'user': False})

	for stat in profile.keys():
		if stat in profile_template:
			profile_template[stat].update(profile[stat])

	return profile_template
