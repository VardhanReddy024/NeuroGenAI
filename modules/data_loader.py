import pandas as pd

def preprocess(df):
    # Convert dates
    df['Admission_Date'] = pd.to_datetime(df['Admission_Date'])
    df['Discharge_Date'] = pd.to_datetime(df['Discharge_Date'])

    # Create Length of Stay
    df['Length_of_Stay'] = (
        df['Discharge_Date'] - df['Admission_Date']
    ).dt.days

    return df