from flask import Flask, request, render_template, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
import bonobo
import threading
from nodes.NameNodes import *


app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"  # Set a secret key for SocketIO
socketio = SocketIO(app)
Bootstrap(app)
datepicker(app)



@app.route("/")
def input_screen():
    return render_template("input.html")


@app.route("/trigger_chain", methods=["POST"])
def trigger_chain():
    max_num = int(request.form['max_num'])
    thread = threading.Thread(target=run_chain, args=[max_num])
    thread.start()
    return render_template("input.html")


@socketio.on("connect")
def handle_connect():
    socketio.emit("status", {"message": "connected"})  # Send initial status


def run_chain(num_items: int):
    graph = bonobo.Graph()
    graph.add_chain(NameProducer(num_items), NameTransformer(), NameConsumer())
    bonobo.run(graph, services={'status': socketio})
    socketio.emit("status", {"message": "finished"})  # Send initial status


@app.route("/status")
def status_screen():
    return render_template("status.html", chain_running=chain_running)


if __name__ == "__main__":
    socketio.run(app, allow_unsafe_werkzeug=True, debug=True)
