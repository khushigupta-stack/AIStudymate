from flask import Flask, request, redirect, session, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
app=Flask(__name__)
app.secret_key="ai_studymate_secret"
@app.route("/")
@app.route("/landing")
def landing():
    return render_template("landing.html")
def get_db():
    conn = sqlite3.connect("database.db", timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout = 10000")
    return conn
def init_db():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS weak_topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT,
            topic TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            score INTEGER,
            total INTEGER
        )
    """)

    conn.commit()
    conn.close()

subjects = []
weak_topics = []
quiz_results = []

study_topics = {
    "python": [
        "Python Basics",
        "Variables and Data Types",
        "If-Else and Loops",
        "Functions",
        "Lists, Tuples and Dictionaries",
        "Object-Oriented Programming",
        "Revision and Mini Test"
    ],

    "java": [
        "Java Basics",
        "Variables and Data Types",
        "Conditions and Loops",
        "Methods",
        "Arrays and Strings",
        "OOP Concepts",
        "Revision and Mini Test"
    ],

    "machine learning": [
        "Introduction to Machine Learning",
        "Types of Machine Learning",
        "Data Preprocessing",
        "Linear Regression",
        "Classification",
        "Model Evaluation",
        "Revision and Mini Test"
    ]
}


# =========================
# SUBJECT-WISE QUIZ QUESTIONS
# =========================

quiz_questions = {

    "python": [
        {
            "question": "Which keyword is used to define a function in Python?",
            "options": ["function", "def", "fun", "define"],
            "answer": "def",
            "topic": "Python Functions",
            "explanation": "def keyword is used to define a function in Python."
        },
        {
            "question": "Which data type stores True or False?",
            "options": ["int", "string", "bool", "float"],
            "answer": "bool",
            "topic": "Python Data Types",
            "explanation": "bool stores True or False values."
        },
        {
            "question": "Which symbol is used for comments in Python?",
            "options": ["//", "#", "/*", "--"],
            "answer": "#",
            "topic": "Python Comments",
            "explanation": "# is used for comments in Python."
        },
        {
            "question": "Which function displays output in Python?",
            "options": ["display()", "show()", "print()", "output()"],
            "answer": "print()",
            "topic": "Python Output",
            "explanation": "print() displays output."
        },
        {
            "question": "Which brackets are used to create a list?",
            "options": ["()", "{}", "[]", "<>"],
            "answer": "[]",
            "topic": "Python Lists",
            "explanation": "Square brackets [] are used to create a list."
        }
    ],

    "java": [
        {
            "question": "Which keyword is used to create a class in Java?",
            "options": ["class", "Class", "define", "struct"],
            "answer": "class",
            "topic": "Java Classes",
            "explanation": "The class keyword is used to define a class."
        },
        {
            "question": "Which method is the starting point of a Java program?",
            "options": ["start()", "main()", "run()", "execute()"],
            "answer": "main()",
            "topic": "Java Basics",
            "explanation": "main() is the entry point of a Java application."
        },
        {
            "question": "Which data type stores whole numbers?",
            "options": ["float", "String", "int", "boolean"],
            "answer": "int",
            "topic": "Java Data Types",
            "explanation": "int is used to store integer values."
        },
        {
            "question": "Which keyword is used for inheritance?",
            "options": ["inherit", "extends", "implements", "superclass"],
            "answer": "extends",
            "topic": "Java OOP",
            "explanation": "extends is used for class inheritance."
        },
        {
            "question": "Which symbol ends most Java statements?",
            "options": [".", ",", ";", ":"],
            "answer": ";",
            "topic": "Java Syntax",
            "explanation": "Most Java statements end with a semicolon."
        }
    ],

    "machine learning": [
        {
            "question": "What is Machine Learning?",
            "options": [
                "A programming language",
                "A method where computers learn from data",
                "A database",
                "An operating system"
            ],
            "answer": "A method where computers learn from data",
            "topic": "ML Introduction",
            "explanation": "Machine Learning allows systems to learn patterns from data."
        },
        {
            "question": "Which is a type of Machine Learning?",
            "options": [
                "Supervised Learning",
                "HTML Learning",
                "Database Learning",
                "Network Learning"
            ],
            "answer": "Supervised Learning",
            "topic": "ML Types",
            "explanation": "Supervised Learning is a major type of Machine Learning."
        },
        {
            "question": "Which algorithm is used for regression?",
            "options": ["Linear Regression",
                "K-Means",
                "Apriori",
                "DFS"
            ],
            "answer": "Linear Regression",
            "topic": "Regression",
            "explanation": "Linear Regression is commonly used for regression problems."
        },
        {
            "question": "What is training data?",
            "options": [
                "Data used to train a model",
                "Deleted data",
                "Only test data",
                "Random software"
            ],
            "answer": "Data used to train a model",
            "topic": "Training Data",
            "explanation": "Training data is used to learn model patterns."
        },
        {
            "question": "Which technique is commonly used for classification?",
            "options": [
                "Logistic Regression",
                "Linear Search",
                "Bubble Sort",
                "Binary Search"
            ],
            "answer": "Logistic Regression",
            "topic": "Classification",
            "explanation": "Logistic Regression is commonly used for classification."
        }
    ],

    "c++": [
        {
            "question": "Which symbol is used to end a C++ statement?",
            "options": [".", ";", ":", ","],
            "answer": ";",
            "topic": "C++ Syntax",
            "explanation": "C++ statements normally end with a semicolon."
        },
        {
            "question": "Which function is the entry point of a C++ program?",
            "options": ["start()", "main()", "run()", "begin()"],
            "answer": "main()",
            "topic": "C++ Basics",
            "explanation": "main() is the entry point of a C++ program."
        },
        {
            "question": "Which header is commonly used for cout?",
            "options": ["stdio.h", "iostream", "string.h", "math.h"],
            "answer": "iostream",
            "topic": "C++ Input Output",
            "explanation": "iostream provides cout and cin."
        },
        {
            "question": "Which operator is used for insertion into cout?",
            "options": ["<<", ">>", "==", "="],
            "answer": "<<",
            "topic": "C++ Operators",
            "explanation": "<< is the insertion operator used with cout."
        },
        {
            "question": "Which concept allows the same function name with different parameters?",
            "options": [
                "Inheritance",
                "Encapsulation",
                "Function Overloading",
                "Abstraction"
            ],
            "answer": "Function Overloading",
            "topic": "C++ OOP",
            "explanation": "Function overloading allows functions with the same name but different parameters."
        }
    ],

    "dbms": [
        {
            "question": "What does DBMS stand for?",
            "options": [
                "Database Management System",
                "Data Basic Management Software",
                "Database Machine System",
                "Data Backup Management System"
            ],
            "answer": "Database Management System",
            "topic": "DBMS Basics",
            "explanation": "DBMS stands for Database Management System."
        },
        {
            "question": "Which language is commonly used to query databases?",
            "options": ["HTML", "SQL", "CSS", "Python"],
            "answer": "SQL",
            "topic": "SQL",
            "explanation": "SQL is used to communicate with relational databases."
        },
        {
            "question": "Which key uniquely identifies a record?",
            "options": [
                "Foreign Key",
                "Primary Key",
                "Candidate Key",
                "Normal Key"
            ],
            "answer": "Primary Key",
            "topic": "Keys",
            "explanation": "A primary key uniquely identifies a record."
        },
        {
            "question": "Which command is used to retrieve data?",
            "options": ["SELECT", "INSERT", "DELETE", "UPDATE"],
            "answer": "SELECT",
            "topic": "SQL Commands",
            "explanation": "SELECT retrieves data from a database."
        },
        {
            "question": "What is a table?",
            "options": [
                "Collection of rows and columns",
                "A programming language",
                "A network",
                "An operating system"
            ],
            "answer": "Collection of rows and columns",
            "topic": "Database Tables",
            "explanation": "A database table organizes data into rows and columns."
        }
    ],

    "computer networks": [
        {
            "question": "What does LAN stand for?",
            "options": [
                "Local Area Network",
                "Large Area Network",
                "Long Area Network",
                "Local Access Node"
            ],
            "answer": "Local Area Network",
            "topic": "Networking Basics",
            "explanation": "LAN stands for Local Area Network."
        },
        {
            "question": "Which device connects different networks?",
            "options": ["Router", "Keyboard", "Monitor", "Printer"],
            "answer": "Router",
            "topic": "Network Devices",
            "explanation": "A router connects and directs traffic between networks."
        },
        {
            "question": "What does IP stand for?",
            "options": [
                "Internet Protocol",
                "Internet Program",
                "Internal Protocol",
                "Internet Port"
            ],
            "answer": "Internet Protocol",
            "topic": "IP Address",
            "explanation": "IP stands for Internet Protocol."
        },
        {
            "question": "Which protocol is used for web pages?",
            "options": ["HTTP", "FTP", "SMTP", "POP3"],
            "answer": "HTTP",
            "topic": "Network Protocols",
            "explanation": "HTTP is used for communication between web browsers and servers."
        },
        {
            "question": "Which device forwards packets between networks?",
            "options": ["Router", "Switch", "Hub", "Repeater"],
            "answer": "Router",
            "topic": "Routing",
            "explanation": "Routers forward packets between different networks."
        }
    ]
}
# =========================
# REGISTER
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        hashed_password = generate_password_hash(password)

        try:
            conn = get_db()

            conn.execute(
                """
                INSERT INTO users (name, email, password)
                VALUES (?, ?, ?)
                """,
                (name, email, hashed_password)
            )

            conn.commit()
            conn.close()

            return redirect("/login")

        except sqlite3.IntegrityError:

            message = "Email already registered!"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Register - AI StudyMate</title>

        <style>
            body {{
                font-family: Arial;
                background: #f4f7fb;
            }}

            .box {{
                width: 400px;
                margin: 80px auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            }}

            input {{
                width: 90%;
                padding: 12px;
                margin: 10px;
                border-radius: 8px;
                border: 1px solid #ccc;
            }}

            button {{
                padding: 12px 25px;
                background: #4f46e5;
                color: white;
                border: none;
                border-radius: 8px;
            }}
        </style>
    </head>

    <body>

        <div class="box">

            <h1>🎓 AI StudyMate</h1>
            <h2>Create Account</h2>

            <p>{message}</p>

            <form method="POST">

                <input
                    type="text"
                    name="name"
                    placeholder="Enter Name"
                    required
                >

                <input
                    type="email"
                    name="email"
                    placeholder="Enter Email"
                    required
                >

                <input
                    type="password"
                    name="password"
                    placeholder="Enter Password"
                    required
                >

                <button type="submit">
                    Register
                </button>

            </form>

            <p>
                Already have an account?
                <a href="/login">Login</a>
            </p>

        </div>

    </body>
    </html>
    """


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db()

        user = conn.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            return redirect("/home")

        else:

            message = "Invalid email or password!"

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>Login - AI StudyMate</title>

        <style>

            body {{
                font-family: Arial;
                background: #f4f7fb;
            }}

            .box {{
                width: 400px;
                margin: 80px auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            }}

            input {{
                width: 90%;
                padding: 12px;
                margin: 10px;
                border-radius: 8px;
                border: 1px solid #ccc;
            }}

            button {{
                padding: 12px 25px;
                background: #4f46e5;
                color: white;
                border: none;
                border-radius: 8px;
            }}

        </style>

    </head>

    <body>

        <div class="box">

            <h1>🎓 AI StudyMate</h1>

            <h2>Login</h2>

            <p>{message}</p>

            <form method="POST">

                <input
                    type="email"
                    name="email"
                    placeholder="Enter Email"
                    required
                >

                <input
                    type="password"
                    name="password"
                    placeholder="Enter Password"
                    required
                >

                <button type="submit">
                    Login
                </button>

            </form>

            <p>
                New student?
                <a href="/register">Create Account</a>
            </p>

        </div>

    </body>

    </html>
    """
# =========================
# HOME PAGE
# =========================
@app.route("/home", methods=["GET", "POST"])
def home():

    if "user_id" not in session:
        return redirect("/login")

    plan = ""

    if request.method == "POST":

        subject = request.form.get("subject", "").strip()
        days_text = request.form.get("days", "7").strip()

        if subject:

            try:
                days = int(days_text)
            except:
                days = 7

            subjects.append(subject)

            topics = study_topics.get(
                subject.lower(),
                [
                    f"Introduction to {subject}",
                    f"Basic Concepts of {subject}",
                    f"Important Topics of {subject}",
                    f"Practice Questions of {subject}",
                    f"Advanced Concepts of {subject}",
                    f"Revision of {subject}",
                    f"Mini Test of {subject}"
                ]
            )

            plan += f"""
            <div class="box">
                <h2>📅 {days}-Day Study Plan for {subject}</h2>
            """

            for i in range(days):

                topic = topics[i % len(topics)]

                plan += f"""
                <div class="day">
                    <h3>Day {i + 1} 📖</h3>
                    <p>{topic}</p>
                    <span>⏱️ Study: 1-2 hours</span>
                </div>
                """

            plan += "</div>"

    subject_list = ""

    for subject in subjects:

        subject_list += f"""
        <li>📚 {subject}</li>
        """

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>AI StudyMate</title>

        <style>

            body {{
                font-family: Arial, sans-serif;
                background: #f4f7fb;  
               margin: 0;
            }}

            .header {{
                background: #4f46e5;
                color: white;
                padding: 30px;
                text-align: center;
            }}

            .container {{
                max-width: 850px;
                margin: 30px auto;
                padding: 20px;
            }}

            .box {{
                background: white;
                padding: 25px;
                border-radius: 15px;
                margin-bottom: 20px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            }}

            input {{
                padding: 12px;
                margin: 5px;
                border: 1px solid #ccc;
                border-radius: 8px;
            }}

            .subject {{
                width: 50%;
            }}

            .days {{
                width: 100px;
            }}

            button {{
                padding: 12px 20px;
                background: #4f46e5;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
            }}

            button:hover {{
                background: #3730a3;
            }}

            li {{
                margin: 10px;
                font-size: 18px;
            }}

            .day {{
                background: #eef2ff;
                padding: 18px;
                margin: 12px 0;
                border-radius: 12px;
            }}

            .day h3 {{
                margin-top: 0;
            }}

            .day p {{
                font-size: 17px;
            }}

            .day span {{
                color: #555;
            }}

            a {{
                text-decoration: none;
            }}

        </style>

    </head>

    <body>

        <div class="header">

            <h1>🎓 AI StudyMate</h1>

            <p>Your Personalized Learning Assistant</p>

        </div>

        <div class="container">

            <div class="box">

                <h2>
                  👋 Welcome, {session.get("user_name", "Student")}!
                </h2>

                <p>
                    Create your own personalized study plan.
                </p>

            </div>

                

            <div class="box">

                <h2>📚 My Subjects</h2>

                <form method="POST">

                    <input
                        class="subject"
                        type="text"
                        name="subject"
                        placeholder="Enter subject e.g. Python"
                        required
                    >

                    <input
                        class="days"
                        type="number"
                        name="days"
                        min="1"
                        max="30"
                        value="7"
                        required
                    >

                    <button type="submit">
                        Generate Plan 🚀
                    </button>

                </form>

                <h3>Your Subjects:</h3>

                <ul>
                    {subject_list}
                </ul>

            </div>


            {plan}


            <div class="box">

                <h2>📝 Quiz</h2>

                <p>
                    Test your knowledge in any subject-.
                </p>

                <a href="/quiz">

                    <button>
                        Start Quiz 🚀
                    </button>

                </a>

            </div>


            <div class="box">

                <h2>📊 Progress Dashboard</h2>

                <p>
                    Track your learning progress.
                </p>

                <a href="/progress">

                    <button>
                        View Progress 📈
                    </button>

                </a>

            </div>
            <br><br>

<a href="/logout">

    <button>
        🚪 Logout
    </button>

</a>

        </div>

    </body>

    </html>
    """

# =========================
# QUIZ PAGE
# =========================


# =========================
# ANY SUBJECT QUIZ
# =========================

@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    if "user_id" not in session:
        return redirect("/login")

    result = ""
    questions = []
    selected_subject = ""

    # =========================
    # SELECT / SUBMIT QUIZ
    # =========================

    if request.method == "POST":

        selected_subject = request.form.get(
            "subject", ""
        ).strip().lower()

        questions = quiz_questions.get(
            selected_subject,
            []
        )

        # =========================
        # QUIZ SUBMISSION
        # =========================

        if request.form.get("quiz_submitted") == "yes":

            if questions:

                score = 0

                # Connect database
                conn = get_db()

                # Check every question
                for i, q in enumerate(questions):

                    user_answer = request.form.get(
                        f"q{i}"
                    )

                    if user_answer == q["answer"]:

                        score += 1

                    else:

                        # Save weak topic in database
                        conn.execute(
                            """
                            INSERT INTO weak_topics
                            (user_id, subject, topic)
                            VALUES (?, ?, ?)
                            """,
                            (
                                session["user_id"],
                                selected_subject,
                                q["topic"]
                            )
                        )

                # Save weak topics
                conn.commit()
                conn.close()

                # Save score in memory
                quiz_results.append(score)

                # Save result in database
                conn = get_db()

                conn.execute(
                    """
                    INSERT INTO quiz_results
                    (user_id, score, total)
                    VALUES (?, ?, ?)
                    """,
                    (
                        session["user_id"],
                        score,
                        len(questions)
                    )
                )

                conn.commit()
                conn.close()

                # Calculate percentage
                percentage = int(
                    (score / len(questions)) * 100
                )

                # Result message
                if percentage >= 80:

                    message = "Excellent work! 🎉"

                elif percentage >= 50:

                    message = "Good job! Keep practicing. 💪"

                else:

                    message = "Keep learning and try again! 📚"

                result = f"""
                <div class="box result">

                    <h2>🎯 Quiz Completed!</h2>

                    <h3>
                        Subject:
                        {selected_subject.title()}
                    </h3>

                    <h2>
                        Score:
                        {score}/{len(questions)}
                    </h2>

                    <h3>
                        📈 Percentage:
                        {percentage}%
                    </h3>

                    <p>
                        {message}
                    </p>

                    <br>

                    <a href="/progress">
                        📊 View Progress
                    </a>

                    <br><br>

                    <a href="/quiz?subject={selected_subject}">
                        🔄 Try Again
                    </a>

                    <br><br>

                    <a href="/home">
                        🏠 Back to Home
                    </a>

                </div>
                """

                # Don't show questions again
                questions = []

            else:

                result = """
                <div class="box error">

                    ❌ Quiz is not available for this subject yet.

                    <br><br>

                    Try:
                    Python, Java, C++, Machine Learning,
                    DBMS or Computer Networks.

                </div>
                """

    else:

        selected_subject = request.args.get(
            "subject",
            ""
        ).strip().lower()

        questions = quiz_questions.get(
            selected_subject,
            []
        )

    # =========================
    # CREATE QUESTIONS HTML
    # =========================

    questions_html = ""

    for i, q in enumerate(questions):

        options_html = ""

        for option in q["options"]:

            options_html += f"""
            <label>

                <input
                    type="radio"
                    name="q{i}"
                    value="{option}"
                    required
                >

                {option}

            </label>
            """

        questions_html += f"""
        <div class="box">

            <h3>
                Q{i + 1}. {q["question"]}
            </h3>

            {options_html}

        </div>
        """

    # =========================
    # QUIZ FORM
    # =========================

    quiz_form = ""

    if questions:

        quiz_form = f"""
        <form method="POST">

            <input
                type="hidden"
                name="subject"
                value="{selected_subject}"
            >

            <input
                type="hidden"
                name="quiz_submitted"
                value="yes"
            >

            {questions_html}

            <button type="submit">
                Submit Quiz ✅
            </button>

        </form>
        """

    # =========================
    # QUIZ PAGE
    # =========================

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>AI StudyMate Quiz</title>

        <style>

            body {{
                font-family: Arial, sans-serif;
                background: #f4f7fb;
                margin: 0;
            }}

            .header {{
                background: #4f46e5;
                color: white;
                padding: 30px;
                text-align: center;
            }}

            .container {{
                max-width: 850px;
                margin: 30px auto;
                padding: 20px;
            }}

            .box {{
                background: white;
                padding: 25px;
                border-radius: 15px;
                margin-bottom: 20px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            }}

            select {{
                width: 70%;
                padding: 13px;
                border-radius: 8px;
                border: 1px solid #ccc;
                font-size: 16px;
            }}

            label {{
                display: block;
                padding: 12px;
                margin: 5px 0;
                background: #f8f9ff;
                border-radius: 8px;
            }}

            label:hover {{
                background: #eef2ff;
            }}

            button {{
                padding: 13px 25px;
                background: #4f46e5;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
            }}

            button:hover {{
                background: #3730a3;
            }}

            .error {{
                color: #b91c1c;
            }}

            .result {{
                border-left: 6px solid #4f46e5;
            }}

            a {{
                color: #4f46e5;
                font-weight: bold;
                text-decoration: none;
            }}

        </style>

    </head>

    <body>

        <div class="header">

            <h1>📝 AI StudyMate Quiz</h1>

            <p>
                Choose a subject and test your knowledge
            </p>

        </div>

        <div class="container">
        <div class="box">

                <h2>📚 Select Subject</h2>

                <form method="POST">

                    <select
                        name="subject"
                        required
                    >

                        <option value="">
                            -- Select Subject --
                        </option>

                        <option value="python">
                            Python
                        </option>

                        <option value="java">
                            Java
                        </option>

                        <option value="machine learning">
                            Machine Learning
                        </option>

                        <option value="c++">
                            C++
                        </option>

                        <option value="dbms">
                            DBMS
                        </option>

                        <option value="computer networks">
                            Computer Networks
                        </option>

                    </select>

                    <br><br>

                    <button type="submit">
                        Start Quiz 🚀
                    </button>

                </form>

            </div>

            {result}

            {quiz_form}

            <br>

            <a href="/home">
                🏠 Back to Home
            </a>

        </div>

    </body>

    </html>
    """

    



# =========================
# PROGRESS DASHBOARD
# =========================

@app.route("/progress")
def progress():

    if "user_id" not in session:
        return redirect("/login")

    # =========================
    # GET QUIZ HISTORY
    # =========================

    conn = get_db()

    history = conn.execute(
        """
        SELECT score, total
        FROM quiz_results
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (session["user_id"],)
    ).fetchall()

    conn.close()

    # =========================
    # QUIZ HISTORY HTML
    # =========================

    history_html = ""

    for item in history:

        percent = int(
            (item["score"] / item["total"]) * 100
        )

        history_html += f"""
        <li>
            🎯 Score: {item["score"]}/{item["total"]}
            — {percent}%
        </li>
        """

    # =========================
    # LATEST SCORE
    # =========================

    if len(history) == 0:

        latest_score = "No quiz attempts yet"
        percentage = ""

    else:

        latest_score = f"{history[0]['score']}/{history[0]['total']}"

        percentage_value = int(
            (history[0]["score"] / history[0]["total"]) * 100
        )

        percentage = f"Percentage: {percentage_value}%"

    # =========================
    # GET WEAK TOPICS
    # =========================

    conn = get_db()

    weak_rows = conn.execute(
        """
        SELECT subject, topic
        FROM weak_topics
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (session["user_id"],)
    ).fetchall()

    conn.close()

    # =========================
    # WEAK TOPICS HTML
    # =========================

    weak_html = ""

    if weak_rows:

        for item in weak_rows:

            weak_html += f"""
            <li>
                ⚠️ {item["subject"].title()} -
                {item["topic"]}
            </li>
            """

    else:

        weak_html = """
        <li>
            🎉 No weak topics yet!
        </li>
        """

    # =========================
    # PROGRESS PAGE
    # =========================

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>Progress Dashboard</title>

        <style>

            body {{
                font-family: Arial, sans-serif;
                background: #f4f7fb;
                margin: 0;
            }}

            .header {{
                background: #4f46e5;
                color: white;
                padding: 30px;
                text-align: center;
            }}

            .container {{
                max-width: 800px;
                margin: 30px auto;
                padding: 20px;
            }}

            .box {{
                background: white;
                padding: 25px;
                border-radius: 15px;
                margin-bottom: 20px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            }}

            li {{
                margin: 12px;
                font-size: 18px;
            }}

            a {{
                color: #4f46e5;
                font-weight: bold;
                text-decoration: none;
            }}

        </style>

    </head>

    <body>

        <div class="header">

            <h1>📊 Progress Dashboard</h1>

            <p>Track your learning progress</p>

        </div>

        <div class="container">

            <div class="box">

                <h2>🎯 Latest Quiz Score</h2>

                <h3>{latest_score}</h3>

                <p>📈 {percentage}</p>

            </div>

            <div class="box">

                <h2>📚 Quiz History</h2>

                <ul>
                    {history_html}
                </ul>

            </div>

            <div class="box">

                <h2>⚠️ Weak Topics</h2>

                <ul>
                    {weak_html}
                </ul>

            </div>

            <div class="box">

                <a href="/quiz">
                    📝 Take Quiz Again
                </a>

                <br><br>

                <a href="/home">
                    🏠 Back to Home
                </a>

                <br><br>

                <a href="/logout">
                    🚪 Logout
                </a>

            </div>

        </div>

    </body>

    </html>
    """


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# =========================
# RUN APP
# =========================

# Initialize database when the application starts
init_db()

if __name__ == "__main__":
    app.run(debug=True)