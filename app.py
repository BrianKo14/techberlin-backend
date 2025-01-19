from flask import Flask, request, send_file, Response
from flask_cors import CORS
import json

from interview import interview_loop 
import matches


app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:8080", "http://127.0.0.1:8080"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})


turn_counter = 0
MAX_TURNS = 5


# ----------------- API ENDPOINTS -----------------

# INTERVIEW ENDPOINTS

@app.route('/interview/start-interview', methods=['GET'])
def start_interview():
	""" Returns the audio file with the first question and initializes dialogue history. """
	global turn_counter
	turn_counter = 0
	print(f"Turn counter - StartInterview: {turn_counter}")
	next_question_path, context_dialogue = interview_loop.start_interview()

	# Get new audio data
	with open(next_question_path, 'rb') as audio_file:
		audio_data = audio_file.read()

	# Prepare response payload
	response_payload = {
		'context_dialogue': context_dialogue,
		'audio_data': audio_data.hex()
	}

	return Response(json.dumps(response_payload), mimetype='application/json')


@app.route('/interview/next-question', methods=['POST'])
def next_question():
	""" Receives the user's audio response and dialogue history.
	    Returns the audio file with the next question and updated dialogue history. """
	
	# Get audio data and convert from hex to wav
	global turn_counter
	turn_counter += 1
	print(f"Turn counter - NextQuestion: {turn_counter}")
	file = request.files['audio']
	audio_hex = file.read().hex()
	audio_bytes = bytes.fromhex(audio_hex)
	
	save_path = 'nlp/recorded_audio.wav'
	with open(save_path, 'wb') as f:
		f.write(audio_bytes)

	# Get dialogue history
	context_dialogue = request.form['metadata']
	context_dialogue = json.loads(context_dialogue)	

	if turn_counter >= MAX_TURNS:
		# End the interview
		interview_loop.save_transcript(context_dialogue)
		return Response(json.dumps({'done': 'Max turns reached.'}), status=201)
	
	# Continue the interview
	next_question_path, context_dialogue = interview_loop.continue_interview(context_dialogue, save_path)

	# Get new audio data
	with open(next_question_path, 'rb') as audio_file:
		audio_data = audio_file.read()

	# Prepare response payload
	response_payload = {
		'context_dialogue': context_dialogue,
		'audio_data': audio_data.hex()
	}

	return Response(json.dumps(response_payload), mimetype='application/json')



# MATCHES ENDPOINTS

@app.route('/matches/get-matches', methods=['GET'])
def get_matches():
	""" Returns an object with the user's matches. """
	return matches.get_matches()

@app.route('/matches/ask-question', methods=['POST'])
def ask_question():
	""" Receives a question and returns the answer. """
	data = request.get_json()
	dialogue_history = data['dialogue_history']
	question = data['question']
	user_id = data['user_id']

	print(f"Dialogue history: {dialogue_history}")
	print(f"Question: {question}")
	print(f"User ID: {user_id}")

	return matches.ask_question(dialogue_history, question, user_id)

# ------------------------------------------------


if __name__ == '__main__':
	app.run(debug=True)
