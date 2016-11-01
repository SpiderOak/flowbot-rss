from jinja2 import Environment, FileSystemLoader
import os


ENV = Environment(
    loader=FileSystemLoader('%s/templates/' % os.path.dirname(__file__))
)
