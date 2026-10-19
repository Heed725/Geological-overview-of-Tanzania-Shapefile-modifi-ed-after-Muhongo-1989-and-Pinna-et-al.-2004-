# Tanzania geology shapefile exports

CRS: WGS 84, EPSG:4326. Add either SHP file to QGIS; its matching QML style uses the reference colours. Keep SHP, SHX, DBF, PRJ, CPG and QML together.

- Tanzania_Geology: 15 multipart colour classes, with real mainland outline, smooth interpreted geological contacts and the restored Cretaceous patch southwest of Dar es Salaam.
- Tanzania_Real_Islands: 10 detailed island polygons, including Pemba, Unguja, Mafia and Lake Victoria islands. Geometry: geoBoundaries gbOpen TZA ADM0 2021, CC BY 4.0. Island fills follow the reference and are not a new geological classification.

Fields: MAP_KEY (style category), UNIT_NAME (legend wording), ERA, HEX_COLOR and DATA_NOTE. UTF-8 text is identified by the CPG file. The full QGIS project retains more source information, comparison layers, layouts and fonts.

Reference: Geological overview of Tanzania, modified after Muhongo (1989) and Pinna et al. (2004), supplied by the user. Reference/publication rights remain with their rights holders. Geology is an image-derived cartographic interpretation, not a new survey. Mainland outline and lake edges: Natural Earth 1:10 million, public domain.

geoBoundaries source: https://www.geoboundaries.org/api/current/gbOpen/TZA/ADM0/
CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
Full project and attribution: ../docs/PROJECT_GUIDE.md in the repository, or the guide in the project archive.
