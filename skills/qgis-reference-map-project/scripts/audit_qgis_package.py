#!/usr/bin/env python3
"""Extract a QGIS package elsewhere and audit source portability and geometry."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
import zipfile


def audit(args):
    os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
    from qgis.core import QgsApplication, QgsProject, QgsVectorLayer, QgsLayoutItemPicture, QgsGeometry, QgsPointXY
    app = QgsApplication([], False)
    app.initQgis()
    project = QgsProject.instance()
    with tempfile.TemporaryDirectory(prefix='qgis-relocation-audit-') as temporary:
        root = Path(temporary).resolve()
        with zipfile.ZipFile(args.archive) as archive:
            for name in archive.namelist():
                candidate = (root / name).resolve()
                if root not in candidate.parents and candidate != root:
                    raise ValueError('Archive contains an unsafe path')
            if archive.testzip() is not None:
                raise ValueError('Broken ZIP')
            archive.extractall(root)
        projects = sorted(root.rglob('*.qgz'))
        if len(projects) != 1:
            raise ValueError(f'Expected one QGZ, found {len(projects)}')
        manifests = list(root.rglob('package_checksums.json'))
        if args.require_checksums and len(manifests) != 1:
            raise ValueError('Expected one package checksum manifest')
        for manifest in manifests:
            for name, expected in json.loads(manifest.read_text()).items():
                path = (manifest.parent / name).resolve()
                if root not in path.parents or not path.is_file():
                    raise ValueError('Unsafe or missing checksum entry')
                if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                    raise ValueError(f'Checksum mismatch: {name}')
        if not project.read(str(projects[0])):
            raise ValueError('Project could not be reopened')
        layers = list(project.mapLayers().values())
        for layer in layers:
            if not layer.isValid():
                raise ValueError(f'Invalid layer: {layer.name()}')
            path = Path(layer.source().split('|', 1)[0]).resolve()
            if root not in path.parents or not path.is_file():
                raise ValueError(f'Nonportable source: {layer.name()}')
        candidates = [l for l in layers if isinstance(l, QgsVectorLayer)
                      and f'layername={args.layer_table}' in l.source()]
        if len(candidates) != 1:
            raise ValueError('Requested main table was not found uniquely')
        main = candidates[0]
        classes = set()
        parts = {}
        geometries = {}
        for feature in main.getFeatures():
            geometry = feature.geometry()
            if geometry.isEmpty() or not geometry.isGeosValid():
                raise ValueError(f'Invalid feature {feature.id()}')
            key = str(feature[args.class_field])
            classes.add(key)
            geometries.setdefault(key, []).append(QgsGeometry(geometry))
            count = len(geometry.asGeometryCollection()) if geometry.isMultipart() else 1
            parts[key] = parts.get(key, 0) + count
        if args.expected_classes is not None and len(classes) != args.expected_classes:
            raise ValueError(f'Class count changed: {len(classes)}')
        for requirement in args.require_parts:
            key, count = requirement.rsplit('=', 1)
            if parts.get(key, 0) < int(count):
                raise ValueError(f'Missing {key} patch: {parts.get(key, 0)} parts')
        for requirement in args.exact_parts:
            key, count = requirement.rsplit('=', 1)
            if parts.get(key, 0) != int(count):
                raise ValueError(f'Unexpected {key} parts: {parts.get(key, 0)}')
        for requirement in args.require_point:
            key, xy = requirement.rsplit('=', 1)
            x, y = map(float, xy.split(','))
            point = QgsGeometry.fromPointXY(QgsPointXY(x, y))
            if not any(g.intersects(point) for g in geometries.get(key, [])):
                raise ValueError(f'Missing {key} at required coordinate')
        layout_names = [l.name() for l in project.layoutManager().layouts()]
        if args.require_layout and args.require_layout not in layout_names:
            raise ValueError('Required named layout is absent')
        if args.mask_table:
            mask_layer = next((l for l in layers if isinstance(l, QgsVectorLayer)
                               and f'layername={args.mask_table}' in l.source()), None)
            if mask_layer is None:
                raise ValueError('Required land mask table is absent')
            mask = QgsGeometry.unaryUnion([f.geometry() for f in mask_layer.getFeatures()])
            all_geoms = [g for group in geometries.values() for g in group]
            union = QgsGeometry.unaryUnion(all_geoms)
            tolerance = max(1e-10, mask.area() * 1e-10)
            if mask.symDifference(union).area() > tolerance:
                raise ValueError('Geological coverage differs from land mask')
            if sum(g.area() for g in all_geoms) - union.area() > tolerance:
                raise ValueError('Geological classes overlap')
        for layout in project.layoutManager().layouts():
            for item in layout.items():
                if isinstance(item, QgsLayoutItemPicture) and item.picturePath():
                    path = Path(item.picturePath()).resolve()
                    if root not in path.parents or not path.is_file():
                        raise ValueError('Nonportable layout picture')
        report = {'layers': len(layers), 'main_table': args.layer_table,
                  'classes': len(classes), 'parts_by_class': parts,
                  'layouts': len(project.layoutManager().layouts()),
                  'all_sources_portable': True, 'all_main_geometries_valid': True,
                  'checksum_manifest_verified': bool(manifests),
                  'required_points_verified': len(args.require_point),
                  'mask_coverage_verified': bool(args.mask_table)}
        project.clear()
    app.exitQgis()
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive')
    parser.add_argument('--layer-table', required=True)
    parser.add_argument('--class-field', default='map_key')
    parser.add_argument('--expected-classes', type=int)
    parser.add_argument('--require-parts', action='append', default=[])
    parser.add_argument('--exact-parts', action='append', default=[])
    parser.add_argument('--require-point', action='append', default=[], help='CLASS=X,Y in main layer coordinates')
    parser.add_argument('--require-layout')
    parser.add_argument('--mask-table')
    parser.add_argument('--require-checksums', action='store_true')
    audit(parser.parse_args())
