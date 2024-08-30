#!/bin/bash
cd ..
pyinstaller src/main.py --onedir --name audio_player --icon resources/logo.ico --noconsole
