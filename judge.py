def judge(source_file, problem_id):
    problem_id = str(problem_id)
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
    while os.path.exists(f"problems/{problem_id}/input{test_id}.txt"):
        input_file = f"problems/{problem_id}/input{test_id}.txt"
        expected_file = f"problems/{problem_id}/expected{test_id}.txt"

        try:
            result = subprocess.run([exe_file],
                                    stdin=open(input_file),
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    timeout=2)
        except subprocess.TimeoutExpired:
            return "TLE", "Time Limit Exceeded", test_id

        if result.returncode != 0:
            err_msg = result.stderr.decode(errors="replace") if result.stderr else "Runtime Error"
            return "RE", err_msg[:200], test_id

        output = result.stdout.decode().strip()
        expected = open(expected_file).read().strip()

        if output != expected:
            return "WA", f"第 {test_id} 筆測資錯誤，輸出: {output[:200]}", test_id

        test_id += 1

    return "AC", "所有測資通過", None
