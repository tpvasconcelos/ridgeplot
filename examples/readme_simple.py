from numpy.random import normal

from ridgeplot import ridgeplot


def main() -> None:
    # Put your real samples here...
    synthetic_samples = [normal(n / 1.2, size=600) for n in reversed(range(9))]

    # The `ridgeplot()` helper comes packed with sensible defaults
    fig = ridgeplot(samples=synthetic_samples)

    # and the returned Plotly figure is still fully customizable
    fig.update_layout(height=500, width=800)

    # show us the work!!
    fig.show()


if __name__ == "__main__":
    main()
