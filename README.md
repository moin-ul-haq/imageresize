# Image Resizer API

A Django REST API application for asynchronous image processing using Celery. Upload images and get them resized to 500x500 pixels in the background.

## Features

- 🚀 Asynchronous image processing with Celery
- 📸 Automatic image resizing to 500x500 pixels
- 🔄 Real-time task status tracking
- 📊 RESTful API endpoints
- 🐰 RabbitMQ message broker integration
- 💾 Redis result backend
- 🖼️ Support for various image formats (via Pillow)

## Tech Stack

- **Backend Framework**: Django 6.0.3
- **API**: Django REST Framework 3.16.1
- **Task Queue**: Celery 5.6.2
- **Message Broker**: RabbitMQ (AMQP)
- **Result Backend**: Redis
- **Image Processing**: Pillow 12.1.1
- **Database**: SQLite (default)

## Prerequisites

Before running this project, ensure you have the following installed:

- Python 3.8+
- RabbitMQ Server
- Redis Server
- pip (Python package manager)

### Installing RabbitMQ

**Windows:**
```powershell
# Download and install from https://www.rabbitmq.com/download.html
# Or use Chocolatey:
choco install rabbitmq
```

**Linux:**
```bash
sudo apt-get install rabbitmq-server
sudo systemctl start rabbitmq-server
```

**macOS:**
```bash
brew install rabbitmq
brew services start rabbitmq
```

### Installing Redis

**Windows:**
```powershell
# Download from https://github.com/microsoftarchive/redis/releases
# Or use Chocolatey:
choco install redis-64
```

**Linux:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

**macOS:**
```bash
brew install redis
brew services start redis
```

## Installation

1. **Clone the repository**
   ```bash
   cd d:\python\django\imageresizer
   ```

2. **Create and activate virtual environment**
   ```powershell
   # Windows PowerShell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   ```bash
   # Linux/macOS
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   cd imageresize
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create media directories**
   ```bash
   # Directories should already exist, but if not:
   mkdir media\uploads
   mkdir media\processed
   ```

## Running the Application

You need to run **three separate processes** in different terminals:

### Terminal 1: Django Development Server

```powershell
cd d:\python\django\imageresizer\imageresize
python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/`

### Terminal 2: Celery Worker

```powershell
cd d:\python\django\imageresizer\imageresize
celery -A imageresize worker -P threads -c 4 -l info
```

### Terminal 3: Redis Server (if not running as service)

```powershell
redis-server
```

### RabbitMQ Server

Ensure RabbitMQ is running:
```powershell
# Check status (Windows)
rabbitmq-service status

# Start if needed
rabbitmq-service start
```

## API Endpoints

### 1. Upload Image

**Endpoint:** `POST /api/upload/`

**Description:** Upload an image for asynchronous processing

**Request:**
- Content-Type: `multipart/form-data`
- Body: `image` (file)

**Response:**
```json
{
  "task id": "a3f5c8e2-1234-5678-90ab-cdef12345678"
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/upload/ \
  -F "image=@/path/to/your/image.jpg"
```

### 2. Check Task Status

**Endpoint:** `GET /api/status/<task_id>/`

**Description:** Check the current status of a processing task

**Response:**
```json
{
  "status": "PENDING"  // or "SUCCESS", "FAILURE", "RETRY", etc.
}
```

**cURL Example:**
```bash
curl http://127.0.0.1:8000/api/status/a3f5c8e2-1234-5678-90ab-cdef12345678/
```

### 3. Get Task Result

**Endpoint:** `GET /api/result/<task_id>/`

**Description:** Get the result of a completed task

**Response (Success):**
```json
{
  "status": "SUCCESS",
  "RESULT: ": "D:\\python\\django\\imageresizer\\imageresize\\media\\processed\\image.jpg"
}
```

**Response (Pending):**
```json
{
  "error": "Task Not completed Yet..."
}
```

**cURL Example:**
```bash
curl http://127.0.0.1:8000/api/result/a3f5c8e2-1234-5678-90ab-cdef12345678/
```

## Project Structure

```
imageresizer/
├── imageresize/              # Django project directory
│   ├── api/                  # API application
│   │   ├── models.py        # ImageTask model
│   │   ├── views.py         # API views
│   │   ├── serializers.py   # DRF serializers
│   │   ├── tasks.py         # Celery tasks
│   │   ├── services.py      # Image processing logic
│   │   ├── urls.py          # API routes
│   │   └── migrations/      # Database migrations
│   ├── imageresize/         # Django settings
│   │   ├── settings.py      # Project settings
│   │   ├── celery.py        # Celery configuration
│   │   ├── urls.py          # Main URL configuration
│   │   └── __init__.py      # Celery app initialization
│   ├── media/               # Media files
│   │   ├── uploads/         # Original uploaded images
│   │   └── processed/       # Resized images
│   ├── manage.py            # Django management script
│   └── db.sqlite3           # SQLite database
└── venv/                    # Virtual environment
```

## Configuration

### Celery Settings (imageresize/celery.py)

```python
app = Celery('imageresize', broker='amqp://localhost')
app.conf.result_backend = 'redis://localhost:6379/0'
```

### Image Processing

Images are automatically resized to **500x500 pixels**. To change this, modify `api/services.py`:

```python
def resize_image(image_path):
    img = Image.open(image_path)
    img = img.resize([500, 500])  # Change dimensions here
    # ... rest of the code
```

## Troubleshooting

### Celery worker not starting

**Error:** `Module 'imageresize' has no attribute 'celery'`

**Solution:** Make sure you're running the celery command from the correct directory:
```powershell
cd d:\python\django\imageresizer\imageresize
celery -A imageresize worker -P threads -c 4 -l info
```

### RabbitMQ connection refused

**Error:** `[Errno 10061] No connection could be made`

**Solution:** Ensure RabbitMQ is running:
```powershell
rabbitmq-service start
```

### Redis connection error

**Error:** `Error 10061 connecting to localhost:6379`

**Solution:** Start Redis server:
```powershell
redis-server
```

### Port already in use

**Error:** `Error: That port is already in use.`

**Solution:** Use a different port:
```bash
python manage.py runserver 8001
```

## Development

### Creating Superuser

```bash
python manage.py createsuperuser
```

### Running Tests

```bash
python manage.py test api
```

### Making Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## How to Use

Here's a complete workflow example:

### Step 1: Start all services

Open 3 terminal windows and run:

**Terminal 1 - Django Server:**
```powershell
cd d:\python\django\imageresizer\imageresize
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

**Terminal 2 - Celery Worker:**
```powershell
cd d:\python\django\imageresizer\imageresize
.\venv\Scripts\Activate.ps1
celery -A imageresize worker -P threads -c 4 -l info
```

**Terminal 3 - Verify services:**
```powershell
# Check RabbitMQ
rabbitmq-service status

# Check Redis (if not running as service)
redis-server
```

### Step 2: Upload an image

Use any HTTP client (Postman, cURL, Python requests, etc.):

**Using cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/upload/ \
  -F "image=@C:\path\to\your\photo.jpg"
```

**Using Python requests:**
```python
import requests

url = 'http://127.0.0.1:8000/api/upload/'
files = {'image': open('photo.jpg', 'rb')}
response = requests.post(url, files=files)
task_id = response.json()['task id']
print(f"Task ID: {task_id}")
```

**Using Postman:**
1. Create a new POST request to `http://127.0.0.1:8000/api/upload/`
2. Go to Body → form-data
3. Add key `image` with type `File`
4. Select your image file
5. Click Send

**Response:**
```json
{
  "task id": "a3f5c8e2-1234-5678-90ab-cdef12345678"
}
```

### Step 3: Check task status

Use the task ID from the previous response:

```bash
curl http://127.0.0.1:8000/api/status/a3f5c8e2-1234-5678-90ab-cdef12345678/
```

**Response:**
```json
{
  "status": "PENDING"  // Initially
}
```

Wait about 50 seconds (the task has a simulated delay), then check again:
```json
{
  "status": "SUCCESS"
}
```

### Step 4: Get the result

Once status is SUCCESS, get the processed image path:

```bash
curl http://127.0.0.1:8000/api/result/a3f5c8e2-1234-5678-90ab-cdef12345678/
```

**Response:**
```json
{
  "status": "SUCCESS",
  "RESULT: ": "D:\\python\\django\\imageresizer\\imageresize\\media\\processed\\photo.jpg"
}
```

### Step 5: Access the processed image

The resized image is saved in:
```
d:\python\django\imageresizer\imageresize\media\processed\
```

You can access it directly from the file system or configure Django to serve media files in production.

### Complete Python Example

```python
import requests
import time

# 1. Upload image
url = 'http://127.0.0.1:8000/api/upload/'
files = {'image': open('photo.jpg', 'rb')}
response = requests.post(url, files=files)
task_id = response.json()['task id']
print(f"Image uploaded. Task ID: {task_id}")

# 2. Poll for status
status_url = f'http://127.0.0.1:8000/api/status/{task_id}/'
while True:
    status_response = requests.get(status_url)
    status = status_response.json()['status']
    print(f"Status: {status}")
    
    if status == 'SUCCESS':
        break
    
    time.sleep(5)  # Wait 5 seconds before checking again

# 3. Get result
result_url = f'http://127.0.0.1:8000/api/result/{task_id}/'
result_response = requests.get(result_url)
result = result_response.json()
print(f"Processed image path: {result['RESULT: ']}")
```

## License

This project is open source and available for educational purposes.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Author

Created as a Django + Celery image processing demonstration project.
