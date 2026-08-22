# coding: utf-8

import pandas as pd

from md_utils import build_filenames, render_talk


talks = pd.read_csv("talks.tsv", sep="\t", header=0)

for row, item in talks.iterrows():
    md_filename, _ = build_filenames(item.date, item.url_slug)
    with open("../_talks/" + md_filename, "w") as f:
        f.write(render_talk(item))
