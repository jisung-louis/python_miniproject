import pandas as pd
import json

df_2022 = pd.read_excel('./data/1학교전공별취업진학통계2022.xlsx', sheet_name='학교별 학과별', skiprows=13)
df_2023 = pd.read_excel('./data/1학교전공별취업진학통계2023.xlsx', sheet_name='학교별 학과별', skiprows=14)
df_2024 = pd.read_excel('./data/1학교전공별취업진학통계2024.xlsx', sheet_name='학교별', skiprows=14)

df_2022['연도'] = 2022
df_2023['연도'] = 2023
df_2024['연도'] = 2024
df = pd.concat([df_2022, df_2023, df_2024], ignore_index=True)

cols = ['연도', '대계열', '중계열', '취업률_계',
        '1차 유지취업률_계', '2차 유지취업률_계',
        '3차 유지취업률_계', '4차 유지취업률_계']
data = df[cols].copy()

num_cols = cols[3:]
for c in num_cols:
    data[c] = pd.to_numeric(data[c], errors='coerce').fillna(0)

# 0 제외하고 실제 데이터만 평균 (0은 무응답으로 간주)
clean = data[data['취업률_계'] > 0]

result = {
    'total_rows': len(data),
    'rows_in_10k': round(len(data)/10000, 1),
    'unique_중계열': data['중계열'].nunique(),
    'unique_대계열': data['대계열'].nunique(),
    'mean_취업률': round(clean['취업률_계'].mean(), 1),
    'mean_1차': round(clean['1차 유지취업률_계'].mean(), 1),
    'mean_2차': round(clean['2차 유지취업률_계'].mean(), 1),
    'mean_3차': round(clean['3차 유지취업률_계'].mean(), 1),
    'mean_4차': round(clean['4차 유지취업률_계'].mean(), 1),
    'corr_취업률_1차': round(clean['취업률_계'].corr(clean['1차 유지취업률_계']), 2),
    'corr_취업률_2차': round(clean['취업률_계'].corr(clean['2차 유지취업률_계']), 2),
    'corr_취업률_3차': round(clean['취업률_계'].corr(clean['3차 유지취업률_계']), 2),
    'corr_취업률_4차': round(clean['취업률_계'].corr(clean['4차 유지취업률_계']), 2),
}
result['gap_취업률_4차'] = round(result['mean_취업률'] - result['mean_4차'], 1)

with open('_eda.txt', 'w', encoding='utf-8') as f:
    f.write(json.dumps(result, ensure_ascii=False, indent=2))
