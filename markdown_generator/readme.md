# Markdown generator

The scripts in this directory convert structured publication and talk data into
Markdown files for the academicpages template. Run them from this directory;
they expect the input files in the current working directory and write output
one directory above it:

* `publications.py` reads `publications.tsv` and writes to `../_publications/`.
* `talks.py` reads `talks.tsv` and writes to `../_talks/`.
* `pubsFromBib.py` reads `proceedings.bib` and `pubs.bib` and writes to
  `../_publications/`.

## TSV input

`publications.tsv` must include the columns `pub_date`, `title`, `venue`,
`excerpt`, `citation`, `url_slug`, and `paper_url`. The `pub_date` must use
`YYYY-MM-DD`; `title`, `venue`, `citation`, and `url_slug` are required.
`excerpt` and `paper_url` may be blank. The date and `url_slug` form the
generated filename (`YYYY-MM-DD-[url_slug].md`) and publication permalink.

`talks.tsv` must include `title`, `type`, `url_slug`, `venue`, `date`,
`location`, `talk_url`, and `description`. `title`, `url_slug`, and `date` are
required, with `date` in `YYYY-MM-DD` format. The other fields may be blank;
blank `type` defaults to `Talk`. The date and `url_slug` form the generated
filename (`YYYY-MM-DD-[url_slug].md`) and talk permalink.

## BibTeX input

`pubsFromBib.py` expects BibTeX entries with `author`, `title`, `year`, and the
venue field appropriate to the source file: `journal` in `pubs.bib` or
`booktitle` in `proceedings.bib`. `month` and `day` are optional and default to
`01`; `note` and `url` are optional. Missing required fields cause that entry
to be warned about and skipped. BibTeX titles are cleaned for generated
filenames and slugs by removing braces and backslashes and converting spaces
to dashes.
