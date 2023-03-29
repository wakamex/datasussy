import pkg_resources, os

try:
    pkg_resources.require(["matplotlib", "numpy", "streamlit"])
    print("All packages already installed")
except Exception:
    os.system("pip install matplotlib numpy streamlit")
    print("Packages have been installed")
import matplotlib.pyplot as plt  # pylint: disable=wrong-import-position
import streamlit as st  # pylint: disable=wrong-import-position
import numpy as np  # pylint: disable=wrong-import-position


def avg(lst):
    lst = [x for x in lst if not np.isnan(x)]
    return sum(lst) / len(lst)


st.set_page_config(layout="wide")
font_size = "<font size=5>"
st.markdown("# Expectations")
st.write(
    f"{font_size}market equilibrium is the combined expectation of all market participants (weighted by their size",
    unsafe_allow_html=True,
)
col1, col2, col3 = st.columns(3, gap="small")
with col1:
    longers = st.slider(label="longers", min_value=1, max_value=10, value=5)
    long_size = st.slider(label="long size", min_value=1, max_value=5, value=2)
with col2:
    shorters = st.slider(label="shorters", min_value=1, max_value=10, value=6)
    short_size = st.slider(label="short size", min_value=1, max_value=5, value=1)
with col3:
    rate_min = st.slider(label="rate min (%)", min_value=0, max_value=10, value=1)
    rate_max = st.slider(label="rate max (%)", min_value=0, max_value=10, value=8)
st.columns(1)
expected_value_choice: str = (
    st.selectbox(
        label="starting point for expectations (longs expect rates to be lower than this number, while shorts expected it to be higher)",
        options=["last value", "historical average"],
    )
    or ""
)
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
    breakdown_string = f"<br>{font_size}<font face='monospace'>"
    formula_string = ""
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
        # st.write("long") if i < longers else st.write("short")
        # st.write(f"expectation: {avg(expectation):.2f}% vs. actual: {history[-1]:.2f}%")
        size = short_size if i >= longers else long_size
        label = ""
        if i == 0:  # set stuff only for the first long
            color = colors[1]
            label = "longer's expectations"
        else:
            formula_string += " + "
        if i == longers:  # set stuff only for the first short
            color = colors[2]
            label = "shorter's expectations"
        p = plt.plot(actual + expectation, label=label, color=color, linewidth=size, alpha=0.5)
        plt.plot(
            actual + [avg(expectation)] * len(expectation),
            color=color,
            linestyle="--",
            linewidth=size,
            alpha=0.5,
        )
        user_type = "longer" if i < longers else "shorter"
        market_equilibrium += avg(expectation) * size
        formula_string += f"{size} * {avg(expectation):.2f}%"
        breakdown_string += f" - market paticipant #{i+1} is a "
        breakdown_string += "&nbsp;" if i < longers else ""
        breakdown_string += f"{user_type} whose market expectation is {avg(expectation):.2f}%" f" of size {size}<br>"
    market_equilibrium = market_equilibrium / (long_size * longers + short_size * shorters)
    formula_string += f") / ({long_size} * {longers} + {short_size} * {shorters})"
    markdown_string = f"\n{font_size}market equilibrium is {market_equilibrium:.2f}% = ("

    plt.plot(actual + [market_equilibrium] * len(expectation), label="market equilibrium", color=colors[3])
    plt.legend()
    st.pyplot(fig)

    st.write(markdown_string + formula_string + breakdown_string, unsafe_allow_html=True)
