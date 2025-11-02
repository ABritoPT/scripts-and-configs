@echo off 
set drives=D L S Z
(for %%a in (%drives%) do ( 
   echo %%a 
   dir %%a:\ /s /b /o:gn > %%a.txt
))