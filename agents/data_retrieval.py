
# NOTE: Here we provide a draft for the data retrieval module.
# In a real-world scenario, having a large user-base would require a more sophisticated database
# for dealing with semantic information. Weaviate and Haystack are necessary frameworks for building this infrastructure.
# Agents will become multi-dimensional beyond single-file personality guidelines, and the matchmaker algorithm
# needs to be able to efficiently digest and retrieve this knowledge.

import json, os

current_dir = os.path.dirname(os.path.abspath(__file__))

USERS_REF_PATH = "../data/users-reference.json"
USERS_REF_PATH = os.path.join(current_dir, USERS_REF_PATH)

AGENTS_REF_PATH = "../data/agents/"
AGENTS_REF_PATH = os.path.join(current_dir, AGENTS_REF_PATH)


def get_user_data(id):
	
	with open(USERS_REF_PATH, 'r') as f:
		users = json.load(f)

	return users["users"][id]


def get_agent(id):

	print(f"Getting agent path: {AGENTS_REF_PATH + 'agent-' + str(id) + '.txt'}")
	with open(AGENTS_REF_PATH + "agent-" + str(id) + ".txt", 'r') as f:
		agent = f.read()

	return agent