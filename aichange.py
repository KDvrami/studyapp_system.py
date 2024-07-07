from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_paginate import Pagination, get_page_parameter
from peewee import *
from io import BytesIO
import pypdf

# データベースの設定
db = SqliteDatabase('studyapp_sora.db')

# データベースのテーブル設定
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
    subject_three = CharField(maxlength=255)
    subject_four = CharField(maxlength=255)
    subject_five = CharField(maxlength=255)
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
    all_rank三 = IntegerField()
    all_rank_four = IntegerField()
    all_rank_five = IntegerField()
    testresult_comments = CharField(maxlength=255)

    class Meta:
        database = db

class LearningReports(Model):
    learn_date = DateField()
    grade = CharField(maxlength=255)
    first_name = CharField(maxlength=255)
    last_name = CharField(maxlength=255)
    course = CharField(maxlength=255)
    subject = CharField(maxlength=255)
    text = TextField()
    learningreport_comments = CharField(maxlength=255)

    class Meta:
        database = db

class TextData(Model):
    text_name = CharField(maxlength=255)
    text = TextField()
    pdf_data = BlobField()

    class Meta:
        database = db

db.create_tables([Students, TestResults, LearningReports, TextData])

app = Flask(__name__)

# テキスト追加
@app.route("/home/text_add", methods=['GET', 'POST'])
def add_textdata():
    if request.method == 'POST':
        text_name = request.form['text_name']

        # アップロードされたpdfからテキストを抽出
        file = request.files['text']
        pdf_reader = pypdf.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()

        # データベースに保存
        TextData.create(
            text_name=text_name,
            text=text,
            pdf_data=file.read()
        )
        db.close()
        return redirect(url_for('all_textdata'))
    return render_template('/text_templates/text_add.html')

# テキスト一覧
@app.route("/home/text_all", methods=['GET'])
def all_textdata():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    total = TextData.select().count()
    texts = TextData.select().paginate(page, per_page)

    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap5')

    return render_template('/text_templates/text_all.html', texts=texts, pagination=pagination)

# テキスト詳細
@app.route("/home/text_all/text_detail_<int:text_id>", methods=['GET'])
def detail_text(text_id):
    try:
        textdata = TextData.get(TextData.id == text_id)
    except TextData.DoesNotExist:
        return redirect(url_for('all_textdata'))
    return render_template('/text_templates/text_detail.html', textdata=textdata)

# PDF表示
@app.route("/home/text_all/text_detail_<int:text_id>/view_pdf", methods=['GET'])
def view_pdf(text_id):
    try:
        textdata = TextData.get(TextData.id == text_id)
    except TextData.DoesNotExist:
        return redirect(url_for('all_textdata'))
    
    return send_file(BytesIO(textdata.pdf_data), attachment_filename=f"{textdata.text_name}.pdf", as_attachment=False)

# テキスト編集(表示)
@app.route("/home/text_all/text_detail_<int:text_id>/text_edit", methods=['GET'])
def edit_text(text_id):
    try:
        text = TextData.get(TextData.id == text_id)
    except TextData.DoesNotExist:
        return redirect(url_for('all_textdata'))

    return render_template('/text_templates/text_edit.html', text=text)

# テキスト編集(保存)
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

    # データベースを更新
    text.text_name = text_name
    text.text = extracted_text
    text.pdf_data = file.read()
    text.save()

    return redirect(url_for('all_textdata'))

if __name__ == '__main__':
    app.run(debug=True)
