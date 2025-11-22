import os
import subprocess

def run_case(case_id, input_file, expected_file, exe_cmd):
    # 讀取 expected
    with open(expected_file, "r", encoding="utf-8") as f:
        expected = f.read().strip()

    # 執行程式，捕捉輸出
    with open(input_file, "r", encoding="utf-8") as f:
        result = subprocess.run(
            exe_cmd,
            stdin=f,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    got = result.stdout.strip()

    # 比對
    if expected == got:
        print(f"✅ {case_id}.in: Pass")
    else:
        print(f"❌ {case_id}.in: Fail")
        print("   🔻 [Expected]:")
        print(expected)
        print("   -----------------------------------")
        print("   🔺 [Got]:")
        print(got)

def main():
    # 這裡設定要測試的題號，例如 01
    problem_id = "01"
    folder = os.path.join("problems", problem_id)

    # 你的程式執行方式，例如 python main.py
    exe_cmd = ["python", "main.py"]

    # 跑所有 input/expected
    for i in range(1, 21):  # 假設有 20 組測資
        case_id = f"{problem_id}{str(i).zfill(2)}"
        input_file = os.path.join(folder, f"input{case_id}.txt")
        expected_file = os.path.join(folder, f"expected{case_id}.txt")

        if os.path.exists(input_file) and os.path.exists(expected_file):
            run_case(case_id, input_file, expected_file, exe_cmd)

if __name__ == "__main__":
    main()
