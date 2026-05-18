# Copyright 2025 ZTE Corporation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple

from app.common.logger_util import logger


class MathGraphToolkit:
    """Helpers for deterministic graph-shape and simple letter-clue tasks."""

    @staticmethod
    def _json(data: Dict[str, Any]) -> str:
        return json.dumps(data, ensure_ascii=False, indent=2)

    @staticmethod
    def _normalize_equations(equations: Any) -> List[str]:
        if isinstance(equations, str):
            lines = re.split(r"[\n;]+", equations)
            return [line.strip() for line in lines if line.strip()]
        if isinstance(equations, (list, tuple)):
            return [str(item).strip() for item in equations if str(item).strip()]
        return [str(equations).strip()] if equations is not None else []

    @staticmethod
    def _normalize_expression(value: str) -> str:
        value = str(value or "").lower()
        value = (
            value.replace(" ", "")
            .replace("\u2212", "-")
            .replace("\u2010", "-")
            .replace("\u2011", "-")
            .replace("\u2012", "-")
            .replace("\u2013", "-")
            .replace("\u2014", "-")
            .replace("**", "^")
            .replace("*", "")
        )
        return value

    @staticmethod
    def _parse_coefficient(value: str) -> float:
        if value in ("", "+"):
            return 1.0
        if value == "-":
            return -1.0
        return float(value)

    @classmethod
    def _parse_quadratic_rhs(cls, rhs: str, variable: str) -> Tuple[float, float, float]:
        expr = cls._normalize_expression(rhs)
        if not expr:
            raise ValueError("Empty equation right-hand side")
        if expr[0] not in "+-":
            expr = "+" + expr

        a = b = c = 0.0
        for token in re.findall(r"[+-][^+-]+", expr):
            sign = -1.0 if token[0] == "-" else 1.0
            body = token[1:]
            squared_suffix = f"{variable}^2"
            if body.endswith(squared_suffix):
                coeff = body[: -len(squared_suffix)]
                a += sign * cls._parse_coefficient(coeff)
            elif body.endswith(variable):
                coeff = body[: -len(variable)]
                b += sign * cls._parse_coefficient(coeff)
            else:
                c += sign * float(body)
        if a == 0:
            raise ValueError(f"Not a quadratic expression in {variable}: {rhs}")
        return a, b, c

    @classmethod
    def _analyze_equation(cls, equation: str, index: int) -> Dict[str, Any]:
        if "=" not in equation:
            raise ValueError(f"Equation must contain '=': {equation}")
        lhs, rhs = equation.split("=", 1)
        lhs = cls._normalize_expression(lhs)

        if lhs == "y":
            variable = "x"
            axis = "vertical"
            a, b, c = cls._parse_quadratic_rhs(rhs, variable)
            opens = "upward" if a > 0 else "downward"
            letter = "U" if a > 0 else "N"
            evidence = (
                "upward-opening parabola resembles U"
                if a > 0
                else "downward-opening parabola resembles n/N"
            )
        elif lhs == "x":
            variable = "y"
            axis = "horizontal"
            a, b, c = cls._parse_quadratic_rhs(rhs, variable)
            opens = "right" if a > 0 else "left"
            letter = "C" if a > 0 else "reverse C"
            evidence = (
                "right-opening sideways parabola resembles C"
                if a > 0
                else "left-opening sideways parabola resembles a reversed C"
            )
        else:
            raise ValueError(f"Only equations solved for x or y are supported: {equation}")

        vertex_input = -b / (2 * a)
        vertex_output = a * vertex_input * vertex_input + b * vertex_input + c
        vertex = (
            {"x": vertex_input, "y": vertex_output}
            if lhs == "y"
            else {"x": vertex_output, "y": vertex_input}
        )
        return {
            "index": index,
            "equation": equation,
            "lhs": lhs,
            "quadratic_variable": variable,
            "coefficients": {"a": a, "b": b, "c": c},
            "axis": axis,
            "orientation": opens,
            "vertex": vertex,
            "letter_guess": letter,
            "evidence": evidence,
        }

    @staticmethod
    def _parse_plot_range(plot_range: Any) -> Tuple[float, float]:
        if plot_range is None or plot_range == "":
            return -2.0, 2.0
        if isinstance(plot_range, (int, float)):
            value = abs(float(plot_range))
            return -value, value
        if isinstance(plot_range, str):
            numbers = [float(item) for item in re.findall(r"-?\d+(?:\.\d+)?", plot_range)]
            if len(numbers) >= 2:
                return numbers[0], numbers[1]
        if isinstance(plot_range, (list, tuple)) and len(plot_range) >= 2:
            return float(plot_range[0]), float(plot_range[1])
        raise ValueError(f"Invalid plot_range: {plot_range}")

    @staticmethod
    def _resolve_output_path(output_image_path: Optional[str]) -> str:
        path = output_image_path or "function_graph_letters.png"
        if not os.path.isabs(path):
            workspace = os.environ.get("WORKSPACE_PATH") or os.getcwd()
            path = os.path.join(workspace, path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return path

    @classmethod
    def _render_plot(
        cls,
        analyses: List[Dict[str, Any]],
        plot_range: Tuple[float, float],
        output_image_path: str,
    ) -> None:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np

        count = len(analyses)
        fig, axes = plt.subplots(1, count, figsize=(max(4 * count, 4), 4))
        if count == 1:
            axes = [axes]
        low, high = plot_range
        values = np.linspace(low, high, 400)

        for ax, item in zip(axes, analyses):
            coeffs = item["coefficients"]
            a, b, c = coeffs["a"], coeffs["b"], coeffs["c"]
            if item["lhs"] == "y":
                x_values = values
                y_values = a * values**2 + b * values + c
            else:
                y_values = values
                x_values = a * values**2 + b * values + c
            ax.plot(x_values, y_values, linewidth=2)
            ax.axhline(0, color="#cccccc", linewidth=0.8)
            ax.axvline(0, color="#cccccc", linewidth=0.8)
            ax.set_aspect("equal", adjustable="box")
            ax.set_title(f"{item['equation']} -> {item['letter_guess']}")
            ax.grid(True, linewidth=0.4, alpha=0.45)

        fig.tight_layout()
        fig.savefig(output_image_path, dpi=150, bbox_inches="tight")
        plt.close(fig)

    def function_graph_letter_probe(
        self,
        equations: Any,
        plot_range: Any = None,
        output_image_path: Optional[str] = None,
    ) -> str:
        """Render simple quadratic graphs and infer letter-like shapes."""
        try:
            normalized_equations = self._normalize_equations(equations)
            if not normalized_equations:
                raise ValueError("Provide at least one equation")

            analyses = [
                self._analyze_equation(equation, index + 1)
                for index, equation in enumerate(normalized_equations)
            ]
            letters = [item["letter_guess"] for item in analyses]
            acronym = "".join(letter for letter in letters if len(letter) == 1)
            low, high = self._parse_plot_range(plot_range)
            image_path = self._resolve_output_path(output_image_path)
            warnings: List[str] = []
            try:
                self._render_plot(analyses, (low, high), image_path)
            except Exception as exc:
                image_path = ""
                warnings.append(f"Plot rendering failed: {exc}")

            result = {
                "equations": normalized_equations,
                "plot_range": [low, high],
                "rendered_image_path": image_path,
                "letters": letters,
                "acronym": acronym,
                "analyses": analyses,
                "evidence": [item["evidence"] for item in analyses],
                "method": (
                    "Parse simple quadratic equations solved for x or y, identify the opening "
                    "direction from coefficient a, render the curves, and map the shape to a letter cue."
                ),
            }
            if warnings:
                result["warnings"] = warnings
            return self._json(result)
        except Exception as exc:
            logger.error("function_graph_letter_probe failed: %s", exc, exc_info=True)
            return self._json(
                {
                    "error": str(exc),
                    "equations": equations,
                    "plot_range": plot_range,
                    "output_image_path": output_image_path,
                }
            )
