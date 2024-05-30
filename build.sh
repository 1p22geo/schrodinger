#!/bin/bash
rm ./dist/libschrodinger-*
python -m build --verbose
python -m twine upload --repository pypi dist/* --verbose
