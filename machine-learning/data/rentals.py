import kagglehub
import shutil
from pathlib import Path

data_dir = Path(__file__).parent

downloaded = kagglehub.dataset_download(
    "sergionefedov/dubai-real-estate-sales-and-rentals-20202026"
)

source = Path(downloaded) / "rentals.csv"
destination = data_dir / "rentals.csv"

shutil.copy2(source, destination)

print(f"Copied rentals.csv to {destination}")