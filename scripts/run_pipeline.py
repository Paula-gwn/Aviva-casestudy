from src.data.data_prep import run_data_pipeline

if __name__ == "__main__":
    run_data_pipeline(
        repairers_path="data/raw/repairers.csv",
        postcodes_path="data/raw/ukpostcodes.csv",
        roads_path="data/raw/roads/roads.shp",
        output_dir="data/processed"
    )