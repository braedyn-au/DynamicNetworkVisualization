# DynamicNetworkVisualization
NeuroNexus Competition

If you are making a localhost to run the html file, make sure you make localhost in the parent folder where you have all the files and folders together. While running index.html file on the browser, simply go to the folder where you have index.html file and run it.

When you run websocket_server_EEG.py file, if will not start sending data until client side is connected to the designated port setup by the websocket in the python code. You have to make a local lost in the parent folder where you have all your files related to the visualization. Once you run the index.html file, python code will start sending data to the client side which you can see on the browser itself.

Smaller_EEGfile.csv is the 10000 timepoints for all channels as a pre-processed data file. It is part of the original file named as 1.csv which can be found using the link-https://www.kaggle.com/broach/button-tone-sz


