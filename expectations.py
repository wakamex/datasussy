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
st.write(f"{font_size}market equilibrium is the combined expectation of all market participants (weighted by their size", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3, gap="small")
with col1:
  longers = st.slider(label="longers", min_value=1, max_value=10, value=1)
  long_size = st.slider(label="long size", min_value=1, max_value=5, value=2)
with col2:
  shorters = st.slider(label="shorters", min_value=1, max_value=10, value=2)
  short_size = st.slider(label="short size", min_value=1, max_value=5, value=1)
with col3:
  rate_min = st.slider(label="rate min (%)", min_value=0, max_value=10, value=1)
  rate_max = st.slider(label="rate max (%)", min_value=0, max_value=10, value=8)

if __name__ == "__main__":
    st.columns(1)
    rate_range = rate_max - rate_min
    max_size = max(long_size, short_size)
    history = [np.random.rand() * rate_range + rate_min]
    term_length = 90
    history.extend(history[-1] + (np.random.rand() - 0.5) * rate_range / 10 for _ in range(term_length - 1))
    fig = plt.figure(figsize=[10, 6])
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    p = plt.plot(history, label="history")
    plt.plot([avg(history)] * len(history), color=p[0].get_color(), linestyle="--")
    actual = [np.nan] * (term_length - 1)
    label = "longer's expectations"
    size = long_size
    expectation = [history[-1]]
    for i in range(longers + shorters):
        expectation = [history[-1]]
        color = colors[1]  # starting color
        expectation.extend(expectation[-1] + (np.random.rand() - 0.5) * rate_range / 10 for _ in range(term_length - 1))
        if i >= longers:  # we are plotting a short
            size = short_size
            if i == longers:  # set stuff only for the first short
                color = colors[2]
                label = "shorter's expectations"
            else:
                label = ""
        p = plt.plot(actual + expectation, label=label, color=color, linewidth=size, alpha=0.5)
        plt.plot(
            actual + [avg(expectation)] * len(expectation),
            color=color,
            linestyle="--",
            linewidth=size / max_size,
            alpha=0.5,
        )
    market_equilibrium = np.mean([line.get_ydata()[-1] * line.get_linewidth() for line in plt.gca().lines[2:]])
    plt.plot(
        actual + [market_equilibrium] * len(expectation),
        label="market equilibrium",
        color=colors[3],
    )
    plt.legend()
    markdown_string = f"{font_size}"
    for i, line in enumerate(plt.gca().lines[2:-2:2]):
        user_type = "longer" if i < longers else "shorter"
        user_size = long_size if i < longers else short_size
        markdown_string += (
            f"market paticipant #{i+1} is a {user_type:7s}"
            f" whose market expectation is {avg(line.get_ydata()):.2f}%"
            f" of size {user_size}"
            f"<br>\n"
        )
    markdown_string += f"\n{font_size}market equilibrium is {market_equilibrium:.2f}% = "
    markdown_string += " + ".join(f"{line.get_linewidth()} * {line.get_ydata()[-1]:.2f}%" for line in plt.gca().lines[2:-2:2])
    st.write(markdown_string, unsafe_allow_html=True)
    st.pyplot(fig)
