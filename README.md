# Project2

We've used python3 for this project\
To run the scripts, install these dependencies using requirements.txt\
pip3 install -r requirements.txt

## Client-server

Functionality:\
    Clients connect to server and are asked to introduce a username.\
    They take a Covid19 survey and answer multiple questions.\
    Depending on the answers, the client is recommeded to take a test or it's informed that he/she is fine.\
    If server stops running, clients stop as well.
    
To run files:\
python3 server.py\
python3 clientDoctor.py\
python3 client.py (open as many terminal windows as clients you desire)\
Important to start server process before any client.

![demo](images/demo.png)

## Heatmap

Heatmap of what our service would look like if like 2500 people use it:\
To generate it go into the heatmap direcrory and run:\
python3 heatmap.py\
![heatmap](images/heatmapimg.png)

## GUI

We have tried to implement a small GUI to improve the UX with the program\
gui.py file was made to run the GUI version of client.py\
It would still need work to fix some errors (therefore, client.py file should be ran for testing the code as shown above)

![Gui_1](images/gui_1.PNG)
![Gui_2](images/gui_2.PNG)

