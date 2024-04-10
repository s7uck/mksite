#!/usr/bin/python3

import os
import argparse
import shutil
from enum import Enum

home="~"
templates_dir=os.popen("xdg-user-dir TEMPLATES").read().strip()
code_folder="~/Codice"
sitesfolder=os.path.join(code_folder, "Siti Web")

class SiteType(Enum):
    static="static"
    jekyll="jekyll"
    express="express"

    def __str__(self):
        return self.value

    def makeNew(self):
        return {
            "static": Site,
            "jekyll": JekyllSite,
            "express": ExpressApp}[self.value]

parser = argparse.ArgumentParser(description="Website folder creator tool")

parser.add_argument('name', type=str, help="the website's name")
parser.add_argument('--type', type=SiteType, default=SiteType.static, help="type of website (available options: static, jekyll, express)")
parser.add_argument('--description', type=str, help="site description (optional))")
parser.add_argument('--url', type=str, help="site url (optional))")
parser.add_argument('--lang', type=str, default="en", help="site language (default: en))")
parser.add_argument('--email', type=str, help="site email (optional))")
parser.add_argument('--sites_dir', type=str, default=".", help="directory to create the website (default: .)")
parser.add_argument('--template_dir', type=str, help="template dir (default: xdg TEMPLATES dir)")

args = parser.parse_args()

if args.template_dir:
    templates_dir=args.template_dir
if args.sites_dir:
    sitesfolder=args.sites_dir

class Site:
    template=f"{templates_dir}/Sito"
    build_commands=[]
    preview_commands=[]
    static=True

    def __init__(self, name, parent_dir):
        self.name = name
        self.path = os.path.join(parent_dir, name)
        self.index_file = os.path.join(self.path, "index.html")
        shutil.copytree(self.template, self.path)
        os.chdir(self.path)
        for command in self.build_commands:
            os.system(command)

    def subst(self, title, description="", url="", lang="", email=""):
        with open(self.index_file, 'r') as file:
            filedata = file.read()
        filedata = filedata.format(title, description, lang=lang)
        with open(self.index_file, 'w') as file:
            file.write(filedata)

    def preview(self):
        if preview_commands == []:
            os.system(f'xdg-open {self.index_file}')
        else:
            for command in self.preview_commands:
                os.system(command)

class JekyllSite(Site):
    template=f"{templates_dir}/Sito Jekyll"
    build_commands=["jekyll build"]
    preview_commands=["jekyll s"]
    static=True

class ExpressApp(Site):
    template=f"{templates_dir}/App Express"
    build_commands=["npm i"]
    preview_commands=["PORT=8080 npm start"]
    static=False


if args.name:
    try:
        print(f"Creating site {args.name} in {sitesfolder}...")
        site = args.type.makeNew()(args.name, sitesfolder)
    except FileExistsError:
        print(f"{sitesfolder}/{args.name} already exists")
        exit()

    description = args.description or input("Description (leave empty to skip): ")
    url = args.url or input("URL (leave empty to skip): ")
    email = args.url or input("Email (leave empty to skip): ")

    site.subst(args.name, description=description, url=url, lang=args.lang, email=email)
