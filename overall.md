# 📘 EMS / LMS - Django Based Education Management System

Welcome to the **EMS / LMS Project** – a modular, extensible Django-based web application designed for managing academic institutions with powerful role-based access control.

This project is architected around key modules that handle every critical academic activity: from attendance tracking and result publishing to assignments, learning materials, and dynamic timetable scheduling.

---

## 🧱 Layer 0: Global Layout & Navigation

### 🎨 Base Templates & Layout

* **`templates/base.html`**: Main foundational layout file.

  * Includes Navbar, Footer, Sidebar (if needed).
  * Contains `{% block %}` tags for injecting app-specific content.
* **Dashboard Templates:**

  * `accounts/dashboard.html`: Loads after login; varies based on user role.
  * Shows quick links to attendance, materials, timetable, etc.

### 🌐 Static Resources

* `static/css/base.css`, `style.css` – Global styling rules.
* `static/js/script.js` – Handles global UI interactions.
* Favicon and theme icons

---

## 🧩 Layer 1: Functional App Modules

Each Django app encapsulates its own:

* `models.py` for database structure
* `views.py` for logic
* `forms.py` for user input
* `templates/<app>/` for UI
* `urls.py` for routing

### 🔐 `accounts/`

User authentication and role-based access.

* **Roles**: Admin, Teacher, Student
* **CustomUser Model**:

  * Extended fields: `role`, `roll_number`, `profile_picture`, `microsoft_id`
* **Features**:

  * Registration & login
  * CSV import/export of users
  * Profile view/edit
  * Role-based redirect after login
  * Email verification flag
* **Templates**:

  * `add_user.html`, `login.html`, `signup.html`, `dashboard.html`, `profile.html`, `settings.html`

---

### 📅 `attendance/`

Record and view student attendance.

* **Views by Role**:

  * Teacher: Mark attendance
  * Student: View attendance
  * Admin: View all records, download reports
* **Models**: AttendanceRecord, Subject (imported/shared)
* **Templates**:

  * `mark_attendance.html`, `view_attendance_teacher.html`, `attendance_report.html`
* **Extras**:

  * Date picker for filtering
  * CSV Export for reports

---

### 📝 `assignments/`

Manage assignment uploads and submissions.

* **Teacher**:

  * Upload assignment (deadline, description, file)
  * View student submissions
  * Grade and give feedback
* **Student**:

  * Upload PDF submissions
  * Track deadline, status
* **Models**:

  * Assignment, Submission, Grade
* **Templates**:

  * `upload_assignments.html`, `view_assignments.html`, `grade_submission.html`

---

### 📊 `results/`

Publish and manage results securely.

* **Teacher**:

  * Add/edit marks
* **Student**:

  * View marks and grades
* **Admin**:

  * Export result sheets, view aggregate data
* **Models**:

  * ResultEntry, Subject (shared)
* **Templates**:

  * `edit_results.html`, `publish_results.html`, `report_results.html`

---

### 🧾 `materials/`

Upload and access lecture notes and study materials.

* **Teacher**:

  * Upload notes (PDF, DOC, PPT)
  * Organize by subject, week, topic
* **Student**:

  * Download/access assigned materials
* **Models**:

  * Material, Subject (shared)
* **Templates**:

  * `upload_material.html`, `view_materials.html`

---

### 📆 `timetable/`

Design and view class schedules.

* **Admin**:

  * Add/edit weekly timetable
  * Assign time slots to rooms, teachers
* **Student & Teacher**:

  * View schedules dynamically
* **Models**:

  * TimeSlot, Room, Subject, Teacher
* **Templates**:

  * `create_timetable.html`, `view_timetable.html`
* **Static**:

  * CSS: `timetable_base.css` for grid layout

---

## ⚙️ Layer 2: Shared Core Models (`core/`)

Central app for:

* `Teacher`
* `Student`
* `Subject`
* `Department`
* `Room`
* `TimeSlot`

These models are imported and extended by all functional apps.

* Relationships:

  * `Subject` links to `Teacher`, `Department`
  * `TimeSlot` defines period scheduling for `timetable`

Admin customizations and CSV imports handled here.

---

## 🔐 Layer 3: Role & Permissions Engine

Role-based control is deeply integrated:

* **`CustomUser` Model:** Defines role on login
* **Dashboard Rendering:**

  ```django
  {% if user.role == 'Admin' %} ... {% elif user.role == 'Teacher' %} ... {% endif %}
  ```
* **URL Access:** Views are protected with decorators like `@login_required`, `@user_passes_test`, or `permission_required()`

---

## 🗂 Layer 4: Media Management

* `media/` directory stores:

  * `assignments/`
  * `submissions/`
  * `profile_pics/`
* Uploads are validated and restricted by type and size
* Managed in `forms.py` of each app with `FileField`

---

## 🧪 Layer 5: Developer Tools

* `show-all-urls/`: Debug view to print all registered URL patterns
* `trial.html`: Testing page for new UI components
* `backup.json`: Fixtures for test data loading
* `admin.py`: All models are admin-registered with `list_display` customization

---

## 🌐 URL Routing (Main `urls.py`)

```python
urlpatterns = [
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('attendance/', include('attendance.urls')),
    path('assignments/', include('assignments.urls')),
    path('results/', include('results.urls')),
    path('materials/', include('materials.urls')),
    path('timetable/', include('timetable.urls')),
    path('admin/', admin.site.urls),
]
```

---

## 📜 Future Improvements

* 🔔 Notification system for deadlines, marks
* 📢 Announcement module
* 📊 Analytics for performance insights
* 🔒 Two-factor authentication (2FA)
* 🌍 Multi-language support

---

## 🧑‍💻 Dev & Maintenance Notes

* Python: 3.11+
* Django: 5.2.x
* Use `python manage.py runserver` to launch locally
* Use `python manage.py createsuperuser` to access admin dashboard

---

## 📂 Suggested Folder Structure

```
ems_project/
├── accounts/
├── attendance/
├── assignments/
├── results/
├── materials/
├── timetable/
├── core/
├── templates/
├── static/
├── media/
├── db.sqlite3
├── manage.py
└── README.md
```

---

> Made by Siddharth Acharya and Alish

---

