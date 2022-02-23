from flask import render_template, request, flash
from blog import app, db
from blog.models import Entry
from blog.forms import EntryForm

@app.route("/")
def home():     
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template("homepage.html", all_posts = all_posts)


@app.route("/add-post/", methods=["GET", "POST"])
def create_entry():
    form = EntryForm()
    errors = None
    typ = "Dodaj nowy"
    if request.method == "POST":
        if form.validate_on_submit():
            entry = Entry(
                title=form.title.data, 
                body=form.body.data,
                is_published = form.is_published.data
            )
            db.session.add(entry)
            db.session.commit()
            if form.is_published.data == True:
                flash(f'Wpis "{form.title.data}" został opublikowany')
            else:
                flash(f'Wpis "{form.title.data}" został dodany bez publikacji')
        else:
            errors = form.errors
    return render_template("post.html", form=form, errors=errors, type=typ)

@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    typ = "Modyfikuj"
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    form = EntryForm(obj=entry)
    errors = None
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(entry)
            db.session.commit()
            flash(f'Wpis "{form.title.data}" został zmieniony')
        else:
            errors = form.errors
    return render_template("post.html", form=form, errors=errors, type=typ)
