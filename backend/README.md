# Attendance Tracker Backend (Flask + Firebase)

This is the backend for the **Attendance Tracker** system, built with **Flask** and **Firebase (Firestore)**.\
It provides **user authentication, attendance management, automatic planner generation, and attendance insights**.

## 🚀 Features

✔ **Google Authentication with Firebase Auth**\
✔ **Student Attendance Tracking** (Present, Absent, No Class, GT)\
✔ **Auto-Generated Attendance Planner**\
✔ **Attendance Insights & Deficiency Warnings**\
✔ **REST API for frontend integration**

## 📂 Project Structure

```
/backend
├── app.py              # Main Flask App
├── firebase.py         # Firebase Setup
├── config.py           # Configuration File
├── requirements.txt    # Dependencies
├── models/             # Firestore Database Models
│   ├── user.py
│   ├── attendance.py
│   ├── planner.py
├── routes/             # API Routes
│   ├── auth.py
│   ├── attendance.py
│   ├── planner.py
│   ├── reports.py
├── middlewares/
│   ├── auth_middleware.py# Token Authentication Middleware
├── README.md           # Documentation
```

## 🛠️ Setup Instructions

### 1️⃣ Install Dependencies

1. **This Project is made using uv** - If you have [uv](  https://docs.astral.sh/uv/) then simple run the following command 🔥 fast isn't it.

```bash
uv run app.py
``` 
2. **OhterWise requirements is given** 

```bash
pip install -r requirements.txt
```

### 2️⃣ Setup Firebase

1. **Create a Firebase Project** ([https://console.firebase.google.com/](https://console.firebase.google.com/))
2. **Enable Firestore & Authentication**
3. \*\*Download \*\***`serviceAccountKey.json`** and place it in `/backend/`
4. **Update ********************************************`firebase.py`******************************************** with Firestore initialization**

### 3️⃣ Run the Server

```bash
python app.py
```


## 🔥 Database Schema (Firestore)

Firestore is **NoSQL**, so data is structured as **collections & documents**.

### 1️⃣ Users Collection (`users/{uid}`)

Each user has a document with their **UID**.

#### Fields:
- `uid` (string) – Unique identifier for the user.
- `name` (string) – Full name.
- `email` (string) – User's email.
- `roll_number` (string) – Roll number.
- `branch` (string) – Department/Branch.
- `year` (string) – Graduation year.
- `semester` (string) – Current semester.
- `subjects` (array) – List of subjects.
- `attendance_period` (object) – Start and end date of the attendance period.

---

### 2️⃣ Attendance Collection (`attendance/{uid}/dates/{date}`)

Stores **daily attendance records** for each user.

#### Fields:
- `date` (string) – Date of attendance.
- `attendance` (object) – Key-value pairs of subjects and their attendance status (e.g., Present, Absent, No Class).

---

### 3️⃣ Attendance Summary (`attendance/{uid}/summary/attendance_report`)

Stores **calculated attendance insights**.

#### Fields:
- `subject_wise` (object) – Contains attendance stats for each subject.
  - `percentage` (float) – Attendance percentage.
  - `present` (integer) – Number of attended classes.
  - `total` (integer) – Total classes held.
  - `deficiency` (integer, optional) – Number of classes needed to reach 75%.
- `updated_at` (timestamp) – Last updated timestamp.

---

## 🚀 API Endpoints

### 1️⃣ Create or Update User

- **Endpoint:** `POST /auth/create-or-update-user`
- **Headers:**  
  - `Authorization: Bearer {token}`
- **Body:**
  ```json
  {
    "uid": "abc123",
    "name": "John Doe",
    "email": "your@gmail.com",
    "roll_number": "24",
    "branch": "CSE",
    "year": "2028",
    "semester": "2nd",
    "subjects": ["English", "Maths", "Hindi"],
    "attendance_period": {
      "start": "2024-01-01",
      "end": "2024-05-31"
    }
  }
  ```
- **Response:**
  ```json
  {
    "message": "User updated successfully",
    "uid": "uidisreturned"
  }
  ```

---

### 2️⃣ Mark Attendance

- **Endpoint:** `POST /attendance/mark`
- **Headers:**  
  - `Authorization: Bearer {token}`
- **Body:**
  ```json
  {
    "date": "2025-03-24",
    "attendance": {
      "Math": "Present",
      "Physics": "Absent",
      "CS": "No Class"
    }
  }
  ```
- **Response:**
  ```json
  {
    "data": {
      "CS": "No Class",
      "Math": "Present",
      "Physics": "Absent"
    },
    "message": "Attendance marked successfully"
  }
  ```

---

### 3️⃣ Get Attendance Summary

- **Endpoint:** `GET /attendance/summary`
- **Headers:**  
  - `Authorization: Bearer {token}`
- **Response:**
  ```json
  {
    "subject_wise": {
      "CS": {
        "deficiency": 2,
        "percentage": 0.0,
        "present": 0,
        "total": 3
      },
      "Math": {
        "percentage": 100.0,
        "present": 3,
        "total": 3
      },
      "Physics": {
        "deficiency": 1,
        "percentage": 66.67,
        "present": 2,
        "total": 3
      }
    },
    "updated_at": "Thu, 20 Mar 2025 06:22:14 GMT",
  }
  ```



<!-- ## 🔥 Database Schema (Firestore)

Firestore is **NoSQL**, so data is structured as **collections & documents**.

### 1️⃣ Users Collection (`users/`)

Each user has a document with their **UID**.

- Request **Url http://localhost:5000/auth/create-or-update-user**
- Method **POST**
- **Header should have 'Authorization: Bearer {token}**
- Body is given below
```json

{
  "uid": "abc123",
  "name": "John Doe",
  "email": "your@gmail.com",
  "roll_number":"24",
  "branch":"CSE",
  "year":"2028",
  "semester":"2nd",
  "subjects":["English","Maths","Hindi"],
  "attendance_period":{
    "start": "2024-01-01",
    "end": "2024-05-31"
  }

}
```
- Response is given below
```json
{
    "message": "User updated successfully",
    "uid": "uidisreturned"
}
```

### 2️⃣ Attendance Collection (`attendance/{uid}/dates/`)

Stores **daily attendance records** for each user.
- Request **Url http://localhost:5000/attendance/mark**
- Method **POST**
- **Header should have 'Authorization: Bearer {token}**
- Body is given below

```json
{
    "date": "2025-03-24",
    "attendance": {
        "Math": "Present",
        "Physics": "Absent",
        "CS": "No Class"
    }
}
```

- Response is given below 
```json
{
  "data": {
      "CS": "No Class",
      "Math": "Present",
      "Physics": "Absent"
  },
  "message": "Attendance marked successfully"
}
```

### 3️⃣ Attendance Summary (`attendance/{uid}/summary/attendance_report`)

Stores **calculated attendance insights**.

- Request **Url http://localhost:5000/attendance/summary**
- Method **GET**
- **Header should have 'Authorization: Bearer {token}**
- **There is no need for body**
- **response is given below**
```json
{
    "subject_wise": {
        "CS": {
            "deficiency": 2,
            "percentage": 0.0,
            "present": 0,
            "total": 3
        },
        "Math": {
            "percentage": 100.0,
            "present": 3,
            "total": 3
        },
        "Physics": {
            "deficiency": 1,
            "percentage": 66.67,
            "present": 2,
            "total": 3
        }
    },
    "updated_at": "Thu, 20 Mar 2025 06:22:14 GMT"
}
``` -->

<!-- ### 4️⃣ Planner Collection (`planner/{uid}/`)

Auto-generates **attendance planner** based on user data.

```json
{
  "uid": "abc123",
  "semester": 4,
  "schedule": {
    "Monday": ["Math", "Physics"],
    "Tuesday": ["CS", "Math"],
    "Wednesday": ["Physics", "CS"],
    "Thursday": ["Math"],
    "Friday": ["CS", "Physics"]
  },
  "holidays": ["2025-03-25", "2025-04-14"]
}
``` -->

## 🔌 API Endpoints

### 🟢 Authentication (`routes/auth.py`)

| Method | Endpoint      | Description                         |
| ------ | ------------- | ----------------------------------- |
| `POST` | `/auth/create-or-update-user` | Creates or modifies user                      |
| `GET`  | `/auth/user`  | Fetch user profile (requires token) |

### 🟢 Attendance (`routes/attendance.py`)

| Method | Endpoint              | Description                   |
| ------ | --------------------- | ----------------------------- |
| `POST` | `/attendance/mark`    | Mark attendance for a subject |
| `GET`  | `/attendance/summary` | Get attendance insights       |

📌 **Example Response (GET ********************************************`/attendance/summary`********************************************)**

```json
{
    "subject_wise": {
        "CS": {
            "deficiency": 2,
            "percentage": 0.0,
            "present": 0,
            "total": 3
        },
        "Math": {
            "percentage": 100.0,
            "present": 3,
            "total": 3
        },
        "Physics": {
            "deficiency": 1,
            "percentage": 66.67,
            "present": 2,
            "total": 3
        }
    },
    "updated_at": "Thu, 20 Mar 2025 06:22:14 GMT"
}
```

### 🟢 Planner (`routes/planner.py`)

| Method | Endpoint            | Description                     |
| ------ | ------------------- | ------------------------------- |
| `GET`  | `/planner/generate` | Generate a subject-wise planner |

📌 **Example Response**

```json
{
  "Monday": ["Math", "Physics"],
  "Tuesday": ["CS", "Math"],
  "Wednesday": ["Physics", "CS"],
  "Thursday": ["Math"],
  "Friday": ["CS", "Physics"]
}
```

## 🛡️ Token Authentication (`middlewares.py`)

- **All API requests require a valid Firebase Auth token.**
- **Add ********************************************`@token_required`******************************************** decorator to secure routes.**

📌 **Example Usage**

```python
@attendance_bp.route("/summary", methods=["GET"])
@token_required
def get_attendance_summary():
    uid = request.user.get("uid")  
    response = Attendance.get_attendance_summary(uid)
    return jsonify(response), 200
```

## 🎯 Next Steps

✅ **Finish frontend integration with React**\
✅ **Implement attendance trend reports**\


## 📌 Contributing

1. Fork the repo
2. Create a new branch (`feature-xyz`)
3. Commit changes
4. Open a PR

