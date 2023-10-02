# Documentation of the Video upload API project

This documentation provides detailed information on the Video upload API built with Django and other dependencies. It covers the standard format for requests and responses, sample API usage, known limitations, and setup/deployment instructions.

## Table of Contents
- [Prereqisites](#prerequisites)
- [Setup and Deployment](#setup-and-deployment)
- [Standard Request and Response Format](#standard-request-and-response-format)
- [Sample API Usage](#sample-api-usage)
- [Known Limitations](#known-limitations)

---

## Prerequisites
Before you begin, ensure you have the following prerequisites installed in your system:
- Python (3.10)
- pip (Python package manager)
- pipenv
- git bash terminal (For windows)
- mysql database

## Setup and Deployment
To set up and deploy this API locally or on a server, follow these steps:

1. Clone the repository:
git clone https://github.com/Chiemelie10/hng_task_five_video

2. Enter the cloned directory:
cd hng_task_five_video

3. Create a virtual environment:
pipenv shell

4. Install the dependencies:
pipenv install

5. Add localhost to allowed hosts:
cd hng_task_five
open settings.py file with your editor
scroll down till you see 'ALLOWED_HOSTS'
add 'localhost' to the list
set DEBUG to True
save and exit

6. Set up mysql database
Configure your mysql database to match the one in settings.py.
Grant CREAT on all tables and databases to the USER
Grant ALL PRIVILEGES on all tables in the chosen database to the USER 

7. Run makemigrations

8. Run migrate

9. Run the API locally:
python manage.py runserver

The API will be accessible at http://localhost:8000.

For production deployment, consider using a production-ready web server (e.g., Gunicorn) and configuring a proper database server.

## Standard Request and Response Format

### POST /api/chunked_upload
**Request to post a video to the database:**
- accecpts multipart/form-data

- request body:
- {"file": <file>}

- request header:
- Content-Range: <offset>-<file_size - 1>/<total_size>

NB: Content-Range can be set for the first request but it is only required if subsequent requests will be made to this endpoint using upload_id that will be sent as response. The value offset for the first request is 0 (zero). file_size is the size of the particular file that will be posted. total_size is file_size if the file was not broken into chunks. If file was broken into chunks, total_size is the file size before the video was broken into chunks. 

**Response (200 OK):**
{
    "upload_id": 5230ec1f59d1485d9d7974b853802e31,
    "offset": 10000,
    "expires": "2023-10-01T12:50:25.186Z"
}

Repeatedly POST subsequent chunks using the 'upload_id' to identify the upload to the url.
Example:
{
    "upload_id": 5230ec1f59d1485d9d7974b853802e31,
    "file": <file>
}

Also set Content-Range in the header before making this request:
Example:
Content-Range: <offset>-<file_size - 1>/<total_size>

NB: Repeat this process until all chunks has been uploaded.

### POST /api/completed_upload
**Request to inform the server that the upload is complete:**

- Request body:
{
    "upload_id": 5230ec1f59d1485d9d7974b853802e31,
}

- No header required.

**Response (200 OK):**
{
    "upload_id": 5230ec1f59d1485d9d7974b853802e31,
    "upload_status": 2,
    "created_on": "2023-10-02T04:11:32.940Z",
    "completed_on": "2023-10-02T04:12:35.030Z",
    "filename": "mixkit-group-of-colleagues-brainstorming-in-a-meeting-48713-medium.mp4",
    "url": "https://hngvideoapi.pythonanywhere.com/media/videos/55035b852f92448e9f99000c7f5c3469.mp4"
}

NB: for upload_status, the value of 2 shows the upload is successful. The video can be watched by clicking on the url returned.

## Sample API Usage

Upload a video (POST /api)
Request:
POST http://localhost:8000/api/chunked_upload

- Request body:
{"file": <file>}

- Request header:
- Content-Range: <offset>-<file_size - 1>/<total_size>

Response (200 OK)
{
    "upload_id": 5230ec1f59d1485d9d7974b853802e31,
    "offset": 10000,
    "expires": "2023-10-01T12:50:25.186Z"
}

Tell server upload is complete (POST /api)
Request:
POST http://localhost:8000/api/completed_upload

- Request body:
{
    "upload_id": 5230ec1f59d1485d9d7974b853802e31,
}

- No header required.

Response (200 OK)
{
    "upload_id": 5230ec1f59d1485d9d7974b853802e31,
    "upload_status": 2,
    "created_on": "2023-10-02T04:11:32.940Z",
    "completed_on": "2023-10-02T04:12:35.030Z",
    "filename": "mixkit-group-of-colleagues-brainstorming-in-a-meeting-48713-medium.mp4",
    "url": "https://hngvideoapi.pythonanywhere.com/media/videos/55035b852f92448e9f99000c7f5c3469.mp4"
}

## Known Limitations
- This API does not include authentication or authorization mechanisms. It assumes open access.
- Error handling for invalid requests is minimal in this sample.
