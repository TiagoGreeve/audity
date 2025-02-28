#!/bin/bash
cd /d/gitRepos/tiago/audity
pyinstaller src/main.py --onedir --name audio_player --icon resources/logo.ico --noconsole
