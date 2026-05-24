import json
import os
import sys

sys.path.insert(0, os.path.abspath("."))

from app.cosight.tool.google_books_toolkit import GoogleBooksToolkit


def test_extract_book_id_from_google_books_url():
    assert (
        GoogleBooksToolkit._extract_book_id(
            book_url="https://books.google.com/books/about/Joy_of_Cooking.html?id=C4_5MCUd6ucC"
        )
        == "C4_5MCUd6ucC"
    )


def test_page_reference_extraction_ranks_target_phrase():
    snippet = (
        "... raccoon with : Sweet Potato and Apple Dressing , 374 "
        "Bake , covered , about 45 minutes ."
    )

    refs = GoogleBooksToolkit._extract_page_references(
        snippet,
        target_phrase="Sweet Potato and Apple Dressing",
    )

    assert refs
    assert refs[0]["page_number"] == 374
    assert "Sweet Potato and Apple Dressing" in refs[0]["context"]


def test_google_books_volume_search_shapes_searchwithinvolume_response():
    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "search_results": [
                    {
                        "page_id": "PA516",
                        "snippet_text": (
                            "... raccoon with : Sweet Potato and Apple Dressing , 374 "
                            "Bake , covered , about 45 minutes ."
                        ),
                    }
                ]
            }

    class FakeSession:
        headers = {}

        def get(self, url, params=None, timeout=None):
            assert params["jscmd"] == "SearchWithinVolume2"
            assert params["id"] == "C4_5MCUd6ucC"
            assert params["q"] == "raccoon"
            return FakeResponse()

    tool = GoogleBooksToolkit()
    tool.session = FakeSession()

    result = json.loads(
        tool.google_books_volume_search(
            book_id="C4_5MCUd6ucC",
            query="raccoon",
            target_phrase="Sweet Potato and Apple Dressing",
        )
    )

    assert result["book_id"] == "C4_5MCUd6ucC"
    assert result["matched_pages"][0]["page_id"] == "PA516"
    assert "snippet_html" not in result["matched_pages"][0]
    assert result["best_page_reference"]["page_number"] == 374
    assert result["best_page_reference"]["source_page_id"] == "PA516"


def test_google_books_volume_search_returns_concise_evidence_by_default():
    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "search_results": [
                    {
                        "page_id": "PA325",
                        "page_number": "325",
                        "snippet_text": "Irma S. Rombauer. STUFFED SWEET POTATOES " + "apple water " * 80,
                    },
                    {
                        "page_id": "PA374",
                        "page_number": "374",
                        "snippet_text": (
                            "SWEET POTATO AND SAUSAGE STUFFING ... APPLE DRESSING "
                            "Prepare : About 5 Cups Sweet Potatoes and Fruit , 325 "
                            + "using apples " * 80
                        ),
                    },
                    {
                        "page_id": "PA516",
                        "page_number": "516",
                        "snippet_text": (
                            "... Stuff the raccoon with : Sweet Potato and Apple Dressing , 374 "
                            "Bake , covered , about 45 minutes . "
                            + "Uncover and bake " * 80
                        ),
                    },
                    {
                        "page_id": "PA861",
                        "page_number": "861",
                        "snippet_text": "Index sweet potato , 260 covered , 417 " + "index item " * 80,
                    },
                    {
                        "page_id": "PA904",
                        "page_number": "904",
                        "snippet_text": "Index sauce, sweet or dessert, 769 " + "index item " * 80,
                    },
                ]
            }

    class FakeSession:
        headers = {}

        def get(self, url, params=None, timeout=None):
            return FakeResponse()

    tool = GoogleBooksToolkit()
    tool.session = FakeSession()

    raw = tool.google_books_volume_search(
        book_id="C4_5MCUd6ucC",
        query="Sweet Potato and Apple Dressing",
        target_phrase="Sweet Potato and Apple Dressing",
        max_results=10,
    )
    result = json.loads(raw)

    assert len(raw) < 3500
    assert result["detail_level"] == "concise"
    assert result["matched_page_count"] == 5
    assert result["returned_page_count"] <= 3
    assert result["best_page_reference"]["page_number"] == 374
    assert result["best_page_reference"]["source_page_id"] == "PA516"
    assert all("snippet_html" not in page for page in result["matched_pages"])
    assert all(len(page["snippet_text"]) <= 220 for page in result["matched_pages"])
