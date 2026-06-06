from functions.get_file_content import get_file_content


def test_get_file_content() -> None:
    result_1 = get_file_content("calculator", "lorem.txt")
    print(f"lorem.txt length: {len(result_1)}")
    print(f"lorem.txt truncated: {'truncated' in result_1}")
    print("============================================")
    result_2 = get_file_content("calculator", "main.py")
    print(result_2)
    print("============================================")
    result_3 = get_file_content("calculator", "pkg/calculator.py")
    print(result_3)
    print("============================================")
    result_4 = get_file_content("calculator", "/bin/cat")
    print(result_4)
    print("============================================")
    result_5 = get_file_content("calculator", "pkg/does_not_exist.py")
    print(result_5)


if __name__ == "__main__":
    test_get_file_content()
