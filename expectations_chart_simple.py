import matplotlib.pyplot as plt
import streamlit as st
import numpy as np


def avg(lst):
    lst = [x for x in lst if not np.isnan(x)]
    return sum(lst) / len(lst)


st.set_page_config(layout="wide")
st.button("Refresh", type="primary", use_container_width=True)
longers = 3
long_size = 1
shorters = 3
short_size = 1
rate_min = 1
rate_max = 8
st.columns(1, gap="small")
expected_value_choice = "last value"
expected_value = 0

if __name__ == "__main__":
    rate_range = rate_max - rate_min
    max_size = max(long_size, short_size)
    history = [np.random.rand() * rate_range + rate_min]
    term_length = 90
    history.extend(history[-1] + (np.random.rand() - 0.5) * rate_range / 10 for _ in range(term_length - 1))
    fig = plt.figure(figsize=[10, 6])
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    color = colors[0]  # starting color
    p = plt.plot(history, label="history", color=color)
    plt.plot([avg(history)] * len(history), color=color, linestyle="--")
    actual = [np.nan] * (term_length - 1)
    label = "longer's expectations"
    market_equilibrium = 0
    if expected_value_choice == "last value":
        expected_value = history[-1]
    elif expected_value_choice == "historical average":
        expected_value = avg(history)
    expectation = [expected_value]
    for i in range(longers + shorters):
        expectation = [expected_value]
        direction = -1 if i < longers else 1
        while (avg(expectation) - expected_value) * direction <= 0:
            expectation = [expected_value]
            expectation.extend(
                expectation[-1] + (np.random.rand() - 0.5 + 0.01 * direction) * rate_range / 10
                for _ in range(term_length - 1)
            )
        size = short_size if i >= longers else long_size
        label = ""
        if i == 0:  # set stuff only for the first long
            color = colors[1]
            label = "expectations"
        p = plt.plot(actual + expectation, label=label, color=color, linewidth=size, alpha=0.5)
        plt.plot(
            actual + [avg(expectation)] * len(expectation),
            color=color,
            linestyle="--",
            linewidth=size,
            alpha=0.5,
        )
        market_equilibrium += avg(expectation) * size
    market_equilibrium = market_equilibrium / (long_size * longers + short_size * shorters)
    plt.plot(actual + [market_equilibrium] * len(expectation), label="market equilibrium", color=colors[3])
    plt.legend()
    st.pyplot(fig)
