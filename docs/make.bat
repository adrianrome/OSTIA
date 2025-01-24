@ECHO OFF
REM Disables command echoing to keep the output clean.

pushd %~dp0
REM Changes the current directory to the script's directory. This ensures that 
REM the script runs relative to its own location, regardless of where it is executed from.

REM Command file for Sphinx documentation.

if "%SPHINXBUILD%" == "" (
    REM Checks if the SPHINXBUILD environment variable is not set.
    REM If not set, assigns the default value 'sphinx-build'.
    set SPHINXBUILD=sphinx-build
)

REM Sets the source and build directories for Sphinx.
set SOURCEDIR=source  REM The directory where the source files for Sphinx are located.
set BUILDDIR=build    REM The directory where the build output will be generated.

REM Test if the sphinx-build command is available.
%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
    REM If the sphinx-build command is not found, display a help message.
    echo.
    echo. The 'sphinx-build' command was not found. Make sure you have Sphinx
    echo. installed, then set the SPHINXBUILD environment variable to point
    echo. to the full path of the 'sphinx-build' executable. Alternatively you
    echo. may add the Sphinx directory to PATH.
    echo.
    echo. If you don't have Sphinx installed, grab it from
    echo. https://www.sphinx-doc.org/
    exit /b 1
    REM Exits the script with error code 1 if sphinx-build is unavailable.
)

if "%1" == "" goto help
REM If no argument is provided, jumps to the ':help' section to display usage information.

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
REM Executes the Sphinx build command with the provided target (%1) and the source 
REM and build directories. Additional Sphinx options (%SPHINXOPTS% and %O%) are appended.

goto end
REM Skips to the ':end' section after running the main command.

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
REM Displays help information for Sphinx targets using the -M help option.

:end
popd
REM Restores the previous directory that was active before the script started.
