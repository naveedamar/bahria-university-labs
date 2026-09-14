import kagglehub
import shutil
from pathlib import Path

data_dir = Path(__file__).parent

downloaded = kagglehub.dataset_download(
    "eugeniyosetrov/building-permits"
)

downloaded_dir = Path(downloaded)

csv_files = list(downloaded_dir.glob("*.csv"))

if csv_files:
    source = csv_files[0]
    destination = data_dir / source.name
    shutil.copy2(source, destination)
    print(f"Copied {source.name} to {destination}")
else:
    print("No CSV file found.")