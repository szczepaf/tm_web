from flask import Flask, render_template
import practice_utils
app = Flask(__name__)

@app.get("/")
def index():
    return render_template('index_v5.html')

@app.get("/kontakt")
def contacts():
    return render_template('kontakt.html')

@app.get("/treninky")
def practices():
    practices = practice_utils.get_trainings()
    return render_template('treninky.html', practices=practices)

@app.get("/tym")
def team():
    return render_template("team.html")

@app.get("/ultimate")
def ultimate():
    return render_template('ultimate.html')

if __name__ == '__main__':
    app.run()
