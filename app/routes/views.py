from flask import Blueprint, render_template, request, redirect
import os
# from app import app, db

views_bp = Blueprint('views', __name__)
@views_bp.route('/')
def index():
    return render_template("base.html")