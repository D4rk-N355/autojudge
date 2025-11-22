import os
import subprocess

def run_case(case_id, input_file, expected_file, exe_cmd):
    with open(expected_file, "r", encoding="utf-8") as f:
        expected = f.read().rstrip("\n")

    with open(input_file, "r", encoding="utf-8") as f:
        try:
            result = subprocess.run(
                exe_cmd,
                stdin=f,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5
            )
        except subprocess.TimeoutExpired:
            print(f"❌ {case_id}.in: Timeout")
            return

    got = result.stdout.rstrip("\n")

    if expected == got:
        print(f"✅ {case_id}.in: Pass")
    else:
        print(f"❌ {case_id}.in: Fail")
        print("   🔻 [Expected]:")
        print(expected)
        print("   -----------------------------------")
        print("   🔺 [Got]:")
        print(got)
        if result.stderr:
            print("   ⚠️ stderr:")
            print(result.stderr.strip())

def main():
    problem_id = "01"
    folder = os.path.join("problems", problem_id)
    exe_cmd = ["python", "main.py"]

    for i in range(1, 21):
        case_id = f"{problem_id}{str(i).zfill(2)}"
        input_file = os.path.join(folder, f"input{case_id}.txt")
        expected_file = os.path.join(folder, f"expected{case_id}.txt")

        if os.path.exists(input_file) and os.path.exists(expected_file):
            run_case(case_id, input_file, expected_file, exe_cmd)

if __name__ == "__main__":
    main()
