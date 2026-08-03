"""Headless, deterministic control-system plotting templates."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def _style_axes(axis: Any, xlabel: str, ylabel: str) -> None:
    axis.set_xlabel(xlabel)
    axis.set_ylabel(ylabel)
    axis.grid(True, which="both", alpha=0.3)


def save_time_plot(time: np.ndarray, response: np.ndarray, path: Path, *, title: str, ylabel: str) -> None:
    figure, axis = plt.subplots(figsize=(7.2, 4.5), constrained_layout=True)
    axis.plot(time, response, color="#006D77", linewidth=1.7)
    axis.set_title(title)
    _style_axes(axis, "Time (s)", ylabel)
    figure.savefig(path)
    figure.savefig(path.with_suffix(".png"), dpi=180)
    plt.close(figure)


def save_bode_plot(omega: np.ndarray, magnitude: np.ndarray, phase_deg: np.ndarray, path: Path) -> None:
    figure, (magnitude_axis, phase_axis) = plt.subplots(2, 1, figsize=(7.2, 6.2), sharex=True, constrained_layout=True)
    magnitude_axis.semilogx(omega, 20 * np.log10(np.maximum(magnitude, np.finfo(float).tiny)), color="#006D77")
    phase_axis.semilogx(omega, phase_deg, color="#BB3E03")
    magnitude_axis.set_title("Bode Plot")
    _style_axes(magnitude_axis, "", "Magnitude (dB)")
    _style_axes(phase_axis, "Angular frequency (rad/s)", "Phase (deg)")
    figure.savefig(path)
    figure.savefig(path.with_suffix(".png"), dpi=180)
    plt.close(figure)


def save_nyquist_plot(response: np.ndarray, path: Path) -> None:
    figure, axis = plt.subplots(figsize=(6.2, 5.6), constrained_layout=True)
    axis.plot(response.real, response.imag, color="#006D77", label="positive frequency")
    axis.plot(response.real, -response.imag, color="#006D77", alpha=0.45, linestyle="--", label="mirror")
    axis.scatter([-1], [0], marker="x", color="#AE2012", s=70, label="critical point")
    axis.axhline(0, color="#333333", linewidth=0.7)
    axis.axvline(0, color="#333333", linewidth=0.7)
    axis.set_aspect("equal", adjustable="datalim")
    axis.set_title("Nyquist Plot")
    _style_axes(axis, "Real", "Imaginary")
    axis.legend(loc="best")
    figure.savefig(path)
    figure.savefig(path.with_suffix(".png"), dpi=180)
    plt.close(figure)


def save_root_locus_plot(loci: np.ndarray, poles: np.ndarray, zeros: np.ndarray, path: Path) -> None:
    figure, axis = plt.subplots(figsize=(6.4, 5.6), constrained_layout=True)
    for branch in range(loci.shape[1]):
        axis.plot(loci[:, branch].real, loci[:, branch].imag, color="#006D77", linewidth=1.0)
    if poles.size:
        axis.scatter(poles.real, poles.imag, marker="x", color="#AE2012", s=65, label="open-loop poles")
    if zeros.size:
        axis.scatter(zeros.real, zeros.imag, facecolors="none", edgecolors="#0A9396", s=65, label="open-loop zeros")
    axis.axhline(0, color="#333333", linewidth=0.7)
    axis.axvline(0, color="#333333", linewidth=0.7)
    axis.set_title("Root Locus")
    _style_axes(axis, "Real", "Imaginary")
    axis.legend(loc="best")
    figure.savefig(path)
    figure.savefig(path.with_suffix(".png"), dpi=180)
    plt.close(figure)

