REM
REM Script to build a one file exe for BRIT
REM

REM To run this, make sure pyinstaller is installed on your system.
REM This should be possible with 
REM  python -m  pip install pyinstaller
REM

SET OSG_BAT=e:\QGIS_Dev\QGIS\OSGeo4W.bat

SET SCRIPT_DIR=%~dp0

cd /D %SCRIPT_DIR%

%OSG_BAT% pyinstaller -F --add-data ui\*;ui --windowed brit.py

