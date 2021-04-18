from itertools import repeat

import plotly.graph_objects as go


def plot_violin(
    data,
    names=None,
    colors=None,
    violin_kwargs: dict = None,
    layout_kwargs: dict = None,
):
    names = names if names is not None else repeat(None)
    colors = colors if colors is not None else repeat(None)
    layout_kwargs = layout_kwargs if layout_kwargs is not None else {}
    violin_kwargs = violin_kwargs if violin_kwargs is not None else {}

    fig = go.Figure()

    ridgeplot = True

    for dist, name, color in zip(data, names, colors):

        defaults_violin = dict(
            fillcolor=color,
            line_color="black" if color else None,
            line_width=1.5,
            points=False,
            name=name,
            # TODO: manual line based on beta_mean
            # meanline_visible=True,
            hoveron="violins",
            hoverinfo="x+y",
            hovertext="foo",
            hoverlabel={"namelength": -1},
            # spanmode="hard",
            width=1.8 if ridgeplot else None,
        )
        defaults_violin.update(violin_kwargs)
        if ridgeplot:
            fig.add_trace(go.Violin(x=dist, **defaults_violin, side="positive"))
        else:
            fig.add_trace(go.Violin(y=dist, **defaults_violin))

    kwargs = dict(
        # title="Beta Distributions for Sub-Groups",
        # height=700,
        # legend_title="Legend Title",
        # xaxis_title=metric.upper() if ridgeplot else None,
        # yaxis_title=None if ridgeplot else metric.upper(),
        xaxis_showticklabels=True if ridgeplot else False,
        yaxis_showticklabels=False if ridgeplot else True,
        hovermode="y unified" if ridgeplot else "x unified",
        xaxis_showgrid=True,
        xaxis_zeroline=False,
        plot_bgcolor="rgba(255, 255, 255, 0.0)",
        xaxis_gridcolor="rgba(0, 0, 0, 0.1)",
        yaxis_gridcolor="rgba(0, 0, 0, 0.1)",
        # legend={"font_size":10}
    )
    kwargs.update(layout_kwargs)
    fig.update_layout(kwargs)

    # fig.show()
    return fig
