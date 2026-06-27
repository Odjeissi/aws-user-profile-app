# AWS User Profile App with Flask, Docker, RDS, S3, and GitLab CI/CD

## Project Overview

This is a hands-on DevOps project I built to practice deploying a real web application on AWS.

The app is built with Flask. Users can fill out a profile form and upload a profile picture. The profile information is saved in an AWS RDS MySQL database, and the uploaded pictures are stored in an S3 bucket.

This project focuses on the application side of DevOps, including Docker, testing, CI/CD, deployment, and troubleshooting.

---

## Infrastructure

The AWS infrastructure for this app was created in a separate Terraform project.

Infrastructure repository:

[aws-scalable-web-infrastructure](https://github.com/Odjeissi/aws-scalable-web-infrastructure)

That project provides the main AWS resources used to run this app, such as networking, EC2, load balancing, RDS, S3, IAM, Route53, and ACM.

---

## Application Architecture

The Flask app runs inside Docker containers on two EC2 instances. These instances sit behind an Application Load Balancer.

The app connects to:

* AWS RDS MySQL to store user profile data
* AWS S3 to store uploaded profile pictures

---

## Current App Design

This project includes:

* A Flask web app for profile submissions
* A MySQL database on AWS RDS
* An S3 bucket for uploaded profile pictures
* Docker to package and run the app
* Docker Hub to store the Docker image
* GitLab CI/CD to test, build, push, and deploy the app
* Two EC2 instances as deployment targets
* Environment variables for database and S3 settings
* Screenshots were captured for validation, troubleshooting, and deployment evidence.

---

## App Features

The app includes:

* A user profile form
* Fields for first name, last name, age, city, and country
* Profile picture upload
* File type validation for images
* Uploads to AWS S3
* Profile data saved in AWS RDS MySQL
* Admin page to view submitted profiles
* Health check route for testing

Main routes:

```text
/        Main profile form
/admin   Admin dashboard
/health  Health check endpoint
```

---

## AWS Services Used

This app uses:

* EC2
* Application Load Balancer
* RDS MySQL
* S3
* IAM Role / Instance Profile
* Security Groups

---

## Tools and Technologies

* Python
* Flask
* MySQL
* PyMySQL
* AWS RDS, S3
* Docker
* Docker Hub
* GitLab CI/CD
* Pytest
* Pylint
* Linux
* SSH

---

## Project Goals

The main goals of this project were to:

* Build a real application for an AWS infrastructure project
* Connect a web app to RDS MySQL
* Upload files from a web app to S3
* Use IAM roles for AWS access
* Run the app inside Docker
* Build and push Docker images with GitLab CI/CD
* Deploy the app to EC2 instances
* Use GitLab CI/CD variables for secrets
* Add basic testing with Pytest
* Add code checks with Pylint
* Document the project with screenshots
* Practice fixing real DevOps, Docker, AWS, and CI/CD issues

---

## Application Code

The main app file is:

```text
app.py
```

The Flask app handles:

* Showing the profile form
* Receiving form submissions
* Checking uploaded image files
* Uploading profile pictures to S3
* Saving user data to RDS MySQL
* Reading submitted profiles from the database
* Returning the app health status

---

## Database Design

The app stores profile information in a MySQL table named `users`.

Example table:

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    age INT,
    city VARCHAR(100),
    country VARCHAR(100),
    profile_picture_key VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

The `profile_picture_key` column stores the S3 file path for the uploaded profile picture.

---

## S3 Storage

Uploaded profile pictures are stored in S3 under this folder:

```text
profile-pictures/
```

Each uploaded file gets a unique name using:

* First and Last name
* UUID
* Original file extension

Example:

```text
profile-pictures/john-doe-uuid-value.jpg
```

Screenshots were added to show that the uploads worked during testing.

---

## Docker

The app is containerized with Docker.

Dockerfile location:

```text
docker/Dockerfile
```

The image uses Python 3.11 Alpine. It installs the needed packages, copies the app files, exposes port `5000`, and starts the Flask app.

Build command:

```bash
docker build -t aws-user-profile-app -f docker/Dockerfile .
```

Run command example:

```bash
docker run -d \
  --name aws-user-profile-app \
  -p 80:5000 \
  -e DB_HOST="your-db-host" \
  -e DB_USER="your-db-user" \
  -e DB_PASSWORD="your-db-password" \
  -e DB_NAME="your-db-name" \
  -e DB_PORT="3306" \
  -e S3_BUCKET="your-s3-bucket" \
  -e S3_REGION="your-aws-region" \
  aws-user-profile-app
```

---

## Environment Variables

The app uses environment variables for the database and S3 settings.

Required variables:

```text
DB_HOST
DB_USER
DB_PASSWORD
DB_NAME
DB_PORT
S3_BUCKET
S3_REGION
```

For local testing, these can go in a `.env` file.

For GitLab CI/CD and production, these should be saved as GitLab CI/CD variables.

Secrets should never be committed to the repository.

---

## Running the App Locally

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file with the needed values:

```text
DB_HOST=your-db-host
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_NAME=your-db-name
DB_PORT=3306
S3_BUCKET=your-s3-bucket
S3_REGION=your-aws-region
```

Run the app:

```bash
python app.py
```

Open the app in your browser:

```text
http://localhost:5000
```

Health check:

```text
http://localhost:5000/health
```

Admin dashboard:

```text
http://localhost:5000/admin
```

---

## Testing

This project includes basic tests with Pytest.

Test files:

```text
tests/test_routes.py
tests/test_uploads.py
```

The tests check that:

* The `/health` route works
* The home page loads
* Valid image file types are accepted
* Invalid file types are rejected

Run tests:

```bash
pytest -v
```

---

## GitLab CI/CD Pipeline

GitLab CI/CD is used to automate testing, building, and deployment.

Pipeline stages:

```text
test
build
deploy
```

Pipeline flow:

1. Code is pushed to the repository.
2. GitLab starts the pipeline.
4. The test stage runs Pytest.
5. The lint job runs Pylint.
6. The build stage builds the Docker image.
7. The image is pushed to Docker Hub.
8. The deploy stage connects to the EC2 instances using SSH.
9. Each EC2 instance pulls the latest image.
10. The old container is removed.
11. A new container starts with the needed environment variables.

---

## GitLab CI/CD Variables

Sensitive values are stored as GitLab CI/CD variables.

Example variables:

```text
DOCKER_USERNAME
DOCKER_PASSWORD
EC2_PRIVATE_KEY
EC2_USER
EC2_1
EC2_1
MY_DB_HOST
MY_DB_USER
MY_DB_PASSWORD
MY_DB_NAME
MY_DB_PORT
MY_S3_BUCKET
MY_S3_REGION
```

These variables are used to:

* Log in to Docker Hub
* Build and push the Docker image
* SSH into EC2 instances
* Pass database settings to the container
* Pass S3 settings to the container

---

## Deployment Evidence

The app was tested, containerized, pushed to Docker Hub, and deployed to two EC2 instances using GitLab CI/CD.

Screenshots were added to show:

* The web app form
* Successful profile submissions
* Error handling
* MySQL table setup
* RDS security group setup
* RDS database records
* S3 uploads
* S3 permissions
* EC2 IAM role
* Docker build steps
* Docker commands
* Docker Hub repository
* Deployment script
* Deployment to both EC2 instances
* GitLab pipeline runs
* GitLab test, and lint jobs
* Troubleshooting steps

Screenshots are stored in:

```text
docs/screenshots/
```

---

## Troubleshooting and Lessons Learned

During this project, I practiced fixing real DevOps issues, such as:

* Docker permission problems on EC2
* GitLab pipeline errors
* Environment variable issues
* SSH deployment from GitLab runners
* Docker image build and push problems
* Replacing old containers during deployment
* Connecting the app to RDS
* Giving the app access to S3
* Checking that files were uploaded to S3
* Checking that profile records were saved in the database

This helped me better understand how application code, cloud infrastructure, Docker, and CI/CD work together in a real deployment.

---

## Security Notes

This project uses a few basic security practices:

* Database credentials are stored in GitLab CI/CD variables
* AWS secrets are not committed to the repository
* The app reads settings from environment variables
* Profile pictures are stored in S3 instead of directly on EC2
* EC2 uses IAM permissions to access AWS services
* RDS security groups control database access
* The app includes a health check endpoint for deployment checks

---

## Skills Demonstrated

This project shows hands-on experience with:

* Python
* Flask
* MySQL
* AWS
* Docker
* GitLab CI/CD
* SSH deployment
* Linux troubleshooting
* Cloud deployment
* DevOps troubleshooting

---

## Author

Created by Oj Mendes
