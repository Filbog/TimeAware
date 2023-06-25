from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "fq)4540sd#@e&&tpe6v3kjl7!w1k=7^)#6-dfmqf44m7xj"


@app.route("/")
def hello():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
