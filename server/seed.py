#!/usr/bin/env python3

from random import randint
from faker import Faker

from app import app
from models import db, Article, User

fake = Faker()

with app.app_context():

    print("Deleting all records...")
    Article.query.delete()
    User.query.delete()

    print("Creating users...")
    users = []
    usernames = []
    for _ in range(25):
        username = fake.first_name()
        while username in usernames:
            username = fake.first_name()
        usernames.append(username)

        user = User(username=username)
        users.append(user)

    db.session.add_all(users)
    db.session.commit()  # Commit so IDs are available

    print("Creating articles...")
    articles = []
    for _ in range(100):
        content = fake.paragraph(nb_sentences=8)
        preview = content[:25] + '...'

        article = Article(
            author=fake.name(),
            title=fake.sentence(),
            content=content,
            preview=preview,
            minutes_to_read=randint(1, 20),
            user_id=users[randint(0, len(users) - 1)].id
        )

        articles.append(article)

    db.session.add_all(articles)
    db.session.commit()

    print("✅ Seeding complete!")
