#! /usr/bin/env python3

from distutils.core import setup

setup (
    name="gkrcmd",
    version="0.1",
    description="Command line tool to access the gnome-keyring",
    author="Juan Tascón",
    author_email="juantascon@gmail.com",
    maintainer="Juan Tascón",
    maintainer_email="juantascon@gmail.com",
    url="https://sourceforge.net/projects/gkrcmd/",
    keywords=["gkrcmd", "gnomekeyring", "cli", "gnome", "keyring"],
    
    packages=["gkrcmd"],
    scripts=["script/gkrcmd"],
    data_files=[("share/gkrcmd", ["README", "LICENSE", "TODO"])],
    
    license="GPL, Version 3.0"
    )
