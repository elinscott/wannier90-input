from pathlib import Path

directory = Path(__file__).parent
files = {str(path.name): path / "parameters.xml" for path in directory.iterdir() if path.is_dir() and path.name != "__pycache__"}
