import base64
from flask import Flask, Response, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///file_database.db'
db = SQLAlchemy(app)

# Create the database model for file uploads


class FileUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    file_data = db.Column(db.LargeBinary)
    image = db.Column(db.LargeBinary)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    price = db.Column(db.Integer)

    def __repr__(self):
        return f"FileUpload('{self.filename}')"


@app.route('/', methods=['GET'])
def upload_form():
    return render_template('upload.html')


@app.route('/uploadBooks', methods=['POST'])
def uploadBooks():
    if request.method == 'POST':
        # get form data
        form = request.form
        # save the fomr data to the database
        file_data = FileUpload(
            filename=request.files['file'].filename,
            file_data=request.files['file'].read(),
            image=request.files['image'].read(),
            title=form['title'],
            description=form['description'],
            price=form['price']
        )
        db.session.add(file_data)
        db.session.commit()
        return 'File saved to database successfully!'
    return 'Something went wrong'


@app.route('/show_data_all', methods=['GET'])
def show_data():
    files = FileUpload.query.all()
    for file in files:
        file.image_base64 = base64.b64encode(file.image).decode('utf-8')
    return render_template('show_data.html', files=files)


@app.route('/download/<int:file_id>', methods=['GET'])
def download_file(file_id):
    file_data = FileUpload.query.get_or_404(file_id)
    return Response(file_data.file_data, headers={
        'Content-Disposition': f'attachment; filename="{file_data.filename}"'
    })


if __name__ == '__main__':
    with app.app_context():
        # Create the database table
        db.create_all()
    app.run(debug=True)
