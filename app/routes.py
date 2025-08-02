from flask import render_template, request, redirect, url_for, flash, session
from . import db
from .models import DecisionInstance, Choice, Evaluation
from flask import current_app as app



# TEMPORARY AUTHENTICATION
CREATOR_CREDENTIALS = {
    "jean": "secure123",
    "alice": "mypassword",
    "bob": "letmein",
    "Paul-McKay": "login"
}


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form["name"]
        creator_id = request.form["creator_id"]
        return redirect(url_for("add_choices", name=name, creator_id=creator_id))
    return render_template("create.html")


@app.route("/add_choices", methods=["GET", "POST"])
def add_choices():
    name = request.args.get("name")
    creator_id = request.args.get("creator_id")

    if request.method == "POST":
        if "done" in request.form:
            scale = request.form["scale"].strip()
            choices = request.form.getlist("choice")
            descriptions = request.form.getlist("description")

            decision = DecisionInstance(name=name, scale=scale, creator_id=creator_id)
            db.session.add(decision)
            db.session.commit()

            for lbl, desc in zip(choices, descriptions):
                db.session.add(Choice(label=lbl, description=desc, decision_id=decision.id))
            db.session.commit()

            return render_template("share_links.html", decision=decision, url_root=request.url_root)

    return render_template("add_choices.html", name=name, creator_id=creator_id)


# @app.route("/add_choices/<name>", methods=["GET", "POST"])
# def add_choices(name):
#     if request.method == "POST":
#         if "done" in request.form:
#             scale = request.form["scale"].strip()
#             choices = request.form.getlist("choice")
#             descriptions = request.form.getlist("description")
#             decision = DecisionInstance(name=name, scale=scale)
#             db.session.add(decision)
#             db.session.commit()
#             for lbl, desc in zip(choices, descriptions):
#                 db.session.add(Choice(label=lbl, description=desc, decision_id=decision.id))
#             db.session.commit()
#             return render_template("share_links.html", decision=decision, url_root=request.url_root)
#
#     return render_template("add_choices.html", name=name)

@app.route("/evaluate/<decision_id>", methods=["GET", "POST"])
def evaluate(decision_id):
    decision = DecisionInstance.query.get_or_404(decision_id)
    choices = Choice.query.filter_by(decision_id=decision_id).all()
    scale = decision.scale.split(',')

    if request.method == "POST":
        user_name = request.form["user"]
        for choice in choices:
            score = request.form.get(f"score_{choice.id}")
            if score is not None:
                db.session.add(Evaluation(user_name=user_name, choice_id=choice.id, score=int(score), decision_id=decision_id))
        db.session.commit()
        flash("Your evaluation was saved!", "success")
        return render_template("thank_you.html")

    return render_template("evaluate.html", decision=decision, choices=choices, scale=scale)

@app.route("/results/<decision_id>")
def results(decision_id):
    from statistics import mean, median
    decision = DecisionInstance.query.get_or_404(decision_id)
    choices = Choice.query.filter_by(decision_id=decision_id).all()
    evaluations = Evaluation.query.filter_by(decision_id=decision_id).all()

    stats = []
    for c in choices:
        scores = [e.score for e in evaluations if e.choice_id == c.id]
        if scores:
            stats.append({
                "label": c.label,
                "description": c.description,
                "mean": round(mean(scores), 2),
                "median": median(scores),
                "count": len(scores)
            })

    winner = max(stats, key=lambda x: x['mean']) if stats else None
    return render_template("results.html", decision=decision, stats=stats, winner=winner)
#
# @app.route("/list")
# def list_decisions():
#     decisions = DecisionInstance.query.order_by(DecisionInstance.id.desc()).all()
#     return render_template("list.html", decisions=decisions)

@app.route("/share/<decision_id>")
def share_existing(decision_id):
    decision = DecisionInstance.query.get_or_404(decision_id)
    return render_template("share_links.html", decision=decision, url_root=request.url_root)

@app.route("/lookup", methods=["POST"])
def lookup():
    decision_id = request.form.get("decision_id")
    return redirect(url_for("evaluate", decision_id=decision_id))

@app.route("/creator/login", methods=["GET", "POST"])
def creator_login():
    if request.method == "POST":
        creator_id = request.form.get("creator_id")
        password = request.form.get("password")
        if creator_id in CREATOR_CREDENTIALS and CREATOR_CREDENTIALS[creator_id] == password:
            session["creator_id"] = creator_id
            return redirect(url_for("creator_dashboard", creator_id=creator_id))
        else:
            flash("Invalid login", "danger")
            return render_template("creator_login.html")
    return render_template("creator_login.html")


@app.route("/creator/logout")
def creator_logout():
    session.pop("creator_id", None)
    return redirect(url_for("home"))


@app.route("/creator/<creator_id>")
def creator_dashboard(creator_id):
    decisions = DecisionInstance.query.filter_by(creator_id=creator_id).all()
    return render_template("creator_dashboard.html", decisions=decisions)