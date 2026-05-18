import json
import os
import sys

sys.path.insert(0, os.path.abspath("."))

from app.cosight.tool.document_processing_toolkit import DocumentProcessingToolkit


def test_document_abstract_year_count_counts_only_before_raktazodziai():
    class FakeToolkit(DocumentProcessingToolkit):
        def _extract_text_for_counting(self, document_path):
            return """
            BULVIŲ RINKA 2009 METAIS
            THE POTATO MARKET IN 2009

            Ingrida LUKOŠIUTĖ
            LAEI Produktų rinkotyros skyriaus tyrėja

            Straipsnyje aptariamos bulvių kainos. Daugelyje ES šalių bulvių kaina
            mažesnė nei 2008 metais. Nors Lietuvoje bulvės atpigo, jos buvo
            brangesnės nei Vokietijoje.

            Raktažodžiai: bulvės, kaina.
            ĮVADAS
            Lietuvoje bulvių sektorius nėra didelis. 2008 metais bulvės sudarė
            6,7 proc. produkcijos. Kitas 2008 paminėjimas yra正文.
            """

    result = json.loads(
        FakeToolkit().document_abstract_year_count(
            document_path="fake.pdf",
            publication_year="2008",
            book_title="The Propitious Esculent",
        )
    )

    assert result["abstract_count"] == 1
    assert result["answer"] == "1"
    assert result["full_document_count"] == 3
    assert result["abstract_end_marker"] == "Raktažodžiai"
    assert result["excluded_following_section"] == "ĮVADAS"
    assert "ĮVADAS" not in result["abstract_text"]


def test_document_abstract_year_count_requires_year_when_lookup_missing():
    class FakeToolkit(DocumentProcessingToolkit):
        def _resolve_publication_year(self, book_title):
            return "", ""

    result = json.loads(
        FakeToolkit().document_abstract_year_count(
            document_path="fake.pdf",
            book_title="Unknown Book",
        )
    )

    assert "error" in result
    assert "publication_year is required" in result["error"]
