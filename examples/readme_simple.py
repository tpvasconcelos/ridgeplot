def main() -> None:
    import numpy as np

    from ridgeplot import ridgeplot

    # Put your real samples here...
    np.random.seed(0)
    synthetic_samples = [
        [np.random.normal((i + n) / 1.6, scale=np.random.uniform(0.6), size=600) for i in (4, 2, 0)]
        for n in range(22, 0, -3)
    ]

    # Call the `ridgeplot()` helper, packed with sensible defaults
    fig = ridgeplot(samples=synthetic_samples)

    # The returned Plotly `Figure` is still fully customizable
    fig.update_layout(height=500, width=800)

    # show us the work!
    fig.show()


if __name__ == "__main__":
    main()
