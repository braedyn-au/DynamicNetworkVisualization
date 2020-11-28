from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event
from scipy.stats import pearsonr
import pandas as pd
import numpy as np


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#net analysis thread
thread = Thread()
thread_stop_event = Event()

def randomNumberGenerator():
    """
    Generate a random number every 1 second and emit to a socketio instance (broadcast)
    Ideally to be run in a separate thread?
    """
    #infinite loop of magical random numbers
    print("Making random numbers")
    while not thread_stop_event.isSet():
		
	#you can read file using pandas and run a loop to read lines.
	
	
		# Reads only 60000 lines from the file.
		df = pd.read_csv('processed_left_hand_data.txt', header=0, index_col=0, nrows = 60000, delimiter = ",\s+")
		df = df.drop(df.keys()[-1], axis = 1)

		threshold = 0.05
		network = 'Weighted network'   
		header = df.columns.tolist()
		l = len(header)

		totsize = len(df.index)
		timestep = 512

		print(header)
		for k in range(0,totsize,timestep):
		
			print(k)
			
			df1 = df.iloc[k:k+timestep]
			
			# print("DF1: ",df1)

			# ADJ_corr = np.zeros((l,l))
			nodei = []
			nodej = []
			weight = []

			for i in range(l):
				# ADJ_corr[i][i] = 1  # setting the diagonal elements 
				for j in range(i+1,l):
					
					# converting value to interger were taking more time than taking floating point number.
					# print(np.asarray(df1[header[i]]))
					[corr_TS, Pval_TS] = pearsonr(df1[header[i]], df1[header[j]])

					if Pval_TS < threshold:
						nodei.append(i)
						nodej.append(j)
						if network == 'Weighted network':
							# ADJ_corr[i][j] = corr_TS
							# ADJ_corr[j][i] = corr_TS
							weight.append(corr_TS)
						else:    
							# ADJ_corr[i][j] = 1
							# ADJ_corr[j][i] = 1
							weight.append(1)
	
			# You need to send the adjcent matrix. Perhaps sending it as object would be better
			print(nodei,nodej,weight)
			socketio.emit('newnetwork', {'node1': nodei, 'node2':nodej, 'weight':weight}, namespace='/network')
			socketio.sleep(2.0)

@app.route("/")
def home():
	return render_template("BrainDynamics.html")
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
