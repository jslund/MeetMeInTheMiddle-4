from flask import Flask, render_template, request
import MMITMWorker, statistics, Main

app = Flask(__name__)

@app.route('/')
def index_page():
    return render_template(
        "index.html"
    )


@app.route('/search')
def searcher():

    #addresses = ["w53nw", "nw53dn", "ec2r8ah"]

    addresses = [(request.args.get('firstaddress',type=str)),request.args.get('secondaddress',type=str),request.args.get('thirdaddress',type=str)]
    values = Main.main_function(addresses)
    best_location = values[2]

    return render_template(
        "search.html",
        average_travel_time = str(int(best_location['average_time'])/60),
        origins = best_location['travel_times'],
        location = best_location['location'],
        results = values[0]
    )
