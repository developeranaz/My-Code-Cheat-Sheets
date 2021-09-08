import streamlit as st
import time
import numpy as np
import os

os.system('echo "1" >num')
progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
for i in range(1, 101):
    i = open("num", "r")
    os.system('expr 1 + $(cat num) >num')
    status_text.text("%i%% Complete" % i)
    progress_bar.progress(i)
    last_rows = new_rows
    

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
