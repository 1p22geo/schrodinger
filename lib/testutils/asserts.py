def assert_file_exists(file, timeout):
    for _ in range(timeout):
        try:
            with open(file, "rb") as f:
                assert f.readable()
                return True
        except:
            continue
    raise TimeoutError("Assert timeout expired")
