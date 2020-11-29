import os

def get_data(target_file):
	data_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), f"../../data/{target_file}")
	f = open(data_file, 'r')
	data = f.read().splitlines()
	f.close()
	return data