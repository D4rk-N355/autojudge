import os
import sqlite3
import subprocess
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

DB_FILE = "judge.db"
<<<<<<< HEAD
PROBLEM_ROOT = "problems"

app = Flask(__name__)
CORS(app)
=======

app = Flask(__name__)
CORS(app)  # 啟用跨域，讓 GitHub Pages 前端可以呼叫 API
>>>>>>> 8521d065de16b653ecf07adde3347775f58343c9


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem_id TEXT,
        source TEXT,
        status TEXT,
        time_ms REAL,
        message TEXT,
        testcase_id INTEGER
    )
    """)
    conn.commit()
    conn.close()


def judge(source_file, problem_id):
<<<<<<< HEAD
    problem_id = str(problem_id)
    folder = os.path.join(PROBLEM_ROOT, problem_id)
=======
    """Compile and run the C source; return (status, output_preview, fail_case)."""
    problem_id = str(problem_id)
>>>>>>> 8521d065de16b653ecf07adde3347775f58343c9
    os.makedirs("submissions", exist_ok=True)

    exe_file = os.path.abspath(
        f"submissions/{problem_id}.exe" if os.name == "nt" else f"submissions/{problem_id}.out"
    )

    # compile
    compile_cmd = ["gcc", source_file, "-o", exe_file]
    try:
        subprocess.check_output(compile_cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        msg = e.output.decode(errors="replace") if hasattr(e, 'output') and e.output else str(e)
        return "CE", msg[:200], None

    # run multiple testcases
    test_id = 1
<<<<<<< HEAD
    while os.path.exists(os.path.join(folder, f"input{str(test_id).zfill(2)}.txt")):
        input_file = os.path.join(folder, f"input{str(test_id).zfill(2)}.txt")
        expected_file = os.path.join(folder, f"expected{str(test_id).zfill(2)}.txt")
=======
    while os.path.exists(f"problems/{problem_id}/input{test_id}.txt"):
        input_file = f"problems/{problem_id}/input{test_id}.txt"
        expected_file = f"problems/{problem_id}/expected{test_id}.txt"
>>>>>>> 8521d065de16b653ecf07adde3347775f58343c9

        start = time.time()
        try:
            result = subprocess.run([exe_file],
                                    stdin=open(input_file),
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    timeout=2)
        except subprocess.TimeoutExpired:
            return "TLE", "Time Limit Exceeded", test_id

        elapsed = (time.time() - start) * 1000

        if result.returncode != 0:
            err_msg = result.stderr.decode(errors="replace") if result.stderr else "Runtime Error"
            return "RE", err_msg[:200], test_id

        output = result.stdout.decode().strip()
        expected = open(expected_file).read().strip()

        if output != expected:
            return "WA", f"第 {test_id} 筆測資錯誤，輸出: {output[:200]}", test_id

        test_id += 1

    return "AC", "所有測資通過", None


@app.route("/submit", methods=["POST"])
def submit():
    try:
        problem_id = request.form.get("problem_id")
        source_code = request.files["file"]

        source_path = f"submissions/{problem_id}.c"
        source_code.save(source_path)

        result, preview, fail_case = judge(source_path, problem_id)
        return jsonify({
            "status": "success",
            "data": {
                "problem_id": problem_id,
                "result": result,
                "output_preview": preview,
                "fail_case": fail_case
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "success", "data": {"service": "ok"}}), 200
<<<<<<< HEAD


@app.route("/problems", methods=["GET"])
def list_problems():
    try:
        problem_dirs = sorted([
            name for name in os.listdir(PROBLEM_ROOT)
            if os.path.isdir(os.path.join(PROBLEM_ROOT, name))
        ])
        data = [{"id": pid, "title": f"題目 {pid}"} for pid in problem_dirs]
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/problem/<pid>", methods=["GET"])
def get_problem(pid):
    try:
        folder = os.path.join(PROBLEM_ROOT, pid)
        doc_file = os.path.join(folder, f"{pid}doc.txt")

        if not os.path.exists(doc_file):
            return jsonify({"status": "error", "message": "題目敘述不存在"}), 404

        with open(doc_file, "r", encoding="utf-8") as f:
            description = f.read()

        count = 0
        while os.path.exists(os.path.join(folder, f"input{str(count+1).zfill(2)}.txt")):
            count += 1

        return jsonify({
            "status": "success",
            "data": {
                "id": pid,
                "description": description,
                "testcase_count": count
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
=======
>>>>>>> 8521d065de16b653ecf07adde3347775f58343c9


if __name__ == "__main__":
    os.makedirs(PROBLEM_ROOT, exist_ok=True)
    os.makedirs("submissions", exist_ok=True)
    init_db()
    port = int(os.environ.get("PORT", 8080))
<<<<<<< HEAD
    app.run(host="0.0.0.0", port=port)
=======
    app.run(host="0.0.0.0", port=port)
>>>>>>> 8521d065de16b653ecf07adde3347775f58343c9
