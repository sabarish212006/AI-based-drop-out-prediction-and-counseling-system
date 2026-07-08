"""
Comprehensive Project Audit Script
Tests every page, API, CRUD operation, and database interaction.
Uses only stdlib (urllib) to avoid dependency issues.
"""
import sys, os, json, urllib.request, urllib.parse
sys.path.insert(0, os.path.dirname(__file__))

BASE = "http://127.0.0.1:5000"
passed = 0
failed = 0
errors = []

class TestSession:
    def __init__(self):
        self.cookies = {}
    
    def request(self, method, path, data=None):
        full_url = f"{BASE}{path}"
        if data:
            data_bytes = urllib.parse.urlencode(data).encode()
        else:
            data_bytes = None
        
        req = urllib.request.Request(full_url, data=data_bytes, method=method)
        req.add_header("Cookie", "; ".join(f"{k}={v}" for k, v in self.cookies.items()))
        
        try:
            resp = urllib.request.urlopen(req, timeout=10)
            # Save cookies
            for header in resp.headers.get_all("Set-Cookie") or []:
                parts = header.split(";")[0]
                if "=" in parts:
                    k, v = parts.split("=", 1)
                    self.cookies[k] = v
            return resp.status, resp.read().decode("utf-8", errors="ignore")
        except urllib.error.HTTPError as e:
            # Save cookies from error responses too
            for header in e.headers.get_all("Set-Cookie") if hasattr(e.headers, 'get_all') else []:
                parts = header.split(";")[0]
                if "=" in parts:
                    k, v = parts.split("=", 1)
                    self.cookies[k] = v
            return e.code, e.read().decode("utf-8", errors="ignore")
        except urllib.error.URLError as e:
            return 0, str(e)

    def get(self, path):
        return self.request("GET", path)
    
    def post(self, path, data):
        return self.request("POST", path, data)

def test(name, method="GET", url="/", data=None, expected_status=200, check_text=None, session=None):
    global passed, failed
    s = session or global_session
    try:
        if method == "GET":
            status, text = s.get(url)
        else:
            status, text = s.post(url, data or {})
        
        status_ok = status == expected_status
        text_ok = True
        if check_text and check_text not in text:
            text_ok = False
        
        if status_ok and text_ok:
            passed += 1
            print(f"  ✅ {name}")
        else:
            failed += 1
            msg = f"❌ {name}: expected status={expected_status}, got={status}"
            if not text_ok:
                msg += f", expected text='{check_text}' not found in response"
            print(msg)
            errors.append(msg)
    except Exception as e:
        failed += 1
        msg = f"❌ {name}: Exception - {e}"
        print(msg)
        errors.append(msg)

def login(session, email, password):
    return session.post("/login", {"email": email, "password": password})

global_session = TestSession()

print("=" * 60)
print("COMPREHENSIVE PROJECT AUDIT")
print("=" * 60)
print(f"Target: {BASE}")
print(f"Time: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Test 1: PUBLIC ROUTES
print("\n--- PUBLIC / AUTH ROUTES ---")
test("Login page loads", "GET", "/login", expected_status=200, check_text="Login")
test("Register page loads", "GET", "/register", expected_status=200, check_text="Register")
test("Root redirects to login", "GET", "/", expected_status=302)

# Test 2: LOGIN AS STUDENT
print("\n--- STUDENT LOGIN ---")
s = TestSession()
status, _ = login(s, "student01@college.edu", "Student@123")
if status == 302:
    passed += 1
    print("  ✅ Student01 login succeeds (redirect)")
else:
    failed += 1
    print(f"  ❌ Student01 login: got {status}")

# Test 3: STUDENT PAGES
print("\n--- STUDENT PAGES ---")
status, text = s.get("/student/dashboard")
if status == 200:
    passed += 1
    checks = ["Student Dashboard", "Latest CGPA", "AI Prediction"]
    for c in checks:
        if c in text:
            passed += 1
            print(f"  ✅ Dashboard contains '{c}'")
        else:
            failed += 1
            print(f"  ❌ Dashboard missing '{c}'")
else:
    print(f"  ❌ Student dashboard returned {status}")
    failed += 1

status, text = s.get("/student/summary")
if status == 200:
    passed += 1
    checks = ["Academic Summary", "AI Prediction"]
    for c in checks:
        if c.lower() in text.lower():
            passed += 1
            print(f"  ✅ Summary contains '{c}'")
        else:
            failed += 1
            print(f"  ❌ Summary missing '{c}'")
else:
    print(f"  ❌ Summary page returned {status}")
    failed += 1

test("Student profile loads", "GET", "/student/profile", expected_status=200, check_text="Profile", session=s)
test("Academic history loads", "GET", "/student/academic/history", expected_status=200, check_text="Academic History", session=s)
test("Add academic form loads", "GET", "/student/academic/add", expected_status=200, check_text="CGPA", session=s)

# Test 4: LOGIN AS ADMIN
print("\n--- ADMIN DASHBOARD ---")
s2 = TestSession()
status, _ = login(s2, "admin@college.edu", "admin123")
if status == 302:
    passed += 1
    print("  ✅ Admin login succeeds")
else:
    print(f"  ❌ Admin login: {status}")
    failed += 1

status, text = s2.get("/admin/dashboard")
if status == 200:
    passed += 1
    checks = ["Admin Dashboard", "Total Students", "Recent Predictions"]
    for c in checks:
        if c in text:
            passed += 1
            print(f"  ✅ Admin contains '{c}'")
        else:
            failed += 1
            print(f"  ❌ Admin missing '{c}'")
else:
    print(f"  ❌ Admin dashboard returned {status}")
    failed += 1

test("Manage students loads", "GET", "/admin/students", expected_status=200, check_text="student", session=s2)
test("Admin reports loads", "GET", "/admin/reports", expected_status=200, session=s2)
test("Excel export works", "GET", "/admin/reports/excel", expected_status=200, session=s2)

# Test 5: API ENDPOINTS
print("\n--- API ENDPOINTS ---")
status, text = s2.get("/api/dashboard/stats")
if status == 200:
    passed += 1
    try:
        data = json.loads(text)
        if data.get("success") and "data" in data:
            passed += 1
            print(f"  ✅ API returns valid JSON with total_students={data['data'].get('total_students')}")
        else:
            failed += 1
            print(f"  ❌ API response missing success/data keys")
    except:
        failed += 1
        print(f"  ❌ API response not valid JSON")
else:
    print(f"  ❌ API returned {status}")
    failed += 1

# Test 6: LOGIN AS COUNSELLOR
print("\n--- COUNSELLOR DASHBOARD ---")
s3 = TestSession()
status, _ = login(s3, "counsellor@college.edu", "counsellor123")
if status == 302:
    passed += 1
    print("  ✅ Counsellor login succeeds")
else:
    print(f"  ❌ Counsellor login: {status}")
    failed += 1

status, text = s3.get("/counsellor/dashboard")
if status == 200:
    passed += 1
    checks = ["Counsellor Dashboard", "High Risk", "Counselling Notes"]
    for c in checks:
        if c in text:
            passed += 1
            print(f"  ✅ Counsellor contains '{c}'")
        else:
            failed += 1
            print(f"  ❌ Counsellor missing '{c}'")
else:
    print(f"  ❌ Counsellor dashboard returned {status}")
    failed += 1

test("At-risk students loads", "GET", "/counsellor/at-risk", expected_status=200, session=s3)
test("Analytics page loads", "GET", "/counsellor/analytics", expected_status=200, session=s3)

# Test 7: DATABASE VERIFICATION
print("\n--- DATABASE VERIFICATION ---")
import mysql.connector
try:
    conn = mysql.connector.connect(host='localhost', user='root', database='dropout_prediction_db')
    cur = conn.cursor(dictionary=True)
    
    cur.execute("SELECT COUNT(*) as cnt FROM users")
    total_users = cur.fetchone()['cnt']
    cur.execute("SELECT COUNT(*) as cnt FROM users WHERE role='Student'")
    total_students = cur.fetchone()['cnt']
    cur.execute("SELECT COUNT(*) as cnt FROM users WHERE role='Admin'")
    total_admins = cur.fetchone()['cnt']
    cur.execute("SELECT COUNT(*) as cnt FROM users WHERE role='Counsellor'")
    total_counsellors = cur.fetchone()['cnt']
    cur.execute("SELECT COUNT(*) as cnt FROM students")
    total_student_profiles = cur.fetchone()['cnt']
    cur.execute("SELECT COUNT(*) as cnt FROM academic_records")
    total_academic = cur.fetchone()['cnt']
    cur.execute("SELECT COUNT(*) as cnt FROM dropout_predictions")
    total_predictions = cur.fetchone()['cnt']
    cur.execute("SELECT COUNT(*) as cnt FROM counselling_recommendations")
    total_counselling = cur.fetchone()['cnt']
    cur.execute("SELECT COUNT(*) as cnt FROM notifications")
    total_notifications = cur.fetchone()['cnt']
    cur.execute("SELECT COUNT(*) as cnt FROM behaviour_records")
    total_behaviour = cur.fetchone()['cnt']
    
    print(f"  ✅ Users: {total_users} (Students: {total_students}, Admin: {total_admins}, Counsellors: {total_counsellors})")
    print(f"  ✅ Student profiles: {total_student_profiles}")
    print(f"  ✅ Academic records: {total_academic}")
    print(f"  ✅ Predictions: {total_predictions}")
    print(f"  ✅ Counselling notes: {total_counselling}")
    print(f"  ✅ Notifications: {total_notifications}")
    print(f"  ✅ Behaviour records: {total_behaviour}")
    
    if total_students == 20:
        passed += 1
        print(f"  ✅ Exactly 20 students exist")
    else:
        failed += 1
        print(f"  ❌ Expected 20 students, got {total_students}")
    
    cur.close()
    conn.close()
except Exception as e:
    failed += 1
    print(f"  ❌ Database error: {e}")

# Test 8: STUDENT ACADEMIC RECORD CRUD
print("\n--- STUDENT CRUD OPERATIONS ---")
s4 = TestSession()
login(s4, "student01@college.edu", "Student@123")
status, text = s4.post("/student/academic/add", {
    "semester": "6",
    "cgpa": "8.5",
    "attendance": "90",
    "internal_marks": "85",
    "backlog_count": "0",
    "study_hours": "4"
})
if status == 302:
    passed += 1
    print("  ✅ Add academic record succeeds (redirect)")
else:
    failed += 1
    print(f"  ❌ Add academic record failed: {status}")

# Test duplicate semester handling
status, text = s4.post("/student/academic/add", {
    "semester": "6",
    "cgpa": "8.2",
    "attendance": "88",
    "internal_marks": "82",
    "backlog_count": "0",
    "study_hours": "5"
})
if status == 302:
    passed += 1
    print("  ✅ Duplicate semester handles gracefully (redirect)")
else:
    failed += 1
    print(f"  ❌ Duplicate semester failed: {status}")

# Test 9: ALL 20 STUDENT LOGINS
print("\n--- ALL STUDENT LOGIN VERIFICATION ---")
all_ok = True
for i in range(1, 21):
    s_test = TestSession()
    email = f"student{i:02d}@college.edu"
    status, _ = login(s_test, email, "Student@123")
    if status == 302:
        # Also verify dashboard loads
        d_status, _ = s_test.get("/student/dashboard")
        if d_status == 200:
            passed += 1
            if i <= 3 or i >= 18:
                print(f"  ✅ {email} - login OK, dashboard OK")
        else:
            failed += 1
            all_ok = False
            print(f"  ❌ {email} - login OK but dashboard failed ({d_status})")
    else:
        failed += 1
        all_ok = False
        print(f"  ❌ {email} - login FAILED ({status})")

if all_ok:
    print("  ✅ All 20 student accounts verified successfully")

# SUMMARY
print("\n" + "=" * 60)
print(f"AUDIT SUMMARY: {passed} passed, {failed} failed")
print("=" * 60)
if errors:
    print("\nFAILURES:")
    for e in errors[:20]:
        print(f"  {e}")
    if len(errors) > 20:
        print(f"  ... and {len(errors)-20} more errors")

sys.exit(0 if failed == 0 else 1)