"""Versioned public schemas for control tasks and tool outputs."""

from __future__ import annotations

import math
from typing import Any, Annotated, Literal

from pint import UnitRegistry
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

ureg = UnitRegistry(autoconvert_offset_to_baseunit=True)


def _finite(value: float, field_name: str) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{field_name} must be finite")
    return value


def _validate_unit(value: str | None) -> str | None:
    if value is None or not value.strip():
        return None
    try:
        ureg.Unit(value)
    except Exception as exc:
        raise ValueError(f"unknown or invalid unit: {value}") from exc
    return value.strip()


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class Timebase(StrictModel):
    kind: Literal["continuous", "discrete"]
    dt: float | None = None

    @model_validator(mode="after")
    def validate_timebase(self) -> "Timebase":
        if self.kind == "discrete":
            if self.dt is None or _finite(self.dt, "dt") <= 0:
                raise ValueError("discrete systems require a positive finite dt")
        elif self.dt is not None:
            raise ValueError("continuous systems must not define dt")
        return self


class Channel(StrictModel):
    name: str = Field(min_length=1, max_length=80)
    unit: str | None = None

    _unit = field_validator("unit")(_validate_unit)


class ChannelSet(StrictModel):
    inputs: list[Channel] = Field(min_length=1, max_length=8)
    outputs: list[Channel] = Field(min_length=1, max_length=8)
    states: list[Channel] | None = Field(default=None, max_length=50)


class TransferFunctionPlant(StrictModel):
    representation: Literal["transfer_function"]
    numerator: list[float] = Field(min_length=1, max_length=51)
    denominator: list[float] = Field(min_length=1, max_length=52)
    timebase: Timebase
    channels: ChannelSet

    @field_validator("numerator", "denominator")
    @classmethod
    def finite_coefficients(cls, values: list[float]) -> list[float]:
        return [_finite(value, "coefficient") for value in values]

    @model_validator(mode="after")
    def validate_transfer_function(self) -> "TransferFunctionPlant":
        if self.denominator[0] == 0:
            raise ValueError("denominator leading coefficient must be nonzero")
        if all(value == 0 for value in self.denominator):
            raise ValueError("denominator must not be the zero polynomial")
        if len(self.numerator) > len(self.denominator):
            raise ValueError("improper transfer functions are not supported")
        if len(self.channels.inputs) != 1 or len(self.channels.outputs) != 1:
            raise ValueError("transfer-function representation is SISO in schema version 1.0.0")
        if self.channels.states:
            raise ValueError("transfer-function representation must not define state channels")
        return self


class StateSpacePlant(StrictModel):
    representation: Literal["state_space"]
    A: list[list[float]]
    B: list[list[float]]
    C: list[list[float]]
    D: list[list[float]]
    timebase: Timebase
    channels: ChannelSet

    @field_validator("A", "B", "C", "D")
    @classmethod
    def finite_matrix(cls, matrix: list[list[float]]) -> list[list[float]]:
        if not matrix or any(not row for row in matrix):
            raise ValueError("matrices must be nonempty")
        width = len(matrix[0])
        if any(len(row) != width for row in matrix):
            raise ValueError("matrix rows must have equal length")
        return [[_finite(value, "matrix entry") for value in row] for row in matrix]

    @model_validator(mode="after")
    def validate_dimensions(self) -> "StateSpacePlant":
        n = len(self.A)
        if n > 50 or len(self.A[0]) != n:
            raise ValueError("A must be square with at most 50 states")
        m = len(self.B[0])
        p = len(self.C)
        if m > 8 or p > 8:
            raise ValueError("state-space systems support at most 8 inputs and 8 outputs")
        if len(self.B) != n or len(self.C[0]) != n:
            raise ValueError("B and C dimensions must agree with A")
        if len(self.D) != p or len(self.D[0]) != m:
            raise ValueError("D dimensions must be outputs by inputs")
        if len(self.channels.inputs) != m or len(self.channels.outputs) != p:
            raise ValueError("channel counts must match B/C/D dimensions")
        if self.channels.states is not None and len(self.channels.states) != n:
            raise ValueError("state channel count must match A dimension")
        return self


Plant = Annotated[TransferFunctionPlant | StateSpacePlant, Field(discriminator="representation")]


class FeedbackSpec(StrictModel):
    sign: Literal["negative", "positive"]
    gain: float = 1.0

    @field_validator("gain")
    @classmethod
    def finite_gain(cls, value: float) -> float:
        return _finite(value, "feedback gain")


class Requirement(StrictModel):
    metric: Literal[
        "overshoot_percent",
        "rise_time_s",
        "settling_time_s",
        "steady_state_error",
        "gain_margin",
        "gain_margin_db",
        "phase_margin_deg",
        "velocity_constant",
        "acceleration_constant",
    ]
    operator: Literal["<", "<=", ">", ">=", "=="]
    value: float
    unit: str | None = None
    input_index: int = Field(default=0, ge=0, le=7)
    output_index: int = Field(default=0, ge=0, le=7)
    tolerance: float = Field(default=1e-9, ge=0)

    _unit = field_validator("unit")(_validate_unit)

    @field_validator("value")
    @classmethod
    def finite_value(cls, value: float) -> float:
        return _finite(value, "requirement value")


class DesignSpec(StrictModel):
    method: Literal[
        "none",
        "pid_manual",
        "pid_ziegler_nichols",
        "pid_imc_fopdt",
        "lead",
        "lag",
        "frequency_gain",
        "root_locus",
        "state_feedback",
        "lqr",
    ] = "none"
    parameters: dict[str, Any] = Field(default_factory=dict)


class TimeGridSpec(StrictModel):
    mode: Literal["auto", "explicit"] = "auto"
    start: float = 0.0
    stop: float | None = None
    points: int = Field(default=1000, ge=2, le=20000)

    @model_validator(mode="after")
    def validate_explicit(self) -> "TimeGridSpec":
        if self.mode == "explicit":
            if self.stop is None or not math.isfinite(self.stop) or self.stop <= self.start:
                raise ValueError("explicit time grids require stop > start")
        return self


class FrequencyGridSpec(StrictModel):
    mode: Literal["auto", "explicit"] = "auto"
    minimum_rad_s: float | None = None
    maximum_rad_s: float | None = None
    points: int = Field(default=800, ge=10, le=5000)

    @model_validator(mode="after")
    def validate_explicit(self) -> "FrequencyGridSpec":
        if self.mode == "explicit":
            lo, hi = self.minimum_rad_s, self.maximum_rad_s
            if lo is None or hi is None or lo <= 0 or hi <= lo:
                raise ValueError("explicit frequency grids require 0 < minimum < maximum")
        return self


class SimulationSpec(StrictModel):
    configuration: Literal["open_loop", "closed_loop"] = "closed_loop"
    responses: list[Literal["step", "impulse", "bode", "nyquist", "root_locus"]] = Field(
        default_factory=lambda: ["step", "bode"]
    )
    time: TimeGridSpec = Field(default_factory=TimeGridSpec)
    frequency: FrequencyGridSpec = Field(default_factory=FrequencyGridSpec)
    settling_threshold: float = Field(default=0.02, gt=0, lt=1)
    rise_limits: tuple[float, float] = (0.1, 0.9)

    @field_validator("rise_limits")
    @classmethod
    def validate_rise_limits(cls, value: tuple[float, float]) -> tuple[float, float]:
        if not (0 <= value[0] < value[1] <= 1):
            raise ValueError("rise_limits must satisfy 0 <= lower < upper <= 1")
        return value


class ControlTask(StrictModel):
    schema_version: Literal["1.0.0"] = "1.0.0"
    task_id: str = Field(min_length=1, max_length=120)
    plant: Plant
    feedback: FeedbackSpec
    requirements: list[Requirement] = Field(default_factory=list, max_length=100)
    design: DesignSpec = Field(default_factory=DesignSpec)
    simulation: SimulationSpec = Field(default_factory=SimulationSpec)
    backends: list[Literal["python-control", "scipy", "octave", "matlab"]] = Field(
        default_factory=lambda: ["python-control", "scipy"]
    )


class ToolEnvelope(StrictModel):
    schema_version: Literal["1.0.0"] = "1.0.0"
    status: Literal["ok", "warning", "error", "review_required"]
    execution_id: str
    data: Any = None
    warnings: list[dict[str, Any]] = Field(default_factory=list)
    errors: list[dict[str, Any]] = Field(default_factory=list)
    review_required: bool = False
    artifacts: list[dict[str, Any]] = Field(default_factory=list)
    provenance: dict[str, Any] = Field(default_factory=dict)

