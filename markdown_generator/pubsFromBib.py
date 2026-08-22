#!/usr/bin/env python
# coding: utf-8

from pybtex.database.input import bibtex
import pybtex.database.input.bibtex
import os

from md_utils import (
    bibtex_pub_date,
    bibtex_url_slug,
    build_filenames,
    render_bibtex_entry,
)


publist = {
    "proceeding": {
        "file": "proceedings.bib",
        "venuekey": "booktitle",
        "venue-pretext": "In the proceedings of ",
        "collection": {"name": "publications", "permalink": "/publication/"},
    },
    "journal": {
        "file": "pubs.bib",
        "venuekey": "journal",
        "venue-pretext": "",
        "collection": {"name": "publications", "permalink": "/publication/"},
    },
}


for pubsource in publist:
    parser = bibtex.Parser()
    bibdata = parser.parse_file(publist[pubsource]["file"])

    for bib_id in bibdata.entries:
        b = bibdata.entries[bib_id].fields

        try:
            pub_date = bibtex_pub_date(b)
            url_slug = bibtex_url_slug(b["title"])
            md_filename, html_filename = build_filenames(
                pub_date, url_slug, collapse_double_dash=True
            )
            md = render_bibtex_entry(
                b,
                bibdata.entries[bib_id].persons["author"],
                publist[pubsource]["venue-pretext"],
                publist[pubsource]["venuekey"],
                publist[pubsource]["collection"]["name"],
                publist[pubsource]["collection"]["permalink"],
                pub_date,
                html_filename,
            )

            with open("../_publications/" + os.path.basename(md_filename), "w") as f:
                f.write(md)
            print(
                f'SUCESSFULLY PARSED {bib_id}: "',
                b["title"][:60],
                "..." * (len(b["title"]) > 60),
                '"',
            )
        except KeyError as e:
            print(
                f'WARNING Missing Expected Field {e} from entry {bib_id}: "',
                b["title"][:30],
                "..." * (len(b["title"]) > 30),
                '"',
            )
            continue
