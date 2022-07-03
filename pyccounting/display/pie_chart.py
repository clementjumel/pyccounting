import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


def _plot_pie(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots()

    categories = [category for category in sorted(set(df["category"])) if category]
    all_sizes, total_size = [], 0.0
    for category in categories:
        size = 0.0
        for _, row in df.loc[df["category"] == category].iterrows():
            size += abs(row["amount"])
        all_sizes.append(size)
        total_size += size

    labels, sizes = [], []
    other_size = 0.0
    for category, size in zip(categories, all_sizes):
        if size / total_size > 0.03:
            labels.append(category)
            sizes.append(size)
        else:
            other_size += size
    if other_size:
        labels.append("other")
        sizes.append(other_size)

    ax.pie(sizes, labels=labels, autopct="%1.1f%%", shadow=True, startangle=90)
    ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig=fig)


def pie_chart(df: pd.DataFrame, types: list[str]) -> None:
    for type_ in [type_ for type_ in types if type_ != "expenses & incomes"]:
        st.write(f"### {type_.capitalize()}")
        if type_ == "expenses":
            df_ = df.loc[df["amount"] < 0]
        elif type_ == "incomes":
            df_ = df.loc[df["amount"] >= 0]
        else:
            raise ValueError

        _plot_pie(df=df_)
