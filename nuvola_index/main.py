import json
import os
from argparse import ArgumentParser, Namespace
from typing import List

from fxwebgen.templater import create_templater
from . import Generator


def main(argv: List[str]) -> int:
    params = parse_args(argv)
    with open(params.globals) as f:
        global_vars = json.load(f)
    with open(params.apps) as f:
        apps = json.load(f)
        apps.sort(key=lambda item: item["name"].lower())
    with open(params.distributions) as f:
        distributions = json.load(f)
    with open(params.team) as f:
        team = json.load(f)
    output = os.path.abspath(params.output)
    templates = os.path.abspath(params.templates)
    global_vars["root"] = params.hostname.rstrip("/")
    templater = create_templater(templates, global_vars)
    static = [os.path.abspath(path) for path in params.static]
    generator = Generator(distributions, apps, team, output, static, templater, params.pages)
    if params.fresh:
        generator.purge()
    generator.build()
    return 0


def parse_args(argv: List[str]) -> Namespace:
    parser = ArgumentParser(prog=argv[0])
    parser.add_argument(
        "-g", "--globals", default="data/globals.json",
        help="Path to global template variables [data/globals.json].")
    parser.add_argument(
        "-d", "--distributions", default="data/distributions.json",
        help="Path to information about distributions [data/distributions.json].")
    parser.add_argument(
        "-a", "--apps", default="data/apps.json",
        help="Path to information about apps [data/apps.json].")
    parser.add_argument(
        "--team", default="data/team.json",
        help="Path to information about the team [data/team.json].")
    parser.add_argument(
        "--pages", default="pages",
        help="Path to a directory with Markdown pages [pages].")
    parser.add_argument(
        "-o", "--output", default="build",
        help="Path to output directory [build].")
    parser.add_argument(
        "-t", "--templates", default="templates",
        help="Path to templates directory [templates].")
    parser.add_argument(
        "-s", "--static", default=["static", "screenshots"], nargs='*',
        help="Path to static files directory [static, screenshots].")
    parser.add_argument(
        "-f", "--fresh", action="store_true", default=False,
        help="Start with a fresh build directory.")
    parser.add_argument(
        "hostname",
        help="Absolute address of server root, e.g. 'https://nuvola.tiliado.eu/' or 'http://127.0.0.1:8000/'.")
    return parser.parse_args(argv[1:])
