"""
Batch reprojection of ASTER GDEM tiles to the Greek Grid (GGRS87)
==================================================================

Python (ArcPy) version of the ModelBuilder model used in Exercise 4
(model "Model2" in Exercise_4.atbx, ArcGIS Pro).

The model iterates over every raster in a file geodatabase and projects it
from WGS84 geographic coordinates to GGRS87 / Greek Grid (EPSG:2100),
using nearest-neighbour resampling and the GGRS_1987_To_WGS_1984 datum
transformation. The projected DEMs were then compared with the national DEM
(elevation differences, mean and standard deviation).

Requirements: ArcGIS Pro (ArcPy). Input data are not included.
"""

import os
import arcpy

IN_WORKSPACE = r".\DEM.gdb"      # geodatabase with the ASTER GDEM tiles
OUT_WORKSPACE = r".\DEM.gdb"     # where the projected rasters are written

OUT_SR = arcpy.SpatialReference(2100)    # GGRS87 / Greek Grid
IN_SR = arcpy.SpatialReference(4326)     # WGS84
CELL_SIZE = "28.4285624970768 28.4285624970768"   # metres
TRANSFORM = "GGRS_1987_To_WGS_1984"


def main():
    arcpy.env.workspace = IN_WORKSPACE
    arcpy.env.overwriteOutput = True

    rasters = arcpy.ListRasters()            # equivalent of "Iterate Rasters"
    for name in rasters:
        out_raster = os.path.join(OUT_WORKSPACE, f"{name}_P")   # %NAME%_P
        arcpy.management.ProjectRaster(
            in_raster=name,
            out_raster=out_raster,
            out_coor_system=OUT_SR,
            resampling_type="NEAREST",
            cell_size=CELL_SIZE,
            geographic_transform=TRANSFORM,
            in_coor_system=IN_SR,
        )
        print(f"Projected {name} -> {out_raster}")


if __name__ == "__main__":
    main()
