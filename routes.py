from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required
from flask_paginate import Pagination, get_page_parameter
from models import Students, TestResults, LearningReports, TextData
from peewee import *
import os

main_bp = Blueprint('main', __name__)

db = SqliteDatabase('studyapp_sora.db')


@main_bp.before_request
def before_request():
    db.connect()

@main_bp.teardown_request
def teardown_request(exception):
    if not db.is_closed():
        db.close()


#home画面
@main_bp.route("/home", methods=['GET'])
@login_required
def home():
    return render_template('/others_templates/home.html')


#生徒追加画面
@main_bp.route("/home/student_add", methods=['GET','POST'])
@login_required
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
        return redirect(url_for('main.add_student'))
    return render_template('/student_templates/student_add.html')


#生徒一覧画面
@main_bp.route("/home/student_all", methods=['GET'])
@login_required
def all_student():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    total = Students.select().count()
    students = Students.select().paginate(page, per_page)
    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap5')
    return render_template('/student_templates/student_all.html', students=students, pagination=pagination)


#ハンドルケース1:表示する生徒がいない場合
@main_bp.route("/home/student_all/no_student", methods=['GET'])
@login_required
def handleone_all_student():
    students = Students.select()
    if not students:
        no_students_message = "No students found."
        return render_template('/student_templates/student_all.html', no_students_message = no_students_message)
    

#ハンドルケース2:要求されたページがページ合計より多い場合
@main_bp.route("/home/student_all/invalid_page", methods=['GET'])
@login_required
def handletwo_all_student():
    students = Students.select()

    page_number = request.args.get('page', default = 1, type = int)
    per_page = 10

    paginator = Pagination(data=students, per_page=per_page)

    if page_number > paginator.total_pages:
        invalid_page_message = "Invalid page number"
        return render_template('/student_templates/student_all.html', invalid_page_message = invalid_page_message)
    

#生徒削除画面
@main_bp.route("/student_delete/<int:student_id>", methods=['POST'])
@login_required
def delete_student(student_id):
    try:
        student = Students.get(Students.id == student_id)
        student.delete_instance()
        flash('Student deleted successfully.', 'success')
    except Students.DoesNotExist:
        flash('Student not found', 'error')
        
    return redirect(url_for('main.all_student'))


#生徒詳細画面
@main_bp.route("/home/student_all/student_detail_<int:student_id>", methods=['GET'])
@login_required
def detail_student(student_id):
    student = Students.get(Students.id == student_id)
    return render_template('/student_templates/student_detail.html', student=student)


#生徒別テスト結果一覧画面
@main_bp.route("/home/studen_all/student_detail_testresult/<int:student_id>", methods=['GET'])
@login_required
def student_all_testresult(student_id):
    student = Students.get(Students.id == student_id)
    first_name = student.first_name
    last_name = student.last_name
    
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    
    query = TestResults.select().where((TestResults.first_name == first_name) & (TestResults.last_name == last_name))
    total = query.count()
    testresults = query.paginate(page, per_page)

    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap5')

    return render_template('/student_templates/student_all_testresult.html', testresults=testresults, pagination=pagination, student=student)


#ハンドルケース1:表示する生徒がいない場合
@main_bp.route("/home/testresult_all/no_student_testresults", methods=['GET'])
@login_required
def handleone_student_all_testresult():
    testresults = TestResults.select()
    if not testresults:
        no_testresults_message = "No test results found."
        return render_template('/student_templates/student_all_testresult.html', no_testresults_message = no_testresults_message)


#生徒別学習記録一覧画面
@main_bp.route("/home/studen_all/student_detail_learningreport/<int:student_id>", methods=['GET'])
@login_required
def student_all_learningreport(student_id):
    student = Students.get(Students.id == student_id)
    first_name = student.first_name
    last_name = student.last_name
    
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    
    query = LearningReports.select().where((LearningReports.first_name == first_name) & (LearningReports.last_name == last_name))
    total = query.count()
    learningreports = query.paginate(page, per_page)

    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap5')

    return render_template('/student_templates/student_all_learningreport.html', learningreports=learningreports, pagination=pagination, student=student)


#ハンドルケース1:表示する生徒がいない場合
@main_bp.route("/home/learningreport_all/no_student_learningreports", methods=['GET'])
@login_required
def handleone_student_all_learningreport():
    learningreports = LearningReports.select()
    if not learningreports:
        no_learningreports_message = "No learning reports found."
        return render_template('/student_templates/student_all_learningreport.html', no_learningreports_message = no_learningreports_message)
    

#生徒情報編集
@main_bp.route("/home/student_all/student_detail_<int:student_id>/student_edit", methods=['GET','POST'])
@login_required
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
        return redirect(url_for('main.edit_student', student_id=student_id))
    return render_template('/student_templates/student_edit.html', student = student)


# 学習記録一覧(全体)
@main_bp.route("/home/learningreport_all", methods=['GET'])
@login_required
def all_learningreport():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    total = LearningReports.select().count()
    learningreports = LearningReports.select().paginate(page, per_page)

    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap5')

    return render_template('/learningreport_templates/learningreport_all.html', learningreports=learningreports, pagination=pagination)


#ハンドルケース1:表示する生徒がいない場合
@main_bp.route("/home/learningreport_all/no_learningreports", methods=['GET'])
@login_required
def handleone_all_learningreport():
    learningreports = LearningReports.select()
    pagination = Pagination(page=1, total=0, per_page=10, css_framework='bootstrap5')  # Add default pagination
    if not learningreports:
        no_learningreports_message = "No learning reports found."
        return render_template('/learningreport_templates/learningreport_all.html', no_learningreports_message = no_learningreports_message, pagination=pagination)
    

#ハンドルケース2:要求されたページがページ合計より多い場合
@main_bp.route("/home/learningreport_all/invalid_page", methods=['GET'])
@login_required
def handletwo_all_learningreport():
    learningreports = LearningReports.select()

    page_number = request.args.get('page', default = 1, type = int)
    per_page = 10

    paginator = Pagination(data=learningreports, per_page=per_page, css_framework='bootstrap5')

    if page_number > paginator.total_pages:
        invalid_page_message = "Invalid page number"
        return render_template('/learningreport_templates/learningreport_all.html', invalid_page_message = invalid_page_message, pagination=paginator)


#学習記録削除画面
@main_bp.route("/learningreport_delete/<int:learningreport_id>", methods=['POST'])
@login_required
def delete_learningreport(learningreport_id):
    try:
        learningreport = LearningReports.get(LearningReports.id == learningreport_id)
        learningreport.delete_instance()
        flash('Learningreport deleted successfully.', 'success')
    except LearningReports.DoesNotExist:
        flash('Learningreport not found', 'error')

    return redirect(url_for('main.all_learningreport'))


#学習記録詳細
@main_bp.route("/home/learningreport_all/learningreport_detail_<int:learningreport_id>", methods=['GET'])
@login_required
def detail_learningreport(learningreport_id):
    learningreport = LearningReports.get(LearningReports.id == learningreport_id)
    return render_template('/learningreport_templates/learningreport_detail.html', learningreport=learningreport, pagination=None)


#学習記録追加
@main_bp.route("/home/learningreport_add", methods=['GET','POST'])
@login_required
def add_learningreport():
    if request.method == 'POST':
        learn_date = request.form['learn_date']
        grade = request.form['grade']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        course = request.form['course']
        subject = request.form['subject']
        used_text = request.form['used_text']
        learningreport_comments = request.form['learningreport_comments']

        #データベースに保存
        LearningReports.create(
            learn_date=learn_date,
            grade=grade,
            first_name=first_name,
            last_name=last_name,
            course=course,
            subject=subject,
            used_text=used_text,
            learningreport_comments=learningreport_comments
        )
        db.close()
        return redirect(url_for('main.add_learningreport'))
    return render_template('/learningreport_templates/learningreport_add.html')


#学習記録編集
@main_bp.route("/home/learningreport_all/learningreport_detail_<int:learningreport_id>/learningreport_edit", methods=['GET','POST'])
@login_required
def edit_learningreport(learningreport_id):
    learningreport = LearningReports.get(LearningReports.id == learningreport_id)
    if request.method == 'POST':
        learningreport.learn_date = request.form['learn_date']
        learningreport.grade = request.form['grade']
        learningreport.first_name = request.form['first_name']
        learningreport.last_name = request.form['last_name']
        learningreport.course = request.form['course']
        learningreport.subject = request.form['subject']
        learningreport.used_text = request.form['used_text']
        learningreport.learningreport_comments = request.form['learningreport_comments']
        learningreport.save()
        return redirect(url_for('main.edit_learningreport', learningreport_id=learningreport_id))
    return render_template('/learningreport_templates/learningreport_edit.html',learningreport=learningreport)


#テスト結果一覧
@main_bp.route("/home/testresult_all", methods=['GET'])
@login_required
def all_testresult():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    total = TestResults.select().count()
    testresults = TestResults.select().paginate(page, per_page)

    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap5')

    return render_template('/testresult_templates/testresult_all.html', testresults=testresults, pagination=pagination)


#ハンドルケース1:表示する生徒がいない場合
@main_bp.route("/home/testresult_all/no_testresults", methods=['GET'])
@login_required
def handleone_all_testresult():
    testresults = TestResults.select()
    if not testresults:
        no_testresults_message = "No test results found."
        return render_template('/testresult_templates/testresult_all.html', no_testresults_message = no_testresults_message)
    

#ハンドルケース2:要求されたページがページ合計より多い場合
@main_bp.route("/home/student_all/testresult_all/invalid_page", methods=['GET'])
@login_required
def handletwo_all_testresult():
    testresults = TestResults.select()

    page_number = request.args.get('page', default = 1, type = int)
    per_page = 10

    paginator = Pagination(data=testresults, per_page=per_page)

    if page_number > paginator.total_pages:
        invalid_page_message = "Invalid page number"
        return render_template('/testresult_templates/testresult_all.html', invalid_page_message = invalid_page_message)
    

#テスト結果削除画面
@main_bp.route("/testresult_delete/<int:testresult_id>", methods=['POST'])
@login_required
def delete_testresult(testresult_id):
    try:
        testresult = TestResults.get(TestResults.id == testresult_id)
        testresult.delete_instance()
        flash('Testresult deleted successfully.', 'success')
    except TestResults.DoesNotExist:
        flash('testresult not found', 'error')

    return redirect(url_for('main.all_testresult'))
    

#テスト結果追加
@main_bp.route("/home/testresult_add", methods=['GET','POST'])
@login_required
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
        return redirect(url_for('main.add_testresult'))
    return render_template('/testresult_templates/testresult_add.html')

#テスト結果詳細
@main_bp.route("/home/testresult_all/testresult_detail_<int:testresult_id>", methods=['GET'])
@login_required
def detail_testresult(testresult_id):
    testresult = TestResults.get(TestResults.id == testresult_id)
    return render_template('/testresult_templates/testresult_detail.html', testresult=testresult)

#テスト結果編集
@main_bp.route("/home/testresult_all/testresult_detail_<int:testresult_id>/testresult_edit", methods=['GET','POST'])
@login_required
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
        testresult.user_total_rank = request.form['user_total_rank']
        testresult.all_total_rank = request.form['all_total_rank']
        testresult.user_rank_one= request.form['user_rank_one']
        testresult.user_rank_two= request.form['user_rank_two']
        testresult.user_rank_three= request.form['user_rank_three']
        testresult.user_rank_four= request.form['user_rank_four']
        testresult.user_rank_five= request.form['user_rank_five']
        testresult.all_rank_one= request.form['all_rank_one']
        testresult.all_rank_two= request.form['all_rank_two']
        testresult.all_rank_three= request.form['all_rank_three']
        testresult.all_rank_four= request.form['all_rank_four']
        testresult.all_rank_five= request.form['all_rank_five']
        return redirect(url_for('main.edit_testresult', testresult_id=testresult_id))
    return render_template("/testresult_templates/testresult_edit.html", testresult=testresult)


# テキスト追加操作画面
@main_bp.route("/home/text_add")
@login_required
def add_text():
    pdf_files = [file for file in os.listdir('files') if file.endswith('.pdf')]
    return render_template('text_templates/text_add.html', pdf_files=pdf_files)

# ファイルのアップロードを行う
@main_bp.route("/upload", methods=['POST'])
@login_required
def upload_text():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and file.filename.endswith('.pdf'):
        file_name = 'uploaded_' + file.filename
        file_path = os.path.join('files', file_name)
        file.save(file_path)

        # Read the file data as bytes
        with open(file_path, 'rb') as f:
            pdf_data = f.read()

        # Save file to TextData
        text_data = TextData.create(
            text_name=file.filename,
            text='Uploaded text file',
            pdf_data=pdf_data
        )
        text_data.save()

        return redirect(url_for('main.add_text'))
    else:
        flash('File is not a PDF')
        return redirect(request.url)

# ファイルの削除を行う
@main_bp.route('/delete/<int:text_id>', methods=['POST'])
@login_required
def delete_text(text_id):
    try:
        text_data = TextData.get(TextData.id == text_id)
        # Delete the file from the filesystem
        file_path = os.path.join('files', 'uploaded_' + text_data.text_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        # Delete from database
        text_data.delete_instance()
        flash('Text deleted successfully')
    except TextData.DoesNotExist:
        flash('Text not found')

    return redirect(url_for('main.all_textdata'))

# テキスト一覧
@main_bp.route("/home/text_all", methods=['GET'])
@login_required
def all_textdata():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    total = TextData.select().count()
    texts = TextData.select().paginate(page, per_page)

    no_texts_message = None
    if total == 0:
        no_texts_message = "No texts available"

    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap5')

    return render_template('/text_templates/text_all.html', texts=texts, pagination=pagination, no_texts_message=no_texts_message)

# テキスト詳細
@main_bp.route("/home/text_all/text_detail_<int:text_id>", methods=['GET'])
@login_required
def detail_text(text_id):
    try:
        textdata = TextData.get(TextData.id == text_id)
    except TextData.DoesNotExist:
        return redirect(url_for('main.all_textdata'))
    return render_template('/text_templates/text_detail.html', textdata=textdata)

# PDF表示
@main_bp.route("/home/text_all/text_detail_<int:text_id>/view_pdf", methods=['GET'])
@login_required
def view_pdf(text_id):
    try:
        textdata = TextData.get(TextData.id == text_id)
    except TextData.DoesNotExist:
        return redirect(url_for('main.all_textdata'))

    file_name = 'uploaded_' + textdata.text_name
    file_path = os.path.join('files', file_name)

    if not os.path.exists(file_path):
        flash('PDF file not found')
        return redirect(url_for('main.detail_text', text_id=text_id))

    return send_file(file_path, mimetype='application/pdf', as_attachment=False, download_name=file_name)

# テキスト編集(表示)
@main_bp.route("/home/text_all/text_detail_<int:text_id>/text_edit", methods=['GET'])
@login_required
def edit_text(text_id):
    try:
        text = TextData.get(TextData.id == text_id)
    except TextData.DoesNotExist:
        return redirect(url_for('main.all_textdata'))

    return render_template('/text_templates/text_edit.html', text=text)
