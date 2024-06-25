import geopandas as gpd
import os

# import zipfile

def clean_shapefile(shapefile, cleaned_folder):
    # reads file in and checks for errors
    try:
        data = gpd.read_file(shapefile)
    except Exception as e:
        raise ValueError(f"Error: problem reading shapefile {shapefile}: {e}")

    # find file name without directory or extensions
    filename = os.path.splitext(os.path.basename(shapefile))[0]

    # make sure there is not already a cleaned file
    cleaned_filename = f"{filename}_cleaned.shp"
    cleaned_file_path = os.path.join(cleaned_folder, cleaned_filename)
    if os.path.exists(cleaned_file_path):
        raise ValueError(f"Error: duplicate file already cleaned, did not clean")

    # required columns check
    required_columns = ["name", "geometry"]
    if not all(col in data.columns for col in required_columns):
        raise ValueError(f"Error: shapefile {shapefile} is missing required columns: {required_columns}")

    # delete all but name and geometry columns
    columns_to_keep = ["name", "geometry"]
    columns_to_drop = [col for col in data.columns if col not in columns_to_keep]
    data.drop(columns_to_drop, axis=1, inplace=True)

    # changes every field name to an indexed field name
    unique_values = data['name'].unique()
    mapping = {value: f"Field {i+1}" for i, value in enumerate(unique_values)}
    data['name'] = data['name'].map(mapping)

    # outputs file as "filename"_cleaned in the Cleaned_files
    try:
        data.to_file(cleaned_file_path, driver="ESRI Shapefile")
    except Exception as e:
        raise ValueError(f"Error: problem writing cleaned shapefile to {cleaned_file_path}: {e}")

    return cleaned_file_path

def main():
    print()
    terminal_width = os.get_terminal_size().columns
    print("#" * terminal_width)

    folder_path = input(f"Enter the folder path containing the .shp files you want to clean.\n")

    # checks for real folder
    if not os.path.exists(folder_path):
        print("Error: folder not found, check your folder path")
        return

    # makes a list of .shp files in recursive search of folder
    shapefiles = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
    # possible improvement to work with .zip files (not finished)
            # if file.endswith('.zip'):
            #     zip_file_path = os.path.join(root, file)
            #     with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            #         zip_ref.extractall(os.path.join(root, file[:-4]))
            if file.endswith(".shp"):
                if file not in shapefiles:
                    shapefiles.append(os.path.join(root, file))
                else:
                    raise ValueError(f"Error: there are duplicate file names, only cleaned first duplicate")

    # checks for proper file extension
    if not shapefiles:
        print("Error: no .shp files in folder path")
        return

    # creates new folder for cleaned shape files in parent folder
    parent_folder = os.path.dirname(folder_path)
    cleaned_folder = os.path.join(parent_folder, "Cleaned_Shapefiles")
    os.makedirs(cleaned_folder, exist_ok=True)

    for i, shapefile in enumerate(shapefiles, start = 1):
        try:
            output_fp = clean_shapefile(shapefile, cleaned_folder)
            print(f" {i})  cleaned file saved as {output_fp}")
        except ValueError as e:
            print(f" {i})  ERROR cleaning file {shapefile}: {e}")


    print("#" * terminal_width)
    print()
    return

if __name__ == "__main__":
    main()


# POSSIBLE IMPROVEMENTS:
# Let it handle .zip files in line

