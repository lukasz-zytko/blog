from faker import Faker
from blog.models import Entry, db

def fake_entries(how_many=10):
    fake = Faker()

    for i in range(how_many):
        post = Entry(
            title = fake.sentence(),
            body = "\n".join(fake.paragraphs(15)),
            pub_date = fake.date_between(start_date="-3y"),
            is_published = False 
        )
        db.session.add(post)
    db.session.commit()
