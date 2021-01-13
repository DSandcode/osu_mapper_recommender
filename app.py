from flask import Flask, render_template, request, redirect

from src.make_player_recomendation import *

# from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():

    if request.method == "POST":

        req = request.form

        missing = list()

        for k, v in req.items():
            if v == "":
                missing.append(k)

        if missing:
            feedback = f"Missing fields for {', '.join(missing)}"
            return render_template("sign_up.html", feedback=feedback)

        return redirect(request.url)

    return render_template("sign_up.html")


@app.route("/player", methods=["GET", "POST"])
def player_id():

    return render_template("player.html")


@app.route("/rec", methods=["GET", "POST"])
def recomendation():
    player_id = 0
    if request.method == "GET":
        # print(request.args)
        req = request.args
        player_id = req["u"]

    p_df = make_player_recomendation(player_id)
    # print(p_df.head(20))

    df_head = p_df.head(20)
    mapids = df_head["beatmapid"].to_numpy()
    setids = df_head["beatmapsetid"].to_numpy()
    zipped_list = zip(mapids, setids)
    return render_template("rec.html", recs=zipped_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
