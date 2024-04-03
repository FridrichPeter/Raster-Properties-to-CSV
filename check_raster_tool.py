import arcpy
from datetime import datetime
import csv

# Define input and output parameters
input_folder = arcpy.GetParameterAsText(0)
output_csv = arcpy.GetParameterAsText(1)

# Start
time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
arcpy.AddMessage(time)

with open(output_csv, 'w', newline='') as csvfile, \
        open('error_log.txt', 'a') as error_file:
    fieldnames = ['Raster', 'Folder', 'CellSizeX', 'CellSizeY', 'Minimum', 'Maximum', 'ValueType']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Walk through all subfolders and list rasters
    for root, dirs, files in arcpy.da.Walk(input_folder, datatype="RasterDataset", type="TIF"):
        for file in files:
            raster_path = arcpy.os.path.join(root, file)
            try:
                cx = arcpy.management.GetRasterProperties(raster_path, "CELLSIZEX")
                cy = arcpy.management.GetRasterProperties(raster_path, "CELLSIZEY")
                cmin = arcpy.management.GetRasterProperties(raster_path, "MINIMUM")
                cmax = arcpy.management.GetRasterProperties(raster_path, "MAXIMUM")
                ctype = arcpy.management.GetRasterProperties(raster_path, "VALUETYPE")

                if any(prop is None for prop in (cx, cy, cmin, cmax, ctype)):
                    arcpy.management.CalculateStatistics(raster_path)
                    cx = arcpy.management.GetRasterProperties(raster_path, "CELLSIZEX")
                    cy = arcpy.management.GetRasterProperties(raster_path, "CELLSIZEY")
                    cmin = arcpy.management.GetRasterProperties(raster_path, "MINIMUM")
                    cmax = arcpy.management.GetRasterProperties(raster_path, "MAXIMUM")
                    ctype = arcpy.management.GetRasterProperties(raster_path, "VALUETYPE")

                writer.writerow({'Raster': file,
                                 'Folder': root,
                                 'CellSizeX': cx,
                                 'CellSizeY': cy,
                                 'Minimum': cmin,
                                 'Maximum': cmax,
                                 'ValueType': ctype})
            except arcpy.ExecuteError:
                error_file.write(f"Failed to retrieve properties for raster: {raster_path}\n")
                continue
# End
time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
arcpy.AddMessage(time)
arcpy.AddMessage("End")
