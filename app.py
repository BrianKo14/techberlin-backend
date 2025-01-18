from flask import Flask, request, send_file, Response

from interview import interview_loop 
import matches
import json


app = Flask(__name__)

turn_counter = 0
MAX_TURNS = 5


# ----------------- API ENDPOINTS -----------------

# INTERVIEW ENDPOINTS

@app.route('/interview/start-interview', methods=['GET'])
def start_interview():
	""" Returns the audio file with the first question and initializes dialogue history. """

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


@app.route('interview/next-question', methods=['POST'])
def next_question():
	""" Receives the user's audio response and dialogue history.
	    Returns the audio file with the next question and updated dialogue history. """
	
	# Get audio data
	file = request.files['audio']
	save_path = 'nlp/recorded_audio.wav'
	file.save(save_path)

	# Get dialogue history
	context_dialogue = request.form['metadata']
	context_dialogue = json.loads(context_dialogue)	

	turn_counter += 1
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



# ------------------------------------------------


if __name__ == '__main__':
	app.run(debug=True)
