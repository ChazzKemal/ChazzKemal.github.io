"""Pure helpers for the markdown generator scripts."""

import html
import os
import re
from time import strptime


HTML_ESCAPE_TABLE = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
}


def html_escape(text):
    """Produce entities within text."""
    return "".join(HTML_ESCAPE_TABLE.get(c, c) for c in text)


def html_escape_talk(text):
    """Escape talk text, retaining the original non-string behavior."""
    if type(text) is str:
        return html_escape(text)
    return "False"


def bibtex_pub_date(fields):
    """Build a publication date using the BibTeX generator's defaults."""
    pub_year = f'{fields.get("year", "1900")}'
    pub_month = "01"
    pub_day = "01"

    if "month" in fields:
        month = fields["month"]
        if isinstance(month, int):
            pub_month = f"{month:02d}"
        elif isinstance(month, str) and month.isdigit():
            pub_month = f"{int(month):02d}"
        elif len(month) < 3:
            pub_month = ("0" + month)[-2:]
        else:
            pub_month = "{:02d}".format(strptime(month[:3], "%b").tm_mon)

    if "day" in fields:
        pub_day = str(fields["day"])

    return pub_year + "-" + pub_month + "-" + pub_day


def strip_bibtex_formatting(title):
    """Remove BibTeX formatting characters while preserving spaces."""
    return title.replace("{", "").replace("}", "").replace("\\", "")


def clean_bibtex_title(title):
    """Prepare a BibTeX title for a filename and URL slug."""
    return strip_bibtex_formatting(title).replace(" ", "-")


def bibtex_url_slug(title):
    """Create the URL slug used by the BibTeX generator."""
    clean_title = clean_bibtex_title(title)
    url_slug = re.sub(r"\[.*\]|[^a-zA-Z0-9_-]", "", clean_title)
    return url_slug.replace("--", "-")


def build_filenames(pub_date, url_slug, collapse_double_dash=False):
    """Return markdown and HTML filenames for a generated item."""
    md_filename = str(pub_date) + "-" + url_slug + ".md"
    html_filename = str(pub_date) + "-" + url_slug
    if collapse_double_dash:
        md_filename = md_filename.replace("--", "-")
        html_filename = html_filename.replace("--", "-")
    return os.path.basename(md_filename), html_filename


def build_bibtex_citation(authors, title, venue, year):
    """Build a citation from BibTeX authors and fields."""
    citation = ""
    for author in authors:
        citation += " " + author.first_names[0] + " " + author.last_names[0] + ", "
    citation += '"' + html_escape(strip_bibtex_formatting(title)) + '."'
    citation += " " + html_escape(strip_bibtex_formatting(venue))
    citation += ", " + str(year) + "."
    return citation


def _field(row, name):
    if isinstance(row, dict):
        return row[name]
    return getattr(row, name)


def render_publication(row):
    """Render one publications.tsv row."""
    pub_date = _field(row, "pub_date")
    title = _field(row, "title")
    venue = _field(row, "venue")
    excerpt = _field(row, "excerpt")
    citation = _field(row, "citation")
    paper_url = _field(row, "paper_url")

    md = "---\ntitle: \"" + title + '"\n'
    md += "collection: publications"
    md += "\npermalink: /publication/" + str(pub_date) + "-" + _field(row, "url_slug")

    if len(str(excerpt)) > 5:
        md += "\nexcerpt: '" + html_escape(excerpt) + "'"

    md += "\ndate: " + str(pub_date)
    md += "\nvenue: '" + html_escape(venue) + "'"

    if len(str(paper_url)) > 5:
        md += "\npaperurl: '" + paper_url + "'"

    md += "\ncitation: '" + html_escape(citation) + "'"
    md += "\n---"

    if len(str(paper_url)) > 5:
        md += "\n\n<a href='" + paper_url + "'>Download paper here</a>\n"

    if len(str(excerpt)) > 5:
        md += "\n" + html_escape(excerpt) + "\n"

    md += "\nRecommended citation: " + citation
    return md


def render_talk(row):
    """Render one talks.tsv row."""
    title = _field(row, "title")
    talk_type = _field(row, "type")
    url_slug = _field(row, "url_slug")
    venue = _field(row, "venue")
    date = _field(row, "date")
    location = _field(row, "location")
    talk_url = _field(row, "talk_url")
    description = _field(row, "description")

    md = "---\ntitle: \"" + title + '"\n'
    md += "collection: talks\n"

    if len(str(talk_type)) > 3:
        md += 'type: "' + talk_type + '"\n'
    else:
        md += 'type: "Talk"\n'

    md += "permalink: /talks/" + str(date) + "-" + url_slug + "\n"

    if len(str(venue)) > 3:
        md += 'venue: "' + venue + '"\n'

    if len(str(location)) > 3:
        md += "date: " + str(date) + "\n"

    if len(str(location)) > 3:
        md += 'location: "' + str(location) + '"\n'

    md += "---\n"

    if len(str(talk_url)) > 3:
        md += "\n[More information here](" + talk_url + ")\n"

    if len(str(description)) > 3:
        md += "\n" + html_escape_talk(description) + "\n"

    return md


def render_bibtex_entry(
    fields,
    authors,
    venue_pretext,
    venue_key,
    collection_name,
    collection_permalink,
    pub_date,
    html_filename,
):
    """Render one BibTeX entry."""
    title = strip_bibtex_formatting(fields["title"])
    venue = venue_pretext + strip_bibtex_formatting(fields[venue_key])
    citation = build_bibtex_citation(authors, fields["title"], venue, fields["year"])

    md = '---\ntitle: "' + html_escape(title) + '"\n'
    md += "collection: " + collection_name
    md += "\npermalink: " + collection_permalink + html_filename

    note = False
    if "note" in fields and len(str(fields["note"])) > 5:
        md += "\nexcerpt: '" + html_escape(fields["note"]) + "'"
        note = True

    md += "\ndate: " + str(pub_date)
    md += "\nvenue: '" + html_escape(venue) + "'"

    url = False
    if "url" in fields and len(str(fields["url"])) > 5:
        md += "\npaperurl: '" + fields["url"] + "'"
        url = True

    md += "\ncitation: '" + html_escape(citation) + "'"
    md += "\n---"

    if note:
        md += "\n" + html_escape(fields["note"]) + "\n"

    if url:
        md += '\n[Access paper here](' + fields["url"] + '){:target="_blank"}\n'
    else:
        scholar_title = clean_bibtex_title(fields["title"]).replace("-", "+")
        md += (
            "\nUse [Google Scholar](https://scholar.google.com/scholar?q="
            + html.escape(scholar_title)
            + '){:target="_blank"} for full citation'
        )

    return md
