from flask import Flask, request, jsonify

from interview import interview_loop 
import matches


app = Flask(__name__)


# ----------------- API ENDPOINTS -----------------

# INTERVIEW ENDPOINTS

@app.route('/interview/start-interview', methods=['GET'])
def start_interview():
	""" Returns the audio file with the first question. """
	pass

@app.route('interview/next-question', methods=['POST'])
def next_question():
	""" Receives the user's audio response and returns the next question's audio file.
	    Or indicate the end of the interview. """
	pass



# MATCHES ENDPOINTS

@app.route('/matches/get-matches', methods=['GET'])
def get_matches():
	""" Returns an object with the user's matches. """
	return matches.get_matches()



# ------------------------------------------------


if __name__ == '__main__':
	app.run(debug=True)
