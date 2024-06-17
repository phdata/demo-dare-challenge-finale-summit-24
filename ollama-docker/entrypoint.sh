#!/bin/bash
nohup python -m streamlit run /src/app/main.py > streamlit.out 2>streamlit.err&
nohup jupyter lab --no-browser --allow-root --ip=0.0.0.0 --NotebookApp.token='' --NotebookApp.password=''&
wait
