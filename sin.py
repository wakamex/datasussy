import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


def _sinusoid(times, ampitude, offset, frequency, phase):
    """
    times : array of time steps
    amplitude : half the distance between the maximum and minimum values of the function
    offset : vertical shift
    frequency : number of cycles between 0 and 1 (the period is 1/frequency)
    phase : horizontal shift
    """
    return amplitude * np.sin(frequency * times + phase) + offset


def sin_df(parameters: dict) -> pd.DataFrame:
    times = params["times"]
    amp = parameters["amplitude"]
    offset = parameters["offset"]
    freq = 2 * np.pi * parameters["frequency"]
    phase = parameters["phase"]
    return pd.DataFrame({"f(t)": _sinusoid(times, amp, offset, freq, phase)})


def hex_from_name(name):
    if name == "blue":
        hex_val = "#005b96"
    elif name == "red":
        hex_val = "#990000"
    return hex_val


time_offset = st.slider(label="time offset", min_value=0.0, max_value=10.0, value=0.0)
amplitude = st.slider(label="amplitude", min_value=0.0, max_value=5.0, value=1.0)
frequency = st.slider(label="frequency", min_value=0.0, max_value=1.0, value=0.5)
phase = st.slider(label="horizontal shift", min_value=0.0, max_value=np.pi, value=0.0)
offset = st.slider(label="vertical shift", min_value=0.0, max_value=5.0, value=0.0)

color = st.selectbox("line color", ["blue", "red"])


def format_inputs(
    time_params: list,
    amplitude: bool,
    frequency: float,
    phase: float,
    offset: float,
    color: str,
) -> dict:
    return {
        "times": np.arange(*time_params),
        "time_min": time_params[0],
        "time_max": time_params[1],
        "time_step": time_params[2],
        "amplitude": amplitude,
        "frequency": frequency,
        "phase": phase,
        "offset": offset,
        "color": hex_from_name(color),
    }


if __name__ == "__main__":
    time_min = 0.0 + time_offset
    time_max = 30.0 + time_offset
    time_step = 0.1

    params = format_inputs(
        [time_min, time_max, time_step], amplitude, frequency, phase, offset, color
    )
    adjusted_times = params["times"] + time_offset

    S = sin_df(parameters=params)
    S.index = adjusted_times

    S = S.reset_index().rename(columns={"index": "t", 0: "f(t)"})  # .query('t < 22.')
    c = (
        alt.Chart(S)
        .mark_line()
        .encode(
            x=alt.X(
                "t",
                scale=alt.Scale(
                    domain=[np.min(adjusted_times), np.max(adjusted_times)]
                ),
            ),
            y="f(t)",
            color=alt.value(params["color"]),
        )
    )
    st.altair_chart(c, use_container_width=True)
