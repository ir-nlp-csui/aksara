import os

def _get_foma_script_path() -> str:
    return os.path.join(
        os.path.dirname(__file__),
        'aksara@v1.4.0.bin'
    )