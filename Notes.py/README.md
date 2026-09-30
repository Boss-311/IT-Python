# Notes REST API (Python / Flask)

A clean and lightweight RESTful API built with Python and Flask for managing notes with local JSON file persistence (`notes.json`). Built to demonstrate standard HTTP CRUD operations without requiring external database dependencies.

## Features

- **Full CRUD Support**: Standard HTTP endpoints (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`).
- **File Persistence**: Native Python `json` and `os` modules read/write directly to `notes.json`.
- **Strict Distinction**: Standard implementation for full object replacement (`PUT`) versus partial field updates (`PATCH`).
- **Standardized Responses**: Clear JSON responses accompanied by standard HTTP status codes (`200`, `201`, `400`, `404`).

---

## Project Structure

```text
notes-api/
├── notes.py          # Main Flask application and API route definitions
├── notes.json        # Local JSON file storing note objects
├── requirements.txt  # Python dependency specification
├── .gitignore        # Excludes virtual environments and cache files
└── README.md         # Project documentation
```

---

## Getting Started

### Prerequisites

- [Python 3.x](https://www.python.org/) installed on your system.

### Installation

1. Clone or download this project repository.
2. Open your terminal inside the project folder and install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Execute the main script:
```bash
python notes.py
```
The Flask development server will start at `http://127.0.0.1:3580`.

---

## API Reference

| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/notes` | Retrieve all notes | `200 OK` |
| `GET` | `/notes/:id` | Retrieve a single note by ID | `200 OK` / `404 Not Found` |
| `POST` | `/notes` | Create a new note | `201 Created` / `400 Bad Request` |
| `PUT` | `/notes/:id` | Fully replace an existing note | `200 OK` / `400 Bad Request` / `404 Not Found` |
| `PATCH` | `/notes/:id` | Partially update an existing note | `200 OK` / `404 Not Found` |
| `DELETE` | `/notes/:id` | Delete a note by ID | `200 OK` / `404 Not Found` |

---

## Request & Response Examples

### 1. Get All Notes
- **Endpoint**: `GET http://127.0.0.1:3580/notes`
- **Response** (`200 OK`):
  ```json
  [
    {
      "id": 1,
      "title": "Study Flask",
      "content": "Learn RESTful principles in Python"
    }
  ]
  ```

### 2. Create Note
- **Endpoint**: `POST http://127.0.0.1:3580/notes`
- **Request Body**:
  ```json
  {
    "title": "Study Flask",
    "content": "Learn RESTful principles in Python"
  }
  ```
- **Response** (`201 Created`):
  ```json
  {
    "message": "Note created successfully",
    "note": {
      "id": 1,
      "title": "Study Flask",
      "content": "Learn RESTful principles in Python"
    }
  }
  ```

### 3. Replace Note (Full Update)
- **Endpoint**: `PUT http://127.0.0.1:3580/notes/1`
- **Request Body**:
  ```json
  {
    "title": "Updated Title",
    "content": "Completely new content replacing old note"
  }
  ```
- **Response** (`200 OK`):
  ```json
  {
    "message": "Note replaced successfully",
    "note": {
      "id": 1,
      "title": "Updated Title",
      "content": "Completely new content replacing old note"
    }
  }
  ```

### 4. Partial Update Note
- **Endpoint**: `PATCH http://127.0.0.1:3580/notes/1`
- **Request Body**:
  ```json
  {
    "title": "Only Title Updated"
  }
  ```
- **Response** (`200 OK`):
  ```json
  {
    "message": "Note updated successfully",
    "note": {
      "id": 1,
      "title": "Only Title Updated",
      "content": "Completely new content replacing old note"
    }
  }
  ```

### 5. Delete Note
- **Endpoint**: `DELETE http://127.0.0.1:3580/notes/1`
- **Response** (`200 OK`):
  ```json
  {
    "message": "Note deleted successfully"
  }
  ```

---

## Testing

You can test these endpoints using VS Code **Thunder Client**, **Postman**, or via **cURL** in your terminal:

```bash
# Get all notes
curl [http://127.0.0.1:3580/notes](http://127.0.0.1:3580/notes)

# Create a new note
curl -X POST [http://127.0.0.1:3580/notes](http://127.0.0.1:3580/notes) \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Terminal Note\", \"content\":\"Created via cURL\"}"
```