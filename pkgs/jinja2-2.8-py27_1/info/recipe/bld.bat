"%PYTHON%" setup.py install --old-and-unmanageable
if errorlevel 1 exit 1

del %SP_DIR%\__pycache__\pkg_res*
if errorlevel 1 echo "Pass"
