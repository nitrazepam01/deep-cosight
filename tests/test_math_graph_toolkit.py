import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.abspath("."))

from app.cosight.tool.math_graph_toolkit import MathGraphToolkit


def test_function_graph_letter_probe_detects_unc_from_quadratics():
    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "letters.png")
        result = json.loads(
            MathGraphToolkit().function_graph_letter_probe(
                equations=[
                    "y = 6x^2 + 4x + 4",
                    "y = -6x^2 + 4x + 4",
                    "x = 6y^2 + 4y + 4",
                ],
                plot_range=[-2, 2],
                output_image_path=output_path,
            )
        )

    assert result["letters"] == ["U", "N", "C"]
    assert result["acronym"] == "UNC"
    assert result["analyses"][0]["orientation"] == "upward"
    assert result["analyses"][1]["orientation"] == "downward"
    assert result["analyses"][2]["orientation"] == "right"
    assert result["evidence"] == [
        "upward-opening parabola resembles U",
        "downward-opening parabola resembles n/N",
        "right-opening sideways parabola resembles C",
    ]


def test_function_graph_letter_probe_accepts_string_equations():
    result = json.loads(
        MathGraphToolkit().function_graph_letter_probe(
            equations="y=x^2; y=-x^2; x=y^2",
            output_image_path=os.path.join(tempfile.gettempdir(), "letters_string.png"),
        )
    )

    assert result["letters"] == ["U", "N", "C"]
    assert result["acronym"] == "UNC"
