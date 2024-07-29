from peewee import *
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import login_manager

db = SqliteDatabase('studyapp_sora.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(UserMixin, BaseModel):
    username = CharField(unique=True)
    password_hash = CharField()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Students(BaseModel):
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    hurigana_first_name = CharField(max_length=255)
    hurigana_last_name = CharField(max_length=255)
    school = CharField(max_length=255)
    grade = CharField(max_length=255)
    student_comments = CharField(max_length=255)

class TestResults(BaseModel):
    test_date = DateField()
    test_name = CharField(max_length=255)
    user_total_rank = IntegerField()
    all_total_rank = IntegerField()
    grade = CharField(max_length=255)
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    subject_one = CharField(max_length=255)
    subject_two = CharField(max_length=255)
    subject_three = CharField(max_length=255)
    subject_four = CharField(max_length=255)
    subject_five = CharField(max_length=255)
    score_one = IntegerField()
    score_two = IntegerField()
    score_three = IntegerField()
    score_four = IntegerField()
    score_five = IntegerField()
    user_rank_one = IntegerField()
    user_rank_two = IntegerField()
    user_rank_three = IntegerField()
    user_rank_four = IntegerField()
    user_rank_five = IntegerField()
    all_rank_one = IntegerField()
    all_rank_two = IntegerField()
    all_rank_three = IntegerField()
    all_rank_four = IntegerField()
    all_rank_five = IntegerField()

class LearningReports(BaseModel):
    learn_date = DateField()
    grade = CharField(max_length=255)
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    course = CharField(max_length=255)
    subject = CharField(max_length=255)
    used_text = CharField(max_length=255)
    learningreport_comments = CharField(max_length=255)

class TextData(BaseModel):
    text_name = CharField(max_length=255)
    text = TextField()
    pdf_data = BlobField()

db.connect()
db.create_tables([User, Students, TestResults, LearningReports, TextData])

@login_manager.user_loader
def load_user(user_id):
    return User.get(User.id == user_id)