from flask import render_template, request, flash, redirect, url_for, session
from blog import app, db
from blog.models import Entry
from blog.forms import EntryForm, LoginForm
import functools

def login_required(view_func):
    @functools.wraps(view_func)
    def check_permissions(*args, **kwargs):
        if session.get("logged_in"):
            return view_func(*args, **kwargs)
        return redirect(url_for("login", next=request.path))
    return check_permissions

@app.route("/")
def home():     
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts = all_posts)

@app.route("/add-post/", methods=["GET", "POST"])
@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
@login_required
def add_mod_entry(entry_id=None):
    errors = None
    if not entry_id:
        action = "Dodaj nowy"
        form = form = EntryForm()
    else:
        action = "Modyfikuj"
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        form = EntryForm(obj=entry)
    if request.method == "POST":
        if not entry_id:
            if form.validate_on_submit():
                entry = Entry(
                    title=form.title.data, 
                    body=form.body.data,
                    is_published = form.is_published.data
                )
                db.session.add(entry)
                if form.is_published.data == True:
                    flash(f'Wpis "{form.title.data}" został opublikowany')
                else:
                    flash(f'Wpis "{form.title.data}" został dodany bez publikacji')
            else:
                erros = form.errors
        elif entry_id:
            if form.validate_on_submit():
                form.populate_obj(entry)
                flash(f'Wpis "{form.title.data}" został zmodyfikowany')
            else:
                errors = form.errors
        db.session.commit()
    return render_template("post.html", form=form, errors=errors, action=action)    

@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get("next")
    if request.method == "POST":
        if form.validate_on_submit():
            session["logged_in"] = True
            session.permanent = True 
            flash("Zalogowano!", "success")
            return redirect(next_url or url_for("home"))
        else:
            errors = form.errors
    return render_template("login.html", form=form, errors=errors)


@app.route("/logout/", methods=["GET", "POST"])
def logout():
    if request.method == "POST":
        session.clear()
        flash("Wylogowano!", "success")        
    return redirect(url_for("home"))