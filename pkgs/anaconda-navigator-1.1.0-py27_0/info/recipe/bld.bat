rd /s /q anaconda_navigator\app\Navigator.app

%PYTHON% setup.py install --old-and-unmanageable
if errorlevel 1 exit 1

set MENU_DIR=%PREFIX%\Menu
IF NOT EXIST (%MENU_DIR%) mkdir %MENU_DIR%

copy %RECIPE_DIR%\navigator.ico %MENU_DIR%\anaconda-navigator.ico
if errorlevel 1 exit 1

copy %RECIPE_DIR%\menu-windows.json %MENU_DIR%\navigator_shortcut.json
if errorlevel 1 exit 1
