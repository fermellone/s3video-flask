from flask import Flask, render_template, request, redirect
import boto3
from werkzeug.utils import secure_filename

app = Flask(__name__)


app.config['S3_BUCKET'] = "nombre del bucket"
app.config['S3_KEY'] = "access key"
app.config['S3_SECRET'] = "aparece como asteriscos al crear una nueva access key"
app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format(app.config['S3_BUCKET'])


s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config['S3_KEY'],
   aws_secret_access_key=app.config['S3_SECRET']
)

def upload_file_to_s3(file, bucket_name, acl="public-read"):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type    #Set appropriate content type as per the file
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e
    return "{}{}".format(app.config["S3_LOCATION"], file.filename)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload-file', methods=['POST'])
def upload_file():
    if "video" not in request.files:
        return "No video key in request.files"

    file = request.files["video"]

    if file.filename == "":
        return "Please select a file"

    if file:
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, app.config['S3_BUCKET'])
        return str(output)
    else:
        return redirect("/")