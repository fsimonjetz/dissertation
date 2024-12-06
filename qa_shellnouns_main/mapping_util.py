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


def add_sentence_index(frame):
    return frame.groupby(level=["batch", "file"]).apply(
        lambda f: f.reset_index(drop=True).rename_axis("sent_index")
    )


def get_mapped_sent_indexes(frame):
    # drop all indexes except for the sent_index
    reindexed = frame.set_index(frame.reset_index().sent_index)

    return reindexed.idxmax()


def get_prediction(scores):
    """
    Get the top-voted sentence, preferring the sentence closest to
    (but preceding) the SN sentence in case of ties.
    """

    top_sents = (
        scores.groupby(level=["batch", "file"])
        .apply(get_mapped_sent_indexes)
        .mode(axis=1)
    )

    # create a mask that only includes sentences preceding the SN sentence
    shellnoun_sents = scores.reset_index()
    shellnoun_sents = shellnoun_sents[shellnoun_sents.is_sn_sent].sent_index

    m = top_sents.ge(shellnoun_sents.values[:, None])

    # but always include the first column (in order to avoid empty rows)
    m[0] = False

    prediction = top_sents.mask(m).ffill(axis=1)

    return prediction.astype(int).iloc[:, -1]
