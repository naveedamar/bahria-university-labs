import kagglehub

kagglehub.dataset_download(
    "sergionefedov/dubai-real-estate-sales-and-rentals-20202026",
    path="rentals.csv",
    output_dir="."
)