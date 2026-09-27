import kagglehub
import shutil
from pathlib import Path

data_dir = Path(__file__).parent

downloaded = kagglehub.dataset_download("adityadesai13/used-car-dataset-ford-and-mercedes")

downloaded_dir = Path(downloaded)
source = downloaded_dir / "toyota.csv"

if source.exists():
    destination = data_dir / source.name
    shutil.copy2(source, destination)
    print(f"Copied {source.name} to {destination}")
else:
    print(f"toyota.csv not found in {downloaded_dir}")
