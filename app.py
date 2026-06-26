"""Flask application for file uploads and S3 storage."""

import os
import uuid
import boto3
import pymysql
from dotenv import load_dotenv
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

if os.path.exists(".env"):
    load_dotenv()

app = Flask(__name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = int(os.getenv("DB_PORT", "3306"))

S3_BUCKET = os.getenv("S3_BUCKET")
S3_REGION = os.getenv("S3_REGION")


def get_s3_client():
    """Create and return an S3 client."""
    return boto3.client("s3", region_name=S3_REGION)


def get_db_connection():
    """Create and return a database connection."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        cursorclass=pymysql.cursors.DictCursor,
    )


def allowed_file(filename):
    """Check whether a filename has an allowed image extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_profile_picture_to_s3(file, first_name, last_name):
    """Upload a profile picture to S3 and return the S3 object key."""
    original_filename = secure_filename(file.filename)

    if not original_filename:
        return None

    if not allowed_file(original_filename):
        raise ValueError("Only png, jpg, jpeg, and gif files are allowed.")

    file_extension = original_filename.rsplit(".", 1)[1].lower()
    unique_id = str(uuid.uuid4())

    clean_first_name = secure_filename(first_name.lower())
    clean_last_name = secure_filename(last_name.lower())

    s3_key = (
        f"profile-pictures/"
        f"{clean_first_name}-{clean_last_name}-{unique_id}.{file_extension}"
    )

    get_s3_client().upload_fileobj(
        file,
        S3_BUCKET,
        s3_key,
        ExtraArgs={"ContentType": file.content_type},
    )

    return s3_key


def generate_presigned_url(s3_key):
    """Generate a temporary presigned URL for an S3 object."""
    if not s3_key:
        return None

    return get_s3_client().generate_presigned_url(
        "get_object",
        Params={"Bucket": S3_BUCKET, "Key": s3_key},
        ExpiresIn=600,
    )


@app.route("/health")
def health():
    """Return application health status."""
    return {"status": "healthy"}, 200


@app.route("/", methods=["GET", "POST"])
def index():
    """Render the main form and handle user profile submissions."""
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        age = request.form.get("age")
        city = request.form.get("city")
        country = request.form.get("country")
        profile_picture = request.files.get("profile_picture")

        profile_picture_key = None

        try:
            if profile_picture and profile_picture.filename:
                profile_picture_key = upload_profile_picture_to_s3(
                    profile_picture,
                    first_name,
                    last_name,
                )

            connection = get_db_connection()

            try:
                with connection.cursor() as cursor:
                    sql = """
                        INSERT INTO users
                        (first_name, last_name, age, city, country, profile_picture_key)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(
                        sql,
                        (
                            first_name,
                            last_name,
                            age,
                            city,
                            country,
                            profile_picture_key,
                        ),
                    )

                connection.commit()

            finally:
                connection.close()

            return render_template(
                "index.html",
                success=True,
                error=None,
                first_name=first_name,
                last_name=last_name,
                age=age,
                city=city,
                country=country,
                profile_picture_name=profile_picture.filename
                if profile_picture
                else None,
            )

        except (ValueError, pymysql.MySQLError, boto3.exceptions.Boto3Error) as error:
            return render_template(
                "index.html",
                success=False,
                error=str(error),
            )

    return render_template("index.html", success=False, error=None)


@app.route("/admin")
def admin():
    """Render the admin page with all submitted users."""
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
            users = cursor.fetchall()

    finally:
        connection.close()

    for user in users:
        user["profile_picture_url"] = generate_presigned_url(
            user.get("profile_picture_key")
        )

    return render_template("admin.html", users=users)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
