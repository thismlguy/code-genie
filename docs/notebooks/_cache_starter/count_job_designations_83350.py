def count_job_designations(df):
    num_job_designations = df['job_title'].nunique()
    return num_job_designations