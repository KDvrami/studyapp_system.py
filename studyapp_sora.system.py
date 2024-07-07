from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_paginate import Pagination, get_page_parameter
from peewee import *
from io import BytesIO
import pypdf

#データベースの設定
db = SqliteDatabase('studyapp_sora.db')

#データベースのテーブル設定
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
    user_total_rank = IntegerField
    all_total_rank = IntegerField
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

class TextData(Model):
    text_name = CharField(max_length=255)
    text = TextField()
    pdf_data = BlobField()

    class Meta:
        database = db

db.create_tables([Students, TestResults, LearningReports, TextData])
    
app = Flask(__name__)

#ログイン画面
@app.route("/sora_login", methods=['GET'])
def login():
    return render_template('others_templates/sora_login.html')

#home画面
@app.route("/home", methods=['GET'])
def home():
    return render_template('/others_templates/home.html')


#生徒追加画面
@app.route("/home/student_add", methods=['GET','POST'])
def add_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        hurigana_first_name = request.form['hurigana_first_name']
        hurigana_last_name = request.form['hurigana_last_name']
        school = request.form['school']
        grade = request.form['grade']
        student_comments = request.form['student_comments']

        Students.create(
            first_name=first_name,
            last_name=last_name,
            hurigana_first_name=hurigana_first_name,
            hurigana_last_name=hurigana_last_name,
            school=school,
            grade=grade,
            student_comments=student_comments
        )
        db.close()
        return redirect(url_for('add_student'))
    return render_template('/student_templates/student_add.html')


#生徒一覧画面
@app.route("/home/student_all", methods=['GET'])
def all_student():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    total = Students.select().count()
    students = Students.select().paginate(page, per_page)

    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap5')

    return render_template('/student_templates/student_all.html', students=students, pagination=pagination)


#ハンドルケース1:表示する生徒がいない場合
@app.route("/home/student_all/no_student", methods=['GET'])
def handleone_all_student():
    students = Students.select()
    if not students:
        no_students_message = "No students found."
        return render_template('/student_templates/student_all.html', no_students_message = no_students_message)
    

#ハンドルケース2:要求されたページがページ合計より多い場合
@app.route("/home/student_all/invalid_page", methods=['GET'])
def handletwo_all_student():
    students = Students.select()

    page_number = request.args.get('page', default = 1, type = int)
    per_page = 10

    paginator = Pagination(data=students, per_page=per_page)

    if page_number > paginator.total_pages:
        invalid_page_message = "Invalid page number"
        return render_template('/student_templates/student_all.html', invalid_page_message = invalid_page_message)


#生徒詳細画面
@app.route("/home/student_all/student_detail_<int:student_id>", methods=['GET'])
def detail_student(student_id):
    student = Students.get(Students.id == student_id)
    return render_template('/student_templates/student_detail.html', student=student)


#生徒情報編集
@app.route("/home/student_all/student_detail_<int:student_id>/student_edit", methods=['GET','POST'])
def edit_student(student_id):
    student = Students.get(Students.id == student_id)
    if request.method == 'POST':
        student.first_name = request.form['first_name']
        student.last_name = request.form['last_name']
        student.hurigana_first_name = request.form['hurigana_first_name']
        student.hurigana_last_name = request.form['hurigana_last_name']
        student.school = request.form['school']
        student.grade = request.form['grade']
        student.student_comments = request.form['student_comments']
        student.save()
        return redirect(url_for('edit_student', student_id=student_id))
    return render_template('/student_templates/student_edit.html', student = student)


# 学習記録一覧(全体)
@app.route("/home/learningreport_all", methods=['GET'])
def all_learningreport_all():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    total = LearningReports.select().count()
    learningreports = LearningReports.select().paginate(page, per_page)

    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap5')

    return render_template('/learningreport_templates/learningreport_all.html', learningreports=learningreports, pagination=pagination)


#ハンドルケース1:表示する生徒がいない場合
@app.route("/home/learningreport_all/no_learningreports", methods=['GET'])
def handleone_all_learningreport():
    learningreports = LearningReports.select()
    if not learningreports:
        no_learningreports_message = "No learning reports found."
        return render_template('/learningreport_templates/learningreport_all.html', no_learningreports_message = no_learningreports_message)
    

#ハンドルケース2:要求されたページがページ合計より多い場合
@app.route("/home/learningreport_all/invalid_page", methods=['GET'])
def handletwo_all_learningreport():
    learningreports = LearningReports.select()

    page_number = request.args.get('page', default = 1, type = int)
    per_page = 10

    paginator = Pagination(data=learningreports, per_page=per_page)

    if page_number > paginator.total_pages:
        invalid_page_message = "Invalid page number"
        return render_template('/learningreport_templates/learningreport_all.html', invalid_page_message = invalid_page_message)

#学習記録一覧(個別)
@app.route("/home/student_all/student_detail_<int:student_id>/learningreport_all", methods=['GET'])
def all_learningreport(student_id):
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    total = LearningReports.select().count()
    learningreports = LearningReports.select().paginate(page, per_page)

    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap5')

    return render_template('/learningreport_templates/learningreport_all.html', learningreports=learningreports, pagination=pagination)


#学習記録詳細
@app.route("/home/student_all/student_detail_<int:student_id>/learningreport_all_<int:learningreport_id>/learningreport_detail_<int:report_id>", methods=['GET'])
def detail_learningreport(student_id, learningreport_id, report_id):
    learningreport = LearningReports.get(LearningReports.id == report_id)
    return render_template('/learningreport_templates/learningreport_all.html', learningreport=learningreport)


#学習記録追加
@app.route("/home/learningreport_add", methods=['GET','POST'])
def add_learningreport():
    if request.method == 'POST':
        learn_date = request.form['learn_date']
        grade = request.form['grade']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        course = request.form['course']
        subject = request.form['subject']
        learningreport_comments = request.form['comments']

        #アップロードされたpdfからテキストを抽出
        file = request.files['text']
        pdf_reader = pypdf.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()

        #データベースに保存
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
        return render_template(url_for('add_learningreport'))
    return render_template('/learningreport_templates/learningreport_add.html')


#学習記録編集
@app.route("/home/student_all/student_detail_<int:student_id>/learningreport_all/learningreport_detail_<int:learningreport_id>/learningreport_edit", methods=['GET','POST'])
def edit_learningreport(student_id, learningreport_id):
    learningreport = LearningReports.get(LearningReports.id == learningreport_id)
    if request.method == 'POST':
        learningreport.learn_date = request.form['learn_date']
        learningreport.grade = request.form['grade']
        learningreport.first_name = request.form['first_name']
        learningreport.last_name = request.form['last_name']
        learningreport.course = request.form['course']
        learningreport.subject = request.form['subject']
        learningreport.text = request.form['text']
        learningreport.comments = request.form['comments']
        learningreport.save()
        return render_template(url_for('edit_learningreport', student_id=student_id, learningreport_id=learningreport_id))
    return render_template('/learningreport_templates/learningreport_edit.html',learningreport=learningreport)


#テスト結果一覧
@app.route("/home/testresult_all", methods=['GET'])
def all_testresult():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    total = TestResults.select().count()
    testresults = TestResults.select().paginate(page, per_page)

    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap5')

    return render_template('/testresult_templates/testresult_all.html', testresults=testresults, pagination=pagination)


#ハンドルケース1:表示する生徒がいない場合
@app.route("/home/testresult_all/no_testresults", methods=['GET'])
def handleone_all_testresult():
    testresults = TestResults.select()
    if not testresults:
        no_testresults_message = "No test results found."
        return render_template('/testresult_templates/testresult_all.html', no_testresults_message = no_testresults_message)
    

#ハンドルケース2:要求されたページがページ合計より多い場合
@app.route("/home/student_all/testresult_all/invalid_page", methods=['GET'])
def handletwo_all_testresult():
    testresults = TestResults.select()

    page_number = request.args.get('page', default = 1, type = int)
    per_page = 10

    paginator = Pagination(data=testresults, per_page=per_page)

    if page_number > paginator.total_pages:
        invalid_page_message = "Invalid page number"
        return render_template('/testresult_templates/testresult_all.html', invalid_page_message = invalid_page_message)

#テスト結果追加
@app.route("/home/testresult_add", methods=['GET','POST'])
def add_testresult():
    if request.method == 'POST':
        test_date = request.form['test_date']
        test_name = request.form['test_name']
        user_total_rank = request.form['user_total_rank']
        all_total_rank = request.form['all_total_rank']
        grade = request.form['grade']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        subject_one = request.form['subject_one']
        subject_two = request.form['subject_two']
        subject_three = request.form['subject_three']
        subject_four = request.form['subject_four']
        subject_five = request.form['subject_five']
        score_one = request.form['score_one']
        score_two = request.form['score_two']
        score_three = request.form['score_three']
        score_four = request.form['score_four']
        score_five = request.form['score_five']
        user_rank_one = request.form['user_rank_one']
        user_rank_two = request.form['user_rank_two']
        user_rank_three = request.form['user_rank_three']
        user_rank_four = request.form['user_rank_four']
        user_rank_five = request.form['user_rank_five']
        all_rank_one = request.form['all_rank_one']
        all_rank_two = request.form['all_rank_two']
        all_rank_three = request.form['all_rank_three']
        all_rank_four = request.form['all_rank_four']
        all_rank_five = request.form['all_rank_five']
        rank = request.form['rank']
        testresult_comments = request.form['comments']

        TestResults.create(
            test_date=test_date,
            test_name=test_name,
            grade=grade,
            first_name=first_name,
            last_name=last_name,
            subject_one=subject_one,
            subject_two=subject_two,
            subject_three=subject_three,
            subject_four=subject_four,
            subject_five=subject_five,
            score_one=score_one,
            score_two=score_two,
            score_three=score_three,
            score_four=score_four,
            score_five=score_five,
            rank=rank,
            testresult_comments=testresult_comments,
            user_total_rank=user_total_rank,
            all_total_rank=all_total_rank,
            user_rank_one=user_rank_one,
            user_rank_two=user_rank_two,
            user_rank_three=user_rank_three,
            user_rank_four=user_rank_four,
            user_rank_five=user_rank_five,
            all_rank_one=all_rank_one,
            all_rank_two=all_rank_two,
            all_rank_three=all_rank_three,
            all_rank_four=all_rank_four,
            all_rank_five=all_rank_five
        )
        db.close()
        return render_template(url_for('add_testresult'))
    return render_template('/testresult_templates/testresult_add.html')

#テスト結果詳細
@app.route("/home/testresult_all/testresult_detail_<int:testresult_id>", methods=['GET'])
def detail_testresult(testresult_id):
    testresult = TestResults.get(TestResults.id == testresult_id)
    return render_template('/testresult_templates/testresult_detail.html', testresult=testresult)

#テスト結果編集
@app.route("/home/testresult_all/testresult_detail_<int:testresult_id>/testresult_edit", methods=['GET','POST'])
def edit_testresult(testresult_id):
    testresult = TestResults.get(TestResults.id == testresult_id)
    if request.method == 'POST':
        testresult.test_date = request.form['test_date']
        testresult.test_name = request.form['test_name']
        testresult.grade = request.form['grade']
        testresult.first_name = request.form['first_name']
        testresult.last_name = request.form['last_name']
        testresult.subject_one = request.form['subject_one']
        testresult.subject_two = request.form['subject_two']
        testresult.subject_three = request.form['subject_three']
        testresult.subject_four = request.form['subject_four']
        testresult.subject_five = request.form['subject_five']
        testresult.score_one = request.form['score_one']
        testresult.score_two = request.form['score_two']
        testresult.score_three = request.form['score_three']
        testresult.score_four = request.form['score_four']
        testresult.score_five = request.form['score_five']
        testresult.rank = request.form['rank']
        testresult.comments = request.form['comments']
        return render_template(url_for('edit_testresult', testresult_id=testresult_id))
    return render_template("/testresult_templates/testresult_edit.html", testresult=testresult)


#テキスト追加
@app.route("/home/text_add", methods=['GET','POST'])
def add_textdata():
    if request.method == 'POST':
        text_name = request.form['text_name']

        #アップロードされたpdfからテキストを抽出
        file = request.files['text']
        pdf_reader = pypdf.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()

        #データベースに保存
        TextData.create(
            text_name=text_name,
            text=text,
            pdf_data=file.read()
        )
        db.close()
        return redirect(url_for('all_textdata'))
    return render_template('/text_templates/text_add.html')


#テキスト一覧
@app.route("/home/text_all", methods=['GET'])
def all_textdata():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    total = TextData.select().count()
    texts = TextData.select().paginate(page, per_page)

    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap5')

    return render_template('/text_templates/text_all.html', texts=texts, pagination=pagination)


#テキスト詳細
@app.route("/home/text_all/text_detail_<int:text_id>", methods=['GET'])
def detail_text(text_id):
    try:
        textdata = TextData.get(TextData.id == text_id)
    except TextData.DoesNotExist:
        return redirect(url_for('all_textdata'))
    return render_template('/text_templates/text_detail.html', textdata=textdata)


#PDF表示
@app.route("/home/text_all/text_detail_<int:text_id>/view_pdf", methods=['GET'])
def view_pdf(text_id):
    try:
        textdata = TextData.get(TextData.id == text_id)
    except TextData.DoesNotExist:
        return redirect(url_for('all_textdata'))
    
    return render_template(BytesIO(textdata.pdf_data), attachment_filename=f"{textdata.text_name}.pdf", as_attachment=False)


#テキスト編集(表示)
@app.route("/home/text_all/text_detail_<int:text_id>/text_edit", methods=['GET'])
def edit_text(text_id):
    try:
        text = TextData.get(TextData.id == text_id)
    except TextData.DoesNotExist:
        return redirect(url_for('all_textdata'))
    
    return render_template('/text_templates/text_edit.html', text=text)

#テキスト編集(保存)
@app.route("/home/text_all/text_detail_<int:text_id>/text_edit", methods=['POST'])
def save_edited_text(text_id):
    text = TextData.get_or_none(TextData.id == text_id)
    if text is None:
        return redirect(url_for('all_textdata'))
    
    text_name = request.form['text_name']
    file = request.files['text']
    pdf_reader = pypdf.PdfReader(file)
    extracted_text = ''
    for page in pdf_reader.pages:
        extracted_text += page.extract_text()

    #データベースを更新
    text.text_name = text_name
    text.text = extracted_text
    text.pdf_data = file.read()
    text.save()

    return redirect(url_for('all_textdata'))

       
if __name__ == '__main__':
    app.run(debug=True)