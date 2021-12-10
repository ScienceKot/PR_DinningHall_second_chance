# Importing all needed libraries.
from flask import Flask, request
import json
import threading
import time
from dinning_hall import DinningHall

# Defining the dinning hall settings.
menu = json.load(open('menu.json', 'r'))
dinning_hall_settings = json.load(open("dinning_hall_settings.json", 'r'))
dinning_hall_settings['menu'] = menu

dinning_hall_obj = None

# Building the flask app.
app = Flask(__name__)

@app.route('/distribution', methods=['POST'])
def distribute_order():
    # Getting the distribution as a json.
    distribution = request.json

    # Notifying the dinning hall that the order was made.
    dinning_hall_obj.notify_order_recieve(distribution)

    print(dinning_hall_obj.marks)
    return ""

if __name__ == "__main__":
    # Running a thread for the flask application.
    threading.Thread(target=lambda: app.run(debug=True, use_reloader=False, port=3000, host="127.0.0.1",)).start()

    # Creating the dinning hall object and running the main function.
    dinning_hall_obj = DinningHall(dinning_hall_settings)
    dinning_hall_obj.run()




