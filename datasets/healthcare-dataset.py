import shutil
from pathlib import Path

import kagglehub

data_dir = Path(__file__).parent

downloaded = kagglehub.dataset_download("prasad22/healthcare-dataset")

downloaded_dir = Path(downloaded)
csv_files = list(downloaded_dir.glob("*.csv"))

if csv_files:
    for source in csv_files:
        destination = data_dir / source.name
        shutil.copy2(source, destination)
        print(f"Copied {source.name} to {destination}")
else:
    print(f"No CSV file found in {downloaded_dir}")
