from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

#chlist = ["E1","E2","E3","E4","E5","E6","E7","E8","E9","E10","E11","E12","E13","E14","E15","E16","E17","E18"]
chlist = []
for i in range(64):
	chlist.append("E"+str(i+1))

def randomNumberGenerator():
	"""
	Generate a random number every 1 second and emit to a socketio instance (broadcast)
	Ideally to be run in a separate thread?
	"""
	#infinite loop of magical random numbers
	#print("Making random numbers")
	df = pd.read_csv('/../../processed_right_hand_data.txt', header=0, index_col=0)
	df = df.drop("E65", axis = 1)
	size = len(df.index)
	while not thread_stop_event.isSet():		
		for i in range(0,size,10):
			data = []
			for j in range(64):
				dic = {}
				dic.update({"ch": chlist[j]})
				dic.update({"val": abs(df.loc[i,chlist[j]])})
				data.append(dic)
			socketio.emit('newnumber', {'number': data}, namespace='/test')
			socketio.sleep(0.01)
        
@app.route("/")
def home():
	return render_template("EEG_index.html")
	#return "hello this is a main page <h1>Hello</h1>"
	
@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(randomNumberGenerator)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host= '0.0.0.0', debug=True)
