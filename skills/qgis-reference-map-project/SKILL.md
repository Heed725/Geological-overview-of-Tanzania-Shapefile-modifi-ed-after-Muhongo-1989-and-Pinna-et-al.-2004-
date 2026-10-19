---
name: qgis-reference-map-project
description: Build or repair editable QGIS projects from illustrated reference maps, matching legend colours while using real national outlines and island coastlines. Use for geological or categorical map replication, smoothing traced borders, restoring missing patches, packaging portable projects, or updating the Tanzania overview after Muhongo (1989) and Pinna et al. (2004).
---

# QGIS reference-map projects

## Establish geometry and appearance

1. Read the image, project and data before editing. Inspect legend colours, CRS, layer sources, coastline and important small patches.
2. Start a correction from the accepted project. Change the requested feature without regenerating unrelated geometry or redesigning the map.
3. Distinguish real geographic GIS outlines, source geological boundaries and image-derived geological interpretations in attributes and documentation. Preserve source fields and licences.
4. Use real national/administrative outlines and real island polygons when a standard GIS boundary is wanted. Match the internal geology separately. Repeatedly rounding image pixels does not reconstruct a coastline.
5. Sample the interiors of solid legend swatches and save exact hexadecimal colours. Avoid antialiased edges and unrequested palette changes.

For this Tanzania map, read [references/tanzania.md](references/tanzania.md), including the accepted repository and Dar es Salaam regression check.

## Reconstruct and smooth contacts

- Register against printed coordinates or reliable control points. Record the transformation and source-image resolution; describe image-derived positions as approximate.
- Classify confident colour interiors, then fill dark text/strokes from neighbouring classes. Preserve white lakes and background separately. Include the original and an optional georeferenced comparison.
- Build a reference-component manifest before smoothing: class, area, bounds, interior point and ID. Flag important small components.
- Node shared contacts and process their edge chains together. Keep junctions fixed so adjoining units stay joined.
- Remove pixel noise at print scale before applying gentle curvature. Rounding a staircase creates scallops; aggressive simplification alone creates angular polygons. Inspect the final print-size render.
- Clip fills to the real mainland/land mask; retain accurate island coastlines separately. Document nearest-class extensions into small gaps between an old illustration and a real outline.
- Preserve identities through topology changes. Do not label changed faces from one representative point alone. Use source IDs or maximum overlap and compare every reference component afterwards. Class count and total coverage can pass while a small patch disappears.
- Restore missing patches by unioning accepted/reference geometry into the intended class and subtracting it from intersecting classes. Recheck coverage and appearance.
- Do not assign survey authority to image colours or symbol positions. Accurate island geometry does not establish accurate island geology.

## Assemble and verify QGIS

1. Use local GeoPackages and relative paths. Keep clear optional comparison layers and useful source attributes.
2. Follow the supplied design and user preferences. For Tanzania, use Barlow variants, a light layout, editable legend swatches and readable labels.
3. Save to an explicit absolute QGZ filename with relative layer-source storage. Reopen that exact file and assert that the new main layer and layout exist. Checking that old layers are valid can miss a stale project save.
4. Render the saved layout. Inspect geography, small class patches, colours, labels and scale-bar units. Hide raster comparison edges when they cover smooth vectors.
5. Check geometry validity, no material overlaps, no unfilled mask gaps and every important reference component. In Tanzania, require the Cretaceous patch southwest of Dar es Salaam, not merely a Cretaceous category.

Run the package auditor in a Python environment with QGIS:

```bash
python scripts/audit_qgis_package.py project.zip --layer-table geology_natural --expected-classes 15 --exact-parts cretaceous=4 --require-point cretaceous=38.7171500545,-7.1340460526 --mask-table mainland_outline --require-checksums
```

## Package and deliver

Commit layer edits before packaging. Never delete a live GeoPackage WAL as cleanup. Close providers when possible; use SQLite backup to capture committed pages, including WAL data, into a standalone file with DELETE journal mode.

```bash
python scripts/package_qgis_project.py project_directory project.zip
```

Place the output outside the source folder. The packager snapshots GeoPackages, excludes journals/backups, tests the ZIP and writes checksums. Audit the resulting archive: the auditor extracts it elsewhere and checks local sources, geometry, classes and required component counts.

Use the available persistent-file workflow for deliverables. Publish only to a repository authorized by the user; preserve existing content and include opening instructions, preview, source/licence notes and a QGIS badge when requested. Do not publish scratch experiments or incomplete versions.
