import geopandas as gpd
import os

def clean_shapefile(shapefile):
    data = gpd.read_file(shapefile)

    # find file name without director or extensions
    filename = os.path.splitext(os.path.basename(shapefile))[0]

    # delete all but name and geometry columns
    data.drop(data.columns[1:18], axis=1, inplace=True)

    # changes every field name to an indexed field name
    unique_values = data['name'].unique()
    mapping = {value: f"Field {i+1}" for i, value in enumerate(unique_values)}
    data['name'] = data['name'].map(mapping)

    # outputs file as "filename"_cleaned
    ouptut_fp = f"{filename}_cleaned.shp"
    data.to_file(ouptut_fp, driver="ESRI Shapefile")

    return ouptut_fp

def main():
    print()
    terminal_width = os.get_terminal_size().columns
    print("#" * terminal_width)

    fp = input("Enter the path to the shapefile you want to clean:\n")


    # checks for real file
    if not os.path.exists(fp):
        print("File not found. Check your file path")
        return

    # checks for proper file extension
    if not fp.endswith(".shp"):
        print("Invalid file type. Please enter a .shp file.")
        return
    output_fp = clean_shapefile(fp)

    print(f"Cleaned file saved as {output_fp}")
    print("#" * terminal_width)
    print()

if __name__ == "__main__":
    main()