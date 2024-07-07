from flask import Flask, render_template, request, redirect, url_for
from flask_paginate import Pagination, get_page_parameter
from peewee import *
import pypdf

# Database configuration
db = SqliteDatabase('studyapp_sora.db')

# Database table configurations
class Students(Model):
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    hurigana_first_name = CharField(max_length=255)
    hurigana_last_name = CharField(max_length=255)
    school = CharField(max_length=255)
    grade = CharField(max_length=255)
    student_comments = CharField(max_length=255)

    class Meta:
        database = db
    
class TestResults(Model):
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
    testresult_comments = CharField(max_length=255)

    class Meta:
        database = db

class LearningReports(Model):
    learn_date = DateField()
    grade = CharField(max_length=255)
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    course = CharField(max_length=255)
    subject = CharField(max_length=255)
    text = TextField()
    learningreport_comments = CharField(max_length=255)

    class Meta:
        database = db

db.create_tables([Students, TestResults, LearningReports])

app = Flask(__name__)

# 学習記録追加
@app.route("/home/learningreport_add", methods=['GET', 'POST'])
def add_learningreport():
    if request.method == 'POST':
        learn_date = request.form['learn_date']
        grade = request.form['grade']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        course = request.form['course']
        subject = request.form['subject']
        learningreport_comments = request.form['learningreport_comments']

        # Extract text from uploaded PDF
        file = request.files['text']
        pdf_reader = pypdf.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Save to database
        LearningReports.create(
            learn_date=learn_date,
            grade=grade,
            first_name=first_name,
            last_name=last_name,
            course=course,
            subject=subject,
            text=text,
            learningreport_comments=learningreport_comments
        )
        db.close()
        return redirect(url_for('add_learningreport'))
    return render_template('/learningreport_templates/learningreport_add.html')

if __name__ == "__main__":
    app.run(debug=True)
