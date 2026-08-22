from types import SimpleNamespace

import pytest

from md_utils import (
    bibtex_pub_date,
    bibtex_url_slug,
    build_bibtex_citation,
    build_filenames,
    clean_bibtex_title,
    html_escape,
    html_escape_talk,
    render_bibtex_entry,
    render_publication,
    render_talk,
    strip_bibtex_formatting,
)


def test_html_escape_special_characters():
    assert html_escape("""A & "quoted" 'value'""") == "A &amp; &quot;quoted&quot; &apos;value&apos;"


def test_html_escape_non_string_raises():
    with pytest.raises(TypeError):
        html_escape(42)


def test_talk_html_escape_preserves_non_string_quirk():
    assert html_escape_talk(42) == "False"
    assert html_escape_talk("A & 'value'") == "A &amp; &apos;value&apos;"


@pytest.mark.parametrize(
    ("fields", "expected"),
    [
        ({"year": "2024", "month": "1", "day": "2"}, "2024-01-2"),
        ({"year": "2024", "month": "12"}, "2024-12-01"),
        ({"year": "2024", "month": "Jan"}, "2024-01-01"),
        ({"year": "2024", "month": "September"}, "2024-09-01"),
        ({"year": "2024", "month": "M"}, "2024-0M-01"),
        ({"year": "2024", "month": 3}, "2024-03-01"),
        ({"year": "2024"}, "2024-01-01"),
    ],
)
def test_bibtex_pub_date_normalizes_months_and_missing_fields(fields, expected):
    assert bibtex_pub_date(fields) == expected


def test_bibtex_pub_date_requires_year():
    with pytest.raises(KeyError):
        bibtex_pub_date({})


def test_bibtex_title_cleaning_and_slug():
    title = r"{A} {B}\: A  Study [remove this] -- Test!"
    assert strip_bibtex_formatting(title) == "A B: A  Study [remove this] -- Test!"
    assert clean_bibtex_title(title) == "A-B:-A--Study-[remove-this]----Test!"
    assert bibtex_url_slug(title) == "A-B-A-Study---Test"


def test_filename_construction_and_double_dash_collapse():
    assert build_filenames("2024-03-01", "a--b") == (
        "2024-03-01-a--b.md",
        "2024-03-01-a--b",
    )
    assert build_filenames("2024-03-01", "a--b", collapse_double_dash=True) == (
        "2024-03-01-a-b.md",
        "2024-03-01-a-b",
    )


def test_bibtex_citation_with_multiple_authors():
    authors = [
        SimpleNamespace(first_names=["Ada"], last_names=["Lovelace"]),
        SimpleNamespace(first_names=["Grace"], last_names=["Hopper"]),
    ]
    assert build_bibtex_citation(
        authors, r"{A} title", r"{Journal} & Venue", "2024"
    ) == ' Ada Lovelace,  Grace Hopper, "A title." Journal &amp; Venue, 2024.'


def test_publication_renderer_with_excerpt_and_paper_url():
    row = {
        "pub_date": "2024-01-02",
        "title": "A publication",
        "venue": "A & venue",
        "excerpt": "An excerpt",
        "citation": 'Author, "A publication".',
        "url_slug": "a-publication",
        "paper_url": "https://example.test/paper.pdf",
    }
    assert render_publication(row) == (
        '---\ntitle: "A publication"\n'
        "collection: publications\n"
        "permalink: /publication/2024-01-02-a-publication\n"
        "excerpt: 'An excerpt'\n"
        "date: 2024-01-02\n"
        "venue: 'A &amp; venue'\n"
        "paperurl: 'https://example.test/paper.pdf'\n"
        "citation: 'Author, &quot;A publication&quot;.'\n"
        "---\n\n"
        "<a href='https://example.test/paper.pdf'>Download paper here</a>\n\n"
        "An excerpt\n\n"
        'Recommended citation: Author, "A publication".'
    )


def test_publication_renderer_without_excerpt_and_paper_url():
    row = {
        "pub_date": "2024-01-02",
        "title": "A publication",
        "venue": "Venue",
        "excerpt": "",
        "citation": "Author citation",
        "url_slug": "a-publication",
        "paper_url": "",
    }
    assert render_publication(row) == (
        '---\ntitle: "A publication"\n'
        "collection: publications\n"
        "permalink: /publication/2024-01-02-a-publication\n"
        "date: 2024-01-02\n"
        "venue: 'Venue'\n"
        "citation: 'Author citation'\n"
        "---\n"
        "Recommended citation: Author citation"
    )


def test_publication_renderer_accepts_row_objects():
    row = SimpleNamespace(
        pub_date="2024-01-02",
        title="A publication",
        venue="Venue",
        excerpt="",
        citation="Author citation",
        url_slug="a-publication",
        paper_url="",
    )
    assert render_publication(row) == render_publication(vars(row))


def test_talk_renderer_with_all_optional_fields():
    row = {
        "title": "A talk",
        "type": "Workshop",
        "url_slug": "a-talk",
        "venue": "A venue",
        "date": "2024-01-02",
        "location": "A location",
        "talk_url": "https://example.test/talk",
        "description": "A & description",
    }
    assert render_talk(row) == (
        '---\ntitle: "A talk"\n'
        "collection: talks\n"
        'type: "Workshop"\n'
        "permalink: /talks/2024-01-02-a-talk\n"
        'venue: "A venue"\n'
        "date: 2024-01-02\n"
        'location: "A location"\n'
        "---\n\n"
        "[More information here](https://example.test/talk)\n\n"
        "A &amp; description\n"
    )


def test_talk_renderer_with_blank_optional_fields():
    row = {
        "title": "A talk",
        "type": "",
        "url_slug": "a-talk",
        "venue": "",
        "date": "2024-01-02",
        "location": "",
        "talk_url": "",
        "description": "",
    }
    assert render_talk(row) == (
        '---\ntitle: "A talk"\n'
        "collection: talks\n"
        'type: "Talk"\n'
        "permalink: /talks/2024-01-02-a-talk\n"
        "---\n"
    )


def test_bibtex_renderer_with_note_and_url():
    fields = {
        "title": r"{A} Study \& Results",
        "year": "2024",
        "journal": "Journal & Venue",
        "note": "A useful note",
        "url": "https://example.test/paper",
    }
    authors = [SimpleNamespace(first_names=["Ada"], last_names=["Lovelace"])]
    assert render_bibtex_entry(
        fields,
        authors,
        "",
        "journal",
        "publications",
        "/publication/",
        "2024-03-02",
        "2024-03-02-A-Study-&-Results",
    ) == (
        '---\ntitle: "A Study &amp; Results"\n'
        "collection: publications\n"
        "permalink: /publication/2024-03-02-A-Study-&-Results\n"
        "excerpt: 'A useful note'\n"
        "date: 2024-03-02\n"
        "venue: 'Journal &amp; Venue'\n"
        "paperurl: 'https://example.test/paper'\n"
        "citation: ' Ada Lovelace, &quot;A Study &amp;amp; Results.&quot; "
        "Journal &amp;amp; Venue, 2024.'\n"
        "---\n"
        "A useful note\n\n"
        '[Access paper here](https://example.test/paper){:target="_blank"}\n'
    )


def test_bibtex_renderer_without_note_and_url_uses_google_scholar():
    fields = {
        "title": r"{A} title: one",
        "year": "2024",
        "booktitle": "Conference",
    }
    authors = [SimpleNamespace(first_names=["Grace"], last_names=["Hopper"])]
    assert render_bibtex_entry(
        fields,
        authors,
        "In the proceedings of ",
        "booktitle",
        "publications",
        "/publication/",
        "2024-01-01",
        "2024-01-01-A-title-one",
    ) == (
        '---\ntitle: "A title: one"\n'
        "collection: publications\n"
        "permalink: /publication/2024-01-01-A-title-one\n"
        "date: 2024-01-01\n"
        "venue: 'In the proceedings of Conference'\n"
        "citation: ' Grace Hopper, &quot;A title: one.&quot; "
        "In the proceedings of Conference, 2024.'\n"
        "---\n"
        "Use [Google Scholar](https://scholar.google.com/scholar?q="
        "A+title:+one){:target=\"_blank\"} for full citation"
    )
