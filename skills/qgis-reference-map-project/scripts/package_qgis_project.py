#!/usr/bin/env python3
"""Snapshot a portable QGIS directory, including committed GeoPackage WAL data."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile
import zipfile


def package(source, output):
    source = Path(source).resolve()
    output = Path(output).resolve()
    if not source.is_dir() or not list(source.rglob('*.qgz')):
        raise ValueError('Source must contain a QGZ project')
    if output == source or source in output.parents:
        raise ValueError('Place the output ZIP outside the source directory')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='qgis-package-') as temporary:
        stage = Path(temporary) / source.name
        hashes = {}
        for item in sorted(source.rglob('*')):
            relative = item.relative_to(source)
            if not item.is_file() or item.is_symlink():
                continue
            if any(p in {'.git', '__pycache__'} for p in relative.parts):
                continue
            if item.name.endswith(('~', '.bak', '.gpkg-wal', '.gpkg-shm', '.pyc')):
                continue
            target = stage / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if item.suffix.lower() == '.gpkg':
                original = sqlite3.connect(item.as_uri() + '?mode=ro', uri=True)
                snapshot = sqlite3.connect(target)
                try:
                    original.backup(snapshot)
                    snapshot.execute('PRAGMA journal_mode=DELETE')
                    if snapshot.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
                        raise ValueError(f'Invalid GeoPackage: {relative}')
                finally:
                    snapshot.close()
                    original.close()
            else:
                shutil.copy2(item, target)
            hashes[relative.as_posix()] = hashlib.sha256(target.read_bytes()).hexdigest()
        (stage / 'package_checksums.json').write_text(
            json.dumps(hashes, indent=2) + '\n', encoding='utf-8'
        )
        temporary_zip = Path(temporary) / 'ready.zip'
        with zipfile.ZipFile(temporary_zip, 'w', zipfile.ZIP_DEFLATED) as archive:
            for item in sorted(stage.rglob('*')):
                if item.is_file():
                    archive.write(item, item.relative_to(stage.parent).as_posix())
        with zipfile.ZipFile(temporary_zip) as archive:
            if archive.testzip() is not None:
                raise ValueError('ZIP integrity check failed')
        shutil.copy2(temporary_zip, output)
    print(json.dumps({'archive': str(output), 'files': len(hashes),
                      'sha256': hashlib.sha256(output.read_bytes()).hexdigest()}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source')
    parser.add_argument('output')
    args = parser.parse_args()
    package(args.source, args.output)
