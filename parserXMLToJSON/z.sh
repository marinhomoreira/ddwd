#!/bin/bash
clear
echo 'Deleting temp files...'
find . -name '*.temp' -delete
echo 'Deleting previous master files...'
rm masterfiles/*
echo 'Go go Python!'
python xmlToJson.py ~/Desktop/ianode/ImagineCup/test ~/Desktop/ianode/ImagineCup/masterfiles
echo 'Deleting temp files'
find . -name '*.temp' -delete
echo 'And the master files are...'
ls masterfiles/
