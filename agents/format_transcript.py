
import mistral_service
import json



def get_transcript(filename):
	with open(filename, 'r') as f:
		transcript = f.read()

	return transcript



def format_transcript(transcript):

	prompt = f"""
	Here is the transcript of a call between an AI agent and a human:

	<being transcript> 
	{transcript}
	<end transcript>

	Extract the following information from the transcript:
	- Name of the user.
	- Age of the user.
	- Which languages they speak.
	- A brief summary of their hobbies.

	Return the information in JSON format. Reply with the JSON object. That is, your response should being with a '{' and end with a '}'.
	
	Format fields template: 
		"Name": ?,
		"Age": ?,
		"Languages": [?, ?, ...]
		"Hobbies": <brief summary>
	"""

	response = mistral_service.ask_mistral(
		prompt,
		response_format = { "type": "json_object" },
		model = "ministral-3b-latest"
	)

	return json.loads(response)



def generate_agent(transcript):

	prompt = f"""
	Here is the transcript of a call between an AI agent and a human:

	<being transcript>
	{transcript}
	<end transcript>

	Generate a personality profile for an AI agent that will pretend to be the human in the call.
	Include in this profile general instructions on how the agent should behave, and an extensive description of the human.
	"""

	response = mistral_service.ask_mistral(prompt)

	return response



def generate_dialogue(transcript1, transcript2):

	person1 = format_transcript(transcript1)
	print("Transcript 1 formatted.")
	person2 = format_transcript(transcript2)
	print("Transcript 2 formatted.")

	agent1 = generate_agent(transcript1)
	print("Agent 1 generated.")
	agent2 = generate_agent(transcript2)
	print("Agent 2 generated.")

	prompt = f"""
	
	Here is a description of {person1["Name"]}:
	{agent1}

	Here is a description of {person2["Name"]}:
	{agent2}

	Generate a message history between the two people. The dialogue should be a friendly conversation between two people who have just met.
	Don't copy from their profiles, but invent an original conversation that reflects their profiles but does not showcase them directly.

	The dialogue should start off the following prompt: "If you could choose to have a superpower, what would that be?"

	Max. length: 10 turns.
	"""

	return mistral_service.ask_mistral(prompt)



def evaluate_dialogue(dialogue):

	prompt = f"""
	Here is a dialogue between two people who have just met:

	<begin dialogue>
	{dialogue}
	<end dialogue>

	We are evaluating the dialogue to decide if the two people will become a match.
	Return a JSON object with the following fields:
	- "Similarity": <score from 1 to 10>
	- "Compatibility": <score from 1 to 10>
	- "Summary": <two-line summary of the evaluation>
	"""

	return mistral_service.ask_mistral(
		prompt,
		response_format = { "type": "json_object" }
	)


james_transcript = get_transcript("transcript_james.txt")
emma_agent = get_transcript("transcript_emma.txt")

dialogue = generate_dialogue(james_transcript, emma_agent)
print(dialogue)

evaluation = evaluate_dialogue(dialogue)
print(evaluation)