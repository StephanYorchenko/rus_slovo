from flask import render_template
from flask_login import login_required


@login_required
def main():
    return render_template("main.html")

