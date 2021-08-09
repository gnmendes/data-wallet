from flask import Flask, request, jsonify
from flask_cors import cross_origin

app = Flask(__name__)

from src.controller import *
