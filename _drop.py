import pandas as pd

df_2022 = pd.read_excel('./data/1학교전공별취업진학통계2022.xlsx', sheet_name='학교별 학과별', skiprows=13)
df_2023 = pd.read_excel('./data/1학교전공별취업진학통계2023.xlsx', sheet_name='학교별 학과별', skiprows=14)
df_2024 = pd.read_excel('./data/1학교전공별취업진학통계2024.xlsx', sheet_name='학교별', skiprows=14)
df_2022['연도']=2022; df_2023['연도']=2023; df_2024['연도']=2024
df = pd.concat([df_2022, df_2023, df_2024], ignore_index=True)

cols = ['중계열', '1차 유지취업률_계', '4차 유지취업률_계']
data = df[cols].copy()
for c in cols[1:]:
    data[c] = pd.to_numeric(data[c], errors='coerce').fillna(0)

g = data.groupby('중계열').agg(
    유지1차=('1차 유지취업률_계', 'mean'),
    유지4차=('4차 유지취업률_계', 'mean')
).reset_index()
g['하락폭'] = g['유지1차'] - g['유지4차']

with open('_out.txt', 'w', encoding='utf-8') as f:
    f.write("하락 폭 큰 순 TOP 5:\n")
    f.write(g.nlargest(5, '하락폭')[['중계열','유지1차','유지4차','하락폭']].to_string() + "\n\n")
    f.write("하락 폭 작은 순 TOP 5:\n")
    f.write(g.nsmallest(5, '하락폭')[['중계열','유지1차','유지4차','하락폭']].to_string() + "\n\n")
    f.write(f"최대 하락폭: {g['하락폭'].max():.2f}\n")
    f.write(f"최소 하락폭: {g['하락폭'].min():.2f}\n")
    f.write(f"차이: {g['하락폭'].max() - g['하락폭'].min():.2f}\n")
    f.write(f"평균 하락폭: {g['하락폭'].mean():.2f}\n")
