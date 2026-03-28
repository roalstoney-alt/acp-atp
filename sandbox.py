import subprocess

def run_in_sandbox(code):
    try:
        result = subprocess.run(
            ["python3", "-c", code],
            capture_output=True,
            timeout=2
        )
        return result.stdout.decode(), None
    except Exception as e:
        return None, str(e)