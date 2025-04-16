# File Data Processing Pipeline

This project contains a file processing pipeline using **Docker**, **RabbitMQ**, and **PostgreSQL**. It includes three main services:

- `publisher`: Watches a directory for new files (`.txt`, `.csv`, `.xlsx`) and pushes parsed data to a RabbitMQ queue.
- `consumer`: Consumes messages from RabbitMQ and saves the parsed data into a PostgreSQL table.
- `api_service`: Provides REST APIs to retrieve `file_data` entries with pagination and filtering by name.

---

## ✅ Prerequisites

Make sure the following are installed:

- Docker
- Docker Compose
- PostgreSQL (configured with a database named `test`)
- RabbitMQ

---

## 🛠 Environment Variables

Create a `.env` file in the project root with the following content:

```env
# RabbitMQ Configuration
RABBITMQ_HOST="host.docker.internal"
RABBITMQ_USER="your_rabbitmq_username"
RABBITMQ_PASSWORD="your_rabbitmq_password"

# PostgreSQL Configuration
DB_HOST="host.docker.internal"
DB_USER="your_db_username"
DB_PASSWORD="your_db_password"
```

> ℹ️ `host.docker.internal` is used to communicate with services running on the host from inside a Docker container. You can change this if everything is running within the same Docker network.

---

## 🚀 How to Run the Project

1. **Clone the repository**  
   ```bash
   git clone https://github.com/priyanknair/file-data-pipeline.git
   cd file-data-pipeline
   ```

2. **Set up `.env` file**  
   Follow the instructions above to create your `.env`.

3. **Start all services using Docker Compose**  
   ```bash
   docker-compose up -d 
   ```

   This command starts:
   - `publisher` service
   - `consumer` service
   - `api_service` (REST API)

4. **Add files for processing**  
   Place your `.txt`, `.csv`, or `.xlsx` files into the `publisher/files/` directory.

---

## 📦 Sample File Format

Supported file formats: `.csv`, `.txt`, `.xlsx`  
Example content (header and values):

```
name
User1
User2
```

---

## 📡 API Service

API Base URL: `http://localhost:5000`

### GET `/file-data`

Query Parameters:

- `pageno`: Page number (default `1`)
- `pagesize`: Number of items per page (default `10`)
- `name`: (optional) Search by name

#### 📘 Sample Response

```json
{
  "count": 3,
  "page": 1,
  "per_page": 10,
  "results": [
    {
      "created_date": "2025-04-16 15:30:31",
      "id": 6,
      "name": "User1"
    },
    {
      "created_date": "2025-04-16 15:19:29",
      "id": 5,
      "name": "User2"
    },
    {
      "created_date": "2025-04-16 15:19:29",
      "id": 4,
      "name": "User3"
    }
  ]
}
```

---

## 🗃 Project Structure

```
.
├── publisher/
│   ├── file_watcher.py
│   ├── files
│   │   └── ...
│   └── ...
├── consumer/
│   ├── consumer.py
│   └── ...
├── api_service/
│   ├── app.py
│   ├── models.py
│   ├── schemas.py
│   ├──utils.py    
│   └── ...
├── docker-compose.yml
├── .env
└── README.md
```

---

## 🧼 Stopping and Cleaning Up

To stop all services:
```bash
docker-compose down
```

---
