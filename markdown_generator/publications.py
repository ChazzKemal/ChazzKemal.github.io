# coding: utf-8

import pandas as pd

from md_utils import build_filenames, render_publication


publications = pd.read_csv("publications.tsv", sep="\t", header=0)

for row, item in publications.iterrows():
    md_filename, _ = build_filenames(item.pub_date, item.url_slug)
    with open("../_publications/" + md_filename, "w") as f:
        f.write(render_publication(item))
