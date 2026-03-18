def normalize(df):
    return (df - df.min()) / (df.max() - df.min())