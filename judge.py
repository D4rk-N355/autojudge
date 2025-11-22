import os
import time
import sqlite3
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_FILE = "judge.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem_id INTEGER,
        source TEXT,
        status TEXT,
        time_ms REAL,
        message TEXT
    )
    """)
    conn.commit()
    conn.close()

def judge(source_file, problem_id):
    """Compile and run the C source; return (status, output_preview).

    status: one of CE, TLE, RE, WA, AC
    output_preview: first 200 chars of program output (or error message)
    """
    problem_id = str(problem_id)
    # paths
    os.makedirs("submissions", exist_ok=True)
    exe_file = os.path.abspath(f"submissions/{problem_id}.exe" if os.name == "nt" else f"submissions/{problem_id}.out")
    output_file = os.path.abspath(f"submissions/{problem_id}.out.txt")
    input_file = os.path.abspath(f"problems/{problem_id}/input.txt")
    expected_file1 = os.path.abspath(f"problems/{problem_id}/expected.txt")
    expected_file2 = os.path.abspath(f"problems/{problem_id}/expect.txt")

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # compile
    compile_cmd = ["gcc", source_file, "-o", exe_file]
    try:
        subprocess.check_output(compile_cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        msg = e.output.decode(errors="replace") if hasattr(e, 'output') and e.output else str(e)
        c.execute("INSERT INTO submissions(problem_id,source,status,message) VALUES (?,?,?,?)",
                  (problem_id, source_file, "CE", msg))
        conn.commit()
        conn.close()
        return "CE", msg[:200]

    # run
    start = time.time()
    try:
        with open(input_file, "r") as fin, open(output_file, "w", encoding="utf-8") as fout:
            result = subprocess.run(
                [exe_file],
                stdin=fin,
                stdout=fout,
                stderr=subprocess.PIPE,
                timeout=2
            )
    except subprocess.TimeoutExpired:
        status = "TLE"
        c.execute("INSERT INTO submissions(problem_id,source,status,message) VALUES (?,?,?,?)",
                  (problem_id, source_file, status, "Time Limit Exceeded"))
        conn.commit()
        conn.close()
        return status, "Time Limit Exceeded"

    elapsed = (time.time() - start) * 1000

    # runtime error
    if result.returncode != 0:
        err_msg = result.stderr.decode(errors="replace") if result.stderr else "Runtime Error"
        status = "RE"
        c.execute("INSERT INTO submissions(problem_id,source,status,message,time_ms) VALUES (?,?,?,?,?)",
                  (problem_id, source_file, status, err_msg, elapsed))
        conn.commit()
        conn.close()
        return status, err_msg[:200]

    # compare output
    try:
        with open(output_file, "r", encoding="utf-8") as f1:
            output_data = f1.read().strip()
    except FileNotFoundError:
        output_data = ""

    expected_path = expected_file1 if os.path.exists(expected_file1) else (expected_file2 if os.path.exists(expected_file2) else None)
    if expected_path is None:
        status = "RE"
        message = "Expected output file not found"
        c.execute("INSERT INTO submissions(problem_id,source,status,message,time_ms) VALUES (?,?,?,?,?)",
                  (problem_id, source_file, status, message, elapsed))
        conn.commit()
        conn.close()
        return status, message

    try:
        with open(expected_path, "r", encoding="utf-8") as f2:
            expected_data = f2.read().strip()
        status = "AC" if output_data == expected_data else "WA"
    except Exception as e:
        status = "RE"
        output_data = ""

    preview = (output_data or "")[:200]

    c.execute("INSERT INTO submissions(problem_id,source,status,time_ms,message) VALUES (?,?,?,?,?)",
              (problem_id, source_file, status, elapsed, ""))
    conn.commit()
    conn.close()
    return status, preview

@app.route("/submit", methods=["POST"])
def submit():
    problem_id = request.form.get("problem_id")
    source_code = request.files["file"]

    # 存檔
    os.makedirs("submissions", exist_ok=True)
    source_path = f"submissions/{problem_id}.c"
    source_code.save(source_path)

    # 判題
    result, preview = judge(source_path, problem_id)
    return jsonify({
        "problem_id": problem_id,
        "result": result,
        "output_preview": preview
    })

if __name__ == "__main__":
    os.makedirs("problems", exist_ok=True)
    os.makedirs("submissions", exist_ok=True)
    init_db()
    app.run(host="0.0.0.0", port=3000)