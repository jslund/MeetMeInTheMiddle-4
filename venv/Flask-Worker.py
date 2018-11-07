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

    return render_template(
        "search.html",
        travel_time = int(statistics.mean(values[1])),
        results = values[0]
    )
