@echo off

del /q report\*
del /q workdir\*

if "%1" == "full" (
    rmdir __pycache__ /s /q
    rmdir workdir /s /q
    rmdir report /s /q
)