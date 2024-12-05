import pandas as pd


def long_to_wide(frame, n, col_names=None):
    """reshape long to wide format, transposing groups of n rows into columns"""
    base_index = pd.RangeIndex(len(frame)).to_series()
    group_level = base_index.floordiv(n)
    column_level = base_index.mod(n)

    if col_names:
        assert (
            len(col_names) == len(set(col_names)) == n
        ), "col_names must be unique and have the same length as n"
        column_level = column_level.map(dict(enumerate(col_names)))

    return (
        frame.set_index([group_level, column_level], append=True)
        .unstack()
        .droplevel(-1)
    )


def wide_to_long(frame):
    """reshape the joined wide sentence-answer frame to long format"""
    frame_long = frame.set_index("sentence", append=True).stack().rename("answer")
    return frame_long.reset_index(2).droplevel(-1)
