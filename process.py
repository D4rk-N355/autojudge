import os

def generate_test_files(folder, prefix, count=20):
    """
    在指定資料夾生成 input/expected 檔案
    prefix: 題號字串，例如 "01"
    count: 要生成的筆數，預設 20
    """
    os.makedirs(folder, exist_ok=True)

    for i in range(1, count+1):
        num = str(i).zfill(2)  # 01, 02, ... 20

        input_file = os.path.join(folder, f"input{prefix}{num}.txt")
        expected_file = os.path.join(folder, f"expected{prefix}{num}.txt")

        # 建立 input 檔案
        with open(input_file, "w", encoding="utf-8") as f:
            f.write(f"# Input data for {prefix}{num}\n")

        # 建立 expected 檔案
        with open(expected_file, "w", encoding="utf-8") as f:
            f.write(f"# Expected output for {prefix}{num}\n")

        print(f"Generated: {input_file}, {expected_file}")

if __name__ == "__main__":
    # 你可以在這裡輸入題號，例如 "01"
    prefix = "12"
    target_folder = os.path.join("problems", prefix)
    generate_test_files(target_folder, prefix, count=20)