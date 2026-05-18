import json
import os
import sys

sys.path.insert(0, os.path.abspath("."))

from app.cosight.tool.taxonomy_toolkit import TaxonomyToolkit


def test_binomial_from_root_appends_suffix_and_duplicates():
    candidate = TaxonomyToolkit._binomial_from_root("histrionic", "us")

    assert candidate["root_word"] == "histrionic"
    assert candidate["suffix"] == "us"
    assert candidate["appended_word"] == "histrionicus"
    assert candidate["scientific_name"] == "Histrionicus histrionicus"


def test_taxon_binomial_verify_finds_histrionic_duck_candidate():
    class FakeToolkit(TaxonomyToolkit):
        def _gbif_match(self, scientific_name):
            if scientific_name == "Histrionicus histrionicus":
                return {
                    "usageKey": 2498383,
                    "canonicalName": "Histrionicus histrionicus",
                    "scientificName": "Histrionicus histrionicus (Linnaeus, 1758)",
                    "rank": "SPECIES",
                    "family": "Anatidae",
                    "matchType": "EXACT",
                    "confidence": 99,
                }
            return {"matchType": "NONE", "rank": None, "confidence": 0}

        def _gbif_vernacular_names(self, usage_key):
            if usage_key == 2498383:
                return ["Harlequin Duck"]
            return []

        def _wikipedia_search(self, scientific_name, language="en"):
            if scientific_name == "Histrionicus histrionicus":
                return {
                    "results": [
                        {
                            "title": "Harlequin duck",
                            "pageid": 123,
                            "snippet": "The harlequin duck is Histrionicus histrionicus.",
                            "url": "https://en.wikipedia.org/wiki/Harlequin_duck",
                        }
                    ]
                }
            return {"results": []}

    result = json.loads(
        FakeToolkit().taxon_binomial_verify(
            candidate_words="dramatic|theatrical|histrionic",
            suffixes="us",
            expected_common_name_keyword="duck",
            expected_family="Anatidae",
        )
    )

    assert result["verified"] is True
    assert result["answer"] == "Histrionic"
    assert result["root_word"] == "histrionic"
    assert result["suffix"] == "us"
    assert result["scientific_name"] == "Histrionicus histrionicus"
    assert result["common_name"] == "Harlequin duck"
    assert result["checked_count"] == 3
