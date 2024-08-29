import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Optimize Streamlit configuration
st.set_page_config(layout="wide")

@st.cache_data
def app():
    st.title("Dashboard | Financial Analytics")
    st.write("Link to GitHub repo: [https://github.com/brukGit/tenx-w1/tree/task-2](https://github.com/brukGit/tenx-w1/tree/task-2)")

    # Create three columns
    left_column, middle_column, right_column = st.columns([1, 2, 2])

       
if __name__ == "__main__":
    app()
