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
        def _parse_html(self, oldid, language):
            return '<p><sup class="reference">[1]</sup><sup class="reference">[1]</sup></p>'

        def _render_html(self, oldid, title, language):
            return """
            <ol class="references">
              <li id="cite_note-a-1"><span class="mw-reference-text">A</span></li>
            </ol>
            <p><sup class="reference">[1]</sup><sup class="reference">[1]</sup></p>
            """

        def _raw_revision_dict(self, oldid, language):
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


def test_zte_reference_delta_shape_uses_unique_counts():
    class FakeToolkit(WikipediaToolkit):
        def _first_revision_dict(self, title, year, language):
            return {
                "title": title,
                "year": year,
                "oldid": 1272009703 if year == 2025 else 1333650803,
                "timestamp": "2025-01-26T19:21:08Z" if year == 2025 else "2026-01-19T00:12:33Z",
                "url": f"https://en.wikipedia.org/w/index.php?title={title}&oldid={year}",
            }

        def _reference_count_dict(self, oldid, title, language, include_raw_ref_check=True):
            if int(oldid) == 1272009703:
                return {
                    "oldid": oldid,
                    "recommended_count": 121,
                    "recommended_count_method": "rendered_reference_list_items",
                    "citation_callouts": 136,
                }
            return {
                "oldid": oldid,
                "recommended_count": 125,
                "recommended_count_method": "rendered_reference_list_items",
                "citation_callouts": 142,
            }

    result = json.loads(
        FakeToolkit().wiki_revision_reference_delta(
            title="ZTE",
            earlier_year=2025,
            later_year=2026,
        )
    )

    assert result["earlier_reference_count"] == 121
    assert result["later_reference_count"] == 125
    assert result["increase"] == 4
    assert result["calculation"] == "125 - 121 = 4"


def test_revision_at_picks_last_revision_before_cutoff():
    class FakeToolkit(WikipediaToolkit):
        def _get_json(self, language, params):
            assert params["rvdir"] == "older"
            return {
                "query": {
                    "pages": [
                        {
                            "title": "Adirondack (train)",
                            "pageid": 123,
                            "revisions": [
                                {
                                    "revid": 200,
                                    "timestamp": "2023-08-01T00:00:00Z",
                                    "size": 10,
                                },
                                {
                                    "revid": 199,
                                    "timestamp": "2023-07-24T11:28:06Z",
                                    "size": 9,
                                },
                            ],
                        }
                    ]
                }
            }

    result = FakeToolkit()._revision_at_dict(
        title="Adirondack (train)",
        cutoff_timestamp="2023-08-01T00:00:00Z",
        language="en",
        inclusive=False,
    )

    assert result["oldid"] == 199
    assert result["timestamp"] == "2023-07-24T11:28:06Z"


def test_revision_size_delta_find_uses_adjacent_chronological_sizes():
    class FakeToolkit(WikipediaToolkit):
        def _revision_size_history(self, title, start_timestamp, end_timestamp, language):
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
        FakeToolkit().wiki_revision_size_delta_find(
            title="Example",
            year=2025,
            target_delta=889,
        )
    )

    assert result["target_delta"] == 889
    assert result["revision_count"] == 4
    assert result["match_count"] == 1
    assert result["matched_revision"]["oldid"] == 12
    assert result["matched_revision"]["parent_oldid"] == 11
    assert result["matched_revision"]["calculation"] == "1989 - 1100 = 889"
    assert result["formatted_date"] == "2025/03/01"


def test_revision_table_parser_preserves_links():
    html = """
    <table class="wikitable">
      <tr><th>Station</th><th>Connections</th></tr>
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


def test_rail_connection_count_deduplicates_adirondack_style_table():
    class FakeToolkit(WikipediaToolkit):
        def _raw_revision_dict(self, oldid, language):
            return {
                "title": "Adirondack (train)",
                "pageid": 456,
                "oldid": int(oldid),
                "timestamp": "2023-07-24T11:28:06Z",
                "size": 100,
                "wikitext": "",
            }

        def _section_index_for_keyword(self, oldid, language, section_keyword):
            return "3"

        def _parse_html(self, oldid, language, section=None):
            return """
            <table class="wikitable">
              <tr><th>Station</th><th>Connections/Notes</th></tr>
              <tr>
                <td>Montreal</td>
                <td>
                  <a title="Quebec City-Windsor Corridor">Corridor</a>;
                  <a title="Ocean (train)">Ocean</a>;
                  <a title="Montreal-Jonquiere train">Montreal-Jonquiere</a>;
                  <a title="Montreal-Senneterre train">Montreal-Senneterre</a>;
                  <a title="Mont-Saint-Hilaire line">Mont-Saint-Hilaire line</a>;
                  <a title="Mascouche line">Mascouche line</a>;
                  Montreal Metro; bus
                </td>
              </tr>
              <tr>
                <td>Albany-Rensselaer</td>
                <td>
                  <a title="Ethan Allen Express">Ethan Allen Express</a>;
                  <a title="Empire Service">Empire Service</a>;
                  <a title="Lake Shore Limited">Lake Shore Limited</a>;
                  <a title="Maple Leaf (train)">Maple Leaf</a>;
                  <a title="Berkshire Flyer">Berkshire Flyer</a>;
                  Amtrak Thruway
                </td>
              </tr>
              <tr>
                <td>Croton-Harmon</td>
                <td>
                  <a title="Hudson Line (Metro-North)">Hudson Line</a>;
                  <a title="Maple Leaf (train)">Maple Leaf</a>
                </td>
              </tr>
              <tr>
                <td>New York Penn Station</td>
                <td>
                  <a title="Cardinal (train)">Cardinal</a>;
                  <a title="Crescent (train)">Crescent</a>;
                  <a title="Palmetto (train)">Palmetto</a>;
                  <a title="Pennsylvanian (train)">Pennsylvanian</a>;
                  <a title="Silver Meteor">Silver Meteor</a>;
                  <a title="Silver Star">Silver Star</a>;
                  <a title="Acela">Acela</a>;
                  <a title="Carolinian (train)">Carolinian</a>;
                  <a title="Keystone Service">Keystone Service</a>;
                  <a title="Northeast Regional">Northeast Regional</a>;
                  <a title="Vermonter (train)">Vermonter</a>;
                  <a title="Main Line (Long Island Rail Road)">Main Line</a>;
                  <a title="Port Washington Branch">Port Washington Branch</a>;
                  <a title="North Jersey Coast Line">North Jersey Coast Line</a>;
                  <a title="Northeast Corridor Line">Northeast Corridor Line</a>;
                  <a title="Gladstone Branch">Gladstone Branch</a>;
                  <a title="Montclair-Boonton Line">Montclair-Boonton Line</a>;
                  <a title="Morristown Line">Morristown Line</a>;
                  New York City Subway
                </td>
              </tr>
            </table>
            """

    result = json.loads(
        FakeToolkit().wiki_rail_connection_count(
            title="Adirondack (train)",
            cutoff_timestamp="2023-08-01T00:00:00Z",
            oldid=1166890780,
        )
    )

    assert result["revision"]["oldid"] == 1166890780
    assert result["connection_count"] == 30
    assert result["group_counts"] == {
        "VIA Rail / Exo": 6,
        "Amtrak": 16,
        "Commuter rail": 8,
    }
    assert result["calculation"] == "6 + 16 + 8 = 30"
    assert any(item["term"] == "subway" for item in result["excluded_detected_terms"])
    assert any(line["name"] == "Amtrak: Maple Leaf" for line in result["counted_lines"])


def test_infobox_field_lookup_extracts_first_link_from_historical_field():
    class FakeToolkit(WikipediaToolkit):
        def _raw_revision_dict(self, oldid, language):
            return {
                "title": "ZTE",
                "pageid": 1785141,
                "oldid": int(oldid),
                "timestamp": "2025-01-26T19:21:08Z",
                "size": 100,
                "wikitext": """
                {{Infobox company
                | name = ZTE
                | subsidiaries = {{ubl|[[Indonesia]]|[[Australia]]}}
                }}
                """,
            }

    result = json.loads(
        FakeToolkit().wiki_infobox_field_lookup(
            title="ZTE",
            oldid=1272009703,
            field_name="subsidiaries",
            link_mode="first_link",
        )
    )

    assert result["oldid"] == 1272009703
    assert result["matched_field_name"] == "subsidiaries"
    assert result["selected_link"]["target"] == "Indonesia"
    assert result["selected_value"] == "Indonesia"
    assert "Australia" in result["cleaned_text"]


def test_infobox_field_lookup_prefers_exact_section_over_partial_infobox_field():
    class FakeToolkit(WikipediaToolkit):
        def _raw_revision_dict(self, oldid, language):
            return {
                "title": "ZTE",
                "pageid": 1785141,
                "oldid": int(oldid),
                "timestamp": "2025-01-26T19:21:08Z",
                "size": 100,
                "wikitext": """
                {{Infobox company
                | name = ZTE
                | subsid = [[Nubia Technology]]
                }}

                ==Subsidiaries==
                [[File:ZTE.jpg|thumb|ZTE]]
                ZTE has subsidiaries in countries including [[Indonesia]], [[Australia]].
                """,
            }

    result = json.loads(
        FakeToolkit().wiki_infobox_field_lookup(
            title="ZTE",
            oldid=1272009703,
            field_name="subsidiaries",
            link_mode="first_link",
        )
    )

    assert result["source_type"] == "section"
    assert result["matched_field_name"] == "Subsidiaries"
    assert result["selected_value"] == "Indonesia"
    assert result["selected_link"]["target"] == "Indonesia"


def test_infobox_field_lookup_cleans_native_phrase_template():
    class FakeToolkit(WikipediaToolkit):
        def _page_wikitext_dict(self, title, language):
            return {
                "title": "Indonesia",
                "pageid": 14579,
                "oldid": 999,
                "timestamp": "2026-01-01T00:00:00Z",
                "size": 100,
                "wikitext": """
                {{Infobox country
                | common_name = Indonesia
                | national_motto = {{native phrase|kaw|[[Bhinneka Tunggal Ika]]|paren=omit}} ([[Old Javanese]])<br />"Unity in Diversity"
                }}
                """,
            }

    result = json.loads(
        FakeToolkit().wiki_infobox_field_lookup(
            title="Indonesia",
            field_name="national_motto",
            link_mode="raw_text",
        )
    )

    assert result["matched_field_name"] == "national_motto"
    assert result["selected_link"]["target"] == "Bhinneka Tunggal Ika"
    assert result["selected_value"].startswith("Bhinneka Tunggal Ika")
    assert "Unity in Diversity" in result["cleaned_text"]
