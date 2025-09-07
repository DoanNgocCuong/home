import pandas as pd
import pygwalker as pyg
import os

# Check if file exists
if not os.path.exists('advertising.csv'):
    print("Error: advertising.csv file not found!")
    print("Please make sure the file exists in the same directory as app.py")
    exit(1)

# Read data
df = pd.read_csv('advertising.csv')

# Create PygWalker application
walker = pyg.walk(df, port=8081)