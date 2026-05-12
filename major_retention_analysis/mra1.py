import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import koreanfont

# 연도별 파일 읽기
df_2022 = pd.read_excel('./data/1학교전공별취업진학통계2022.xlsx', sheet_name='학교별 학과별', skiprows=13)
df_2023 = pd.read_excel('./data/1학교전공별취업진학통계2023.xlsx', sheet_name='학교별 학과별', skiprows=14)
df_2024 = pd.read_excel('./data/1학교전공별취업진학통계2024.xlsx', sheet_name='학교별', skiprows=14)

# 연도 컬럼 추가
df_2022['연도'] = 2022
df_2023['연도'] = 2023
df_2024['연도'] = 2024

# 합치기
df = pd.concat([df_2022, df_2023, df_2024], ignore_index=True)

# 필요한 컬럼 선택
cols = ['연도', '대계열', '중계열', '취업률_계',
        '1차 유지취업률_계', '2차 유지취업률_계',
        '3차 유지취업률_계', '4차 유지취업률_계']

# 데이터 복사
data = df[cols].copy()

# 숫자형 컬럼으로 변환 (문자열로 되어 있는 경우)
num_cols = cols[4:]
for c in num_cols:
    data[c] = pd.to_numeric(data[c], errors='coerce').fillna(0)

# 가설1 취업률이 높은 전공계열이라도 4차 유지취업률이 낮은 경우가 존재할 것이다.

grouped = data.groupby('중계열').agg(
    취업률=('취업률_계', 'mean'), # 중계열별 평균 취업률
    유지4차=('4차 유지취업률_계', 'mean') # 중계열별 평균 4차 유지취업률
).reset_index()

# 평균값 계산
x_mean = grouped['취업률'].mean()  # 전체 평균 취업률
print(x_mean)
y_mean = grouped['유지4차'].mean() # 전체 평균 4차 유지취업률
print(y_mean)

plt.figure(figsize=(10, 7))

# 1. 기본 점들 (회색)
plt.scatter(grouped['취업률'], grouped['유지4차'], color='blue', s=80)

# 2. 4분면 선 (평균선)
plt.axvline(x_mean, color='black', linestyle='--', alpha=0.5)
plt.axhline(y_mean, color='black', linestyle='--', alpha=0.5)

# 3. 가설 영역 (오른쪽 아래) 빨강
target = grouped[(grouped['취업률'] > x_mean) & (grouped['유지4차'] < y_mean)]
plt.scatter(target['취업률'], target['유지4차'], color='red', s=120)

# 4. 빨간 점에 이름 표시
for _, row in target.iterrows():
    plt.text(row['취업률']+0.2, row['유지4차'], row['중계열'], fontsize=9)
    print(row['중계열'], row['취업률'], row['유지4차'])

plt.xlabel('취업률 (%)')
plt.ylabel('4차 유지취업률 (%)')
plt.title('취업률 vs 4차 유지취업률')
plt.show()

# 가설2  전공계열별로 1차 유지취업률에서 4차 유지취업률로 갈수록 하락 폭에 차이가 있을 것이다.

# 중계열별 1~4차 평균 계산
grouped2 = data.groupby('중계열').agg(
    유지1차=('1차 유지취업률_계', 'mean'),
    유지2차=('2차 유지취업률_계', 'mean'),
    유지3차=('3차 유지취업률_계', 'mean'),
    유지4차=('4차 유지취업률_계', 'mean')
).reset_index()

# 하락 폭 계산
grouped2['하락폭'] = grouped2['유지1차'] - grouped2['유지4차']

plt.figure(figsize=(10, 8))
sorted_data = grouped2.sort_values('하락폭', ascending=True)
print(grouped2.sort_values('하락폭', ascending=False)[['중계열','유지1차','유지4차','하락폭']])
plt.barh(sorted_data['중계열'], sorted_data['하락폭'])
plt.xlabel('하락 폭 (1차 - 4차) %p')
plt.title('중계열별 유지취업률 하락 폭')
plt.tight_layout()
plt.show()