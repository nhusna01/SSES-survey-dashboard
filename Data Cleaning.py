import pandas as pd 
# Rename the column
df = df.rename(columns={
    'Timestamp': 'timestamp',
    'Username': 'username',
    'Age (Years)': 'age',
    'Gender': 'gender',
    'Marital Status': 'marital_status',
    'Highest Level of Education': 'education_level',
    'Employment Status': 'employment_status',
    'State': 'state',
    'Main Language Spoken at Home': 'home_language',

    'How often do you feel satisfied with your life as a whole these days?': 'life_satisfaction',
    'I have felt cheerful and in good spirits.': 'cheerful',
    'I have woken up feeling fresh and rested.': 'well_rested',
    'In general, how would you describe your overall health?': 'overall_health',

    'I often spend time with friends or family. ': 'social_time',
    'I often try to help others when they are in need.  ': 'helping_others',
    'People around me are supportive when I face difficulties.  ': 'social_support',
    'With enough effort everyone can increase their social skills. ': 'social_skills_growth',
    'I feel safe in my neighborhood.  ': 'neighborhood_safety',
    'People in my community care about one another. ': 'community_care',
    'I believe I can make a positive difference in my community.': 'community_impact',

    'I enjoy learning new things in my daily life.  ': 'enjoy_learning',
    'I am motivated to improve my skills and knowledge. ': 'self_motivation',

    'What are your main goals for the next few years? \n(Please answer in one word.)': 'future_goals',

    'I can stay calm even when under pressure.  ': 'calm_under_pressure',
    'I can control my emotions when I feel angry or upset.  ': 'emotional_control',
    'I find it easy to work well with others.  ': 'teamwork',
    'I finish tasks even when they are difficult.  ': 'task_persistence',
    'I can adapt easily to new or unexpected situations. ': 'adaptability',

    'Some people are just not good at interacting with others, no matter how hard they try. ': 'fixed_social_belief',
    'Everyone deserves equal opportunities to succeed.  ': 'equal_opportunity_belief',
    'I believe emotional well-being is as important as physical health.  ': 'wellbeing_belief',

    'How often do you participate in community, volunteer, or group activities?  ': 'community_participation',
    'How often do you spend time doing physical exercise or sports?  ': 'physical_activity'
})

# Replace weird dashes and spaces
df['age'] = (
    df['age']
    .astype(str)
    .str.replace('\u2013', '-', regex=False)   # en dash
    .str.replace('\u2014', '-', regex=False)   # em dash
    .str.replace('\xa0', ' ', regex=False)     # non-breaking space
    .str.strip()
)
 
# Check missing values
df.isnull().sum()

# Find duplicate columns (based on values)
columns_to_drop = df.T.duplicated()

# Get column names to drop
dup_cols = df.columns[columns_to_drop].tolist()

if dup_cols:
    print(f"Found duplicate columns (values are identical): {dup_cols}")
    df = df.loc[:, ~columns_to_drop]
    print("Duplicate columns dropped.")
else:
    print("No duplicate columns (with identical values) found.")

#drop unnecessary column
df = df.drop('timestamp', axis=1)
df = df.drop('Email Address', axis=1)
df

# Handling Outlier (Before)
import matplotlib.pyplot as plt

numeric_cols = df.select_dtypes(include='number')

plt.figure(figsize=(14,6))
numeric_cols.boxplot()
plt.title('Boxplots of Numerical Variables (Before Outlier Handling)')
plt.xticks(rotation=45)
plt.ylabel('Value')
plt.show()

# Outlier Count
def count_outliers_iqr(data):
    outlier_count = {}

    for col in data.columns:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = data[(data[col] < lower) | (data[col] > upper)]
        outlier_count[col] = len(outliers)

    return pd.DataFrame.from_dict(outlier_count, orient='index', columns=['Outlier_Count'])

outlier_summary = count_outliers_iqr(numeric_cols)
outlier_summary

# Handling Outlier (After)
import numpy as np

def cap_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    data[column] = np.where(
        data[column] < lower, lower,
        np.where(data[column] > upper, upper, data[column])
    )

numeric_cols = df.select_dtypes(include='number').columns

for col in numeric_cols:
    cap_outliers_iqr(df, col)

import matplotlib.pyplot as plt

plt.figure(figsize=(14,6))
df[numeric_cols].boxplot()
plt.title('Boxplots of Numerical Variables (After Outlier Handling)')
plt.xticks(rotation=45)
plt.ylabel('Value')
plt.show()



