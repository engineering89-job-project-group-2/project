from flask import *
import numpy as np
from list_function import display_table_rank
import pandas as pd

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/")
def index(): # homepage
    return render_template("homepage.html")


data = pd.read_csv("data.csv") #importing a csv as a dataframe to test functionality


@app.route("/list", methods=["GET", "POST"])
def list():
    result = display_table_rank(data)
    return render_template("list_page.html").format(result=result)