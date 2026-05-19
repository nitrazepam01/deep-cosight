import json
import os
import sys

sys.path.insert(0, os.path.abspath("."))

from app.cosight.tool.wikipedia_toolkit import (
    WikipediaToolkit,
    _RenderedReferenceCounter,
    _RevisionTableParser,
)


def test_rendered_reference_counter_separates_list_items_from_callouts():
    html = """
    <p>A<sup class="reference">[1]</sup>B<sup class="reference">[1]</sup></p>
    <ol class="references">
      <li id="cite_note-alpha-1"><span class="mw-reference-text">Alpha</span></li>
      <li id="cite_note-beta-2"><span class="mw-reference-text">Beta</span></li>
    </ol>
    """

    counts = _RenderedReferenceCounter.count(html)

    assert counts["reference_list_items"] == 2
    assert counts["reference_text_spans"] == 2
    assert counts["citation_callouts"] == 2


def test_raw_ref_counter_subtracts_named_self_closing_reuses():
    wikitext = """
    First<ref name="a">A</ref>
    Second<ref name="a" />
    Third<ref>B</ref>
    Fourth<ref name=b/>
    Fifth<ref name="c">{{cite web|title=C}}</ref>
    """

    counts = WikipediaToolkit._count_raw_ref_tags(wikitext)

    assert counts["raw_ref_openings"] == 5
    assert counts["raw_named_self_closing_reuses"] == 2
    assert counts["raw_reference_definitions_after_reuse_adjustment"] == 3


def test_reference_count_prefers_unique_rendered_items_over_callouts():
    class FakeToolkit(WikipediaToolkit):
        def _parse_html(self, oldid, language, section=None, site=""):
            return '<p><sup class="reference">[1]</sup><sup class="reference">[1]</sup></p>'

        def _render_html(self, oldid, title, language, site=""):
            return """
            <ol class="references">
              <li id="cite_note-a-1"><span class="mw-reference-text">A</span></li>
            </ol>
            <p><sup class="reference">[1]</sup><sup class="reference">[1]</sup></p>
            """

        def _raw_revision_dict(self, oldid, language, site=""):
            return {
                "title": "Example",
                "timestamp": "2026-01-01T00:00:00Z",
                "wikitext": '<ref name="a">A</ref><ref name="a" />',
            }

    result = FakeToolkit()._reference_count_dict(123, "Example", "en")

    assert result["recommended_count"] == 1
    assert result["rendered_reference_list_items"] == 1
    assert result["citation_callouts"] == 2
    assert result["recommended_count_method"] == "rendered_reference_list_items"
    assert any("citation_callouts" in warning for warning in result["warnings"])


def test_mediawiki_query_can_select_interval_revisions_and_return_reference_evidence():
    class FakeToolkit(WikipediaToolkit):
        def _first_revision_in_interval_dict(self, title, start_timestamp, end_timestamp, language, site=""):
            is_2025 = start_timestamp.startswith("2025-")
            return {
                "title": title,
                "pageid": 12345,
                "start_timestamp": start_timestamp,
                "end_timestamp": end_timestamp,
                "oldid": 1001 if is_2025 else 2001,
                "timestamp": "2025-01-26T19:21:08Z" if is_2025 else "2026-01-19T00:12:33Z",
                "size": 80487 if is_2025 else 82330,
                "url": f"https://en.wikipedia.org/w/index.php?title={title}&oldid={'1001' if is_2025 else '2001'}",
            }

        def _reference_count_dict(self, oldid, title, language, include_raw_ref_check=True, site=""):
            return {
                "oldid": oldid,
                "title": title,
                "recommended_count": 12 if int(oldid) == 1001 else 16,
                "recommended_count_method": "rendered_reference_list_items",
                "citation_callouts": 14 if int(oldid) == 1001 else 18,
            }

    toolkit = FakeToolkit()
    earlier = json.loads(
        toolkit.mediawiki_evidence_query(
            title="Example Page",
            revision={
                "mode": "first_in_interval",
                "start_timestamp": "2025-01-01T00:00:00Z",
                "end_timestamp": "2026-01-01T00:00:00Z",
            },
            include=["metadata", "references"],
        )
    )
    later = json.loads(
        toolkit.mediawiki_evidence_query(
            title="Example Page",
            revision={
                "mode": "first_in_interval",
                "start_timestamp": "2026-01-01T00:00:00Z",
                "end_timestamp": "2027-01-01T00:00:00Z",
            },
            include=["metadata", "references"],
        )
    )

    assert earlier["revision"]["oldid"] == 1001
    assert later["revision"]["oldid"] == 2001
    assert earlier["counts"]["reference_count"] == 12
    assert later["counts"]["reference_count"] == 16
    assert later["counts"]["reference_count"] - earlier["counts"]["reference_count"] == 4


def test_mediawiki_query_picks_last_revision_before_cutoff():
    class FakeToolkit(WikipediaToolkit):
        def _get_json(self, language, params, site=""):
            assert params["rvdir"] == "older"
            return {
                "query": {
                    "pages": [
                        {
                            "title": "Example",
                            "pageid": 123,
                            "revisions": [
                                {"revid": 200, "timestamp": "2023-08-01T00:00:00Z", "size": 10},
                                {"revid": 199, "timestamp": "2023-07-24T11:28:06Z", "size": 9},
                            ],
                        }
                    ]
                }
            }

    result = json.loads(
        FakeToolkit().mediawiki_evidence_query(
            title="Example",
            revision={"mode": "last_before", "cutoff_timestamp": "2023-08-01T00:00:00Z"},
            include=["metadata"],
        )
    )

    assert result["revision"]["oldid"] == 199
    assert result["revision"]["timestamp"] == "2023-07-24T11:28:06Z"


def test_mediawiki_query_history_interval_can_annotate_adjacent_size_deltas():
    class FakeToolkit(WikipediaToolkit):
        def _revision_size_history(self, title, start_timestamp, end_timestamp, language, site=""):
            return {
                "page": {"title": title, "pageid": 123},
                "revisions": [
                    {"revid": 10, "timestamp": "2025-01-01T00:00:00Z", "size": 1000},
                    {"revid": 11, "timestamp": "2025-02-01T00:00:00Z", "size": 1100},
                    {"revid": 12, "timestamp": "2025-03-01T00:00:00Z", "size": 1989},
                    {"revid": 13, "timestamp": "2025-04-01T00:00:00Z", "size": 2000},
                ],
            }

    result = json.loads(
        FakeToolkit().mediawiki_evidence_query(
            title="Example",
            revision={"mode": "history_interval", "year": 2025},
            include=["revision_history"],
            history_metrics={"with_size_deltas": True, "match_delta": 889},
        )
    )

    history = result["revision_history"]
    assert result["counts"]["revision_count"] == 4
    assert result["counts"]["history_delta_match_count"] == 1
    assert history["matched_revision"]["oldid"] == 12
    assert history["matched_revision"]["parent_oldid"] == 11
    assert history["matched_revision"]["calculation"] == "1989 - 1100 = 889"
    assert history["matched_revision"]["formatted_date"] == "2025/03/01"


def test_revision_table_parser_preserves_links():
    html = """
    <table class="wikitable">
      <tr><th>Place</th><th>Related items</th></tr>
      <tr>
        <td>New York</td>
        <td><a href="/wiki/Maple_Leaf_(train)" title="Maple Leaf (train)">Maple Leaf</a></td>
      </tr>
    </table>
    """

    tables = _RevisionTableParser.parse(html)

    assert len(tables) == 1
    assert tables[0]["rows"][1][1]["text"] == "Maple Leaf"
    assert tables[0]["rows"][1][1]["links"][0]["title"] == "Maple Leaf (train)"


def test_mediawiki_query_table_counting_is_pattern_driven_and_deduplicated():
    class FakeToolkit(WikipediaToolkit):
        def _raw_revision_dict(self, oldid, language, site=""):
            return {
                "title": "Example",
                "pageid": 456,
                "oldid": int(oldid),
                "timestamp": "2023-07-24T11:28:06Z",
                "size": 100,
                "wikitext": "",
            }

        def _section_index_for_keyword(self, oldid, language, section_keyword, site=""):
            return "3"

        def _parse_html(self, oldid, language, section=None, site=""):
            return """
            <table class="wikitable">
              <tr><th>Place</th><th>Related items</th></tr>
              <tr>
                <td>A</td>
                <td>
                  <a title="Maple Leaf (train)">Maple Leaf</a>;
                  <a title="Lake Shore Limited">Lake Shore Limited</a>;
                  <a title="Maple Leaf (train)">Maple Leaf</a>;
                  <a title="Metro Subway">Metro Subway</a>
                </td>
              </tr>
            </table>
            """

    result = json.loads(
        FakeToolkit().mediawiki_evidence_query(
            title="Example",
            revision={"mode": "oldid", "oldid": 1166890780},
            include=["tables"],
            extract={"section_keywords": ["Route"], "table_keywords": ["Related items"]},
            counting={
                "dedupe_by": "link_title",
                "include_patterns": ["Maple|Lake|Subway"],
                "exclude_patterns": ["Subway"],
            },
        )
    )

    assert result["revision"]["oldid"] == 1166890780
    assert result["counts"]["matched_item_count"] == 2
    assert [item["link_title"] for item in result["matched_items"]] == [
        "Maple Leaf (train)",
        "Lake Shore Limited",
    ]


def test_mediawiki_query_extracts_first_link_from_historical_field():
    class FakeToolkit(WikipediaToolkit):
        def _raw_revision_dict(self, oldid, language, site=""):
            return {
                "title": "ExampleOrg",
                "pageid": 1785141,
                "oldid": int(oldid),
                "timestamp": "2025-01-26T19:21:08Z",
                "size": 100,
                "wikitext": """
                {{Infobox company
                | name = ExampleOrg
                | markets = {{ubl|[[Country A]]|[[Country B]]}}
                }}
                """,
            }

    result = json.loads(
        FakeToolkit().mediawiki_evidence_query(
            title="ExampleOrg",
            revision={"mode": "oldid", "oldid": 1001},
            include=["infobox"],
            extract={"field_names": ["markets"], "link_mode": "first_link"},
        )
    )

    field = result["fields"][0]
    assert result["revision"]["oldid"] == 1001
    assert field["matched_field_name"] == "markets"
    assert field["selected_link"]["target"] == "Country A"
    assert field["selected_value"] == "Country A"
    assert "Country B" in field["cleaned_text"]


def test_mediawiki_query_prefers_exact_section_over_partial_infobox_field():
    class FakeToolkit(WikipediaToolkit):
        def _raw_revision_dict(self, oldid, language, site=""):
            return {
                "title": "ExampleOrg",
                "pageid": 1785141,
                "oldid": int(oldid),
                "timestamp": "2025-01-26T19:21:08Z",
                "size": 100,
                "wikitext": """
                {{Infobox company
                | name = ExampleOrg
                | market = [[Partial Field]]
                }}

                ==Markets==
                ExampleOrg operates in [[Country A]] and [[Country B]].
                """,
            }

    result = json.loads(
        FakeToolkit().mediawiki_evidence_query(
            title="ExampleOrg",
            revision={"mode": "oldid", "oldid": 1001},
            include=["infobox", "sections"],
            extract={"field_names": ["markets"], "link_mode": "first_link"},
        )
    )

    field = result["fields"][0]
    assert field["source_type"] == "section"
    assert field["matched_field_name"] == "Markets"
    assert field["selected_value"] == "Country A"
    assert field["selected_link"]["target"] == "Country A"


def test_mediawiki_query_cleans_native_phrase_template_from_current_page():
    class FakeToolkit(WikipediaToolkit):
        def _page_wikitext_dict(self, title, language, site=""):
            return {
                "title": "Example Country",
                "pageid": 14579,
                "oldid": 999,
                "timestamp": "2026-01-01T00:00:00Z",
                "size": 100,
                "wikitext": """
                {{Infobox country
                | common_name = Example Country
                | motto = {{native phrase|xx|[[Example Motto]]|paren=omit}} ([[Example language]])<br />"Plain translation"
                }}
                """,
            }

    result = json.loads(
        FakeToolkit().mediawiki_evidence_query(
            title="Example Country",
            revision={"mode": "current"},
            include=["infobox"],
            extract={"field_names": ["motto"], "link_mode": "raw_text"},
        )
    )

    field = result["fields"][0]
    assert field["matched_field_name"] == "motto"
    assert field["selected_link"]["target"] == "Example Motto"
    assert field["selected_value"].startswith("Example Motto")
    assert "Plain translation" in field["cleaned_text"]
