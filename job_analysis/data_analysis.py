import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import koreanfont
from mjm import major_job_mapping # 딕셔너리 가져오기
# 매핑된 데이터분석 및 시각화

# 전공별 총 졸업자 수 df
df_graduates2022 = pd.read_csv('./data/df_graduates2022.csv', encoding='utf-8')
df_graduates2023 = pd.read_csv('./data/df_graduates2023.csv', encoding='utf-8')
df_graduates2024 = pd.read_csv('./data/df_graduates2024.csv', encoding='utf-8')

# 직종별 총 채용수요 df
job_demand2022 = pd.read_csv('./data/job_demand2022.csv', encoding='utf-8', dtype={'직업코드':str})
job_demand2023 = pd.read_csv('./data/job_demand2023.csv', encoding='utf-8', dtype={'직업코드':str})
job_demand2024 = pd.read_csv('./data/job_demand2024.csv', encoding='utf-8', dtype={'직업코드':str})

print( "=====2022 전공별 총 졸업자 수=====")
print( df_graduates2022.head() )
print( "=====2023 전공별 총 졸업자 수=====")
print( df_graduates2023.head() )
print( "=====2024 전공별 총 졸업자 수=====")
print( df_graduates2024.head() )
print()
print()
print( "=====2022 직종별 채용인원 수=====")
print( job_demand2022.head() )
print( "=====2023 직종별 채용인원 수=====")
print( job_demand2023.head() )
print( "=====2024 직종별 채용인원 수=====")
print( job_demand2024.head() )

# 각 파일이 똑같은 형식으로 저장되어 있으므로 대표되는 파일의 info만 확인
df_graduates2022.info()
job_demand2022.info()

# 각 파일을 딕셔너리 화
graduate_dict2022 = df_graduates2022.set_index('전공')['총 졸업자 수'].to_dict()
graduate_dict2023 = df_graduates2023.set_index('전공')['총 졸업자 수'].to_dict()
graduate_dict2024 = df_graduates2024.set_index('전공')['총 졸업자 수'].to_dict()
job_demand_dict2022 = job_demand2022.set_index('직업코드')['총 구인인원'].to_dict()
job_demand_dict2023 = job_demand2023.set_index('직업코드')['총 구인인원'].to_dict()
job_demand_dict2024 = job_demand2024.set_index('직업코드')['총 구인인원'].to_dict()

#-------------------------------------------------2022---------------------------------------------
# 전공계열별 직종 리스트 길이가 달라 딕셔너리를 행 단위의 리스트로 변환
mjmList2022 = []
for major, jobs in major_job_mapping.items():
    for job in jobs:
        jobcode = job.split()[0]

        mjmList2022.append({
            '전공' : major,
            '직종' : job,
            '구인인원수' : job_demand_dict2022.get(jobcode)
        })

# 전공, 직종, 구인인원
df2022 = pd.DataFrame( mjmList2022 )

# 결측치 재확인
print( df2022.isnull().sum() )

newDf2022 = df2022.groupby('전공')['구인인원수'].sum().reset_index().rename(columns={'구인인원수':'총 구인인원'})
newDf2022['전공 졸업자 수'] = newDf2022['전공'].map(graduate_dict2022)
newDf2022['졸업자대비구인비율'] = newDf2022['총 구인인원'] / newDf2022['전공 졸업자 수']

#-------------------------------------------------2023---------------------------------------------
# 전공계열별 직종 리스트 길이가 달라 딕셔너리를 행 단위의 리스트로 변환
mjmList2023 = []
for major, jobs in major_job_mapping.items():
    for job in jobs:
        jobcode = job.split()[0]

        mjmList2023.append({
            '전공' : major,
            '직종' : job,
            '구인인원수' : job_demand_dict2023.get(jobcode)
        })
# 전공, 직종, 구인인원
df2023 = pd.DataFrame( mjmList2023 )

newDf2023 = df2023.groupby('전공')['구인인원수'].sum().reset_index().rename(columns={'구인인원수':'총 구인인원'})
newDf2023['전공 졸업자 수'] = newDf2023['전공'].map(graduate_dict2023)
newDf2023['졸업자대비구인비율'] = newDf2023['총 구인인원'] / newDf2023['전공 졸업자 수']

#-------------------------------------------------2024---------------------------------------------
# 전공계열별 직종 리스트 길이가 달라 딕셔너리를 행 단위의 리스트로 변환
mjmList2024 = []
for major, jobs in major_job_mapping.items():
    for job in jobs:
        jobcode = job.split()[0]

        mjmList2024.append({
            '전공' : major,
            '직종' : job,
            '구인인원수' : job_demand_dict2024.get(jobcode)
        })
# 전공, 직종, 구인인원
df2024 = pd.DataFrame( mjmList2024 )

newDf2024 = df2024.groupby('전공')['구인인원수'].sum().reset_index().rename(columns={'구인인원수':'총 구인인원'})
newDf2024['전공 졸업자 수'] = newDf2024['전공'].map(graduate_dict2024)
newDf2024['졸업자대비구인비율'] = newDf2024['총 구인인원'] / newDf2024['전공 졸업자 수']


# 가설1. 산업·직종별 채용수요는 전공계열별 졸업생 공급과 일치하지 않을 것이다.
# -> 전공과 관련된 직무에 총 채용수요 / 졸업생수
# -> 전공마다 갈 수 있는 직종의 수가 많아 채용수요보다 항상 적다.
# -> 그 전공이 전체 졸업생 중 어느정도 차지하는지와 직무도 또한 모든 직무 중에 어느정도 차지하는 지 따진 LQ지수로 확인해보았다.
# LQ지수( 비중으로 나타내는 ) 방식으로 정규화하자.
tjd2022 = job_demand2022['총 구인인원'].sum() # 전체 구인 인원
tg2022 = df_graduates2022['총 졸업자 수'].sum() # 전체 졸업자 수

tjd2023 = job_demand2023['총 구인인원'].sum() # 전체 구인 인원
tg2023 = df_graduates2023['총 졸업자 수'].sum() # 전체 졸업자 수

tjd2024 = job_demand2024['총 구인인원'].sum() # 전체 구인 인원
tg2024 = df_graduates2024['총 졸업자 수'].sum() # 전체 졸업자 수


newDf2022['LQ지수'] = (
    (newDf2022['총 구인인원'] / tjd2022 ) /
    (newDf2022['전공 졸업자 수'] / tg2022 )
).round(3)

newDf2023['LQ지수'] = (
    (newDf2023['총 구인인원'] / tjd2023 ) /
    (newDf2023['전공 졸업자 수'] / tg2023 )
).round(3)

newDf2024['LQ지수'] = (
    (newDf2024['총 구인인원'] / tjd2024 ) /
    (newDf2024['전공 졸업자 수'] / tg2024 )
).round(3)

# 년도 칼럼 추가
newDf2022['년도'] = 2022
newDf2023['년도'] = 2023
newDf2024['년도'] = 2024

# df_filtered = pd.concat([newDf2022, newDf2023, newDf2024])
totalDf = pd.concat([newDf2022, newDf2023, newDf2024], ignore_index=True)

# 전공별 3년 평균 LQ 및 졸업자 수 계산
df_supply = totalDf.groupby('전공')[['LQ지수', '전공 졸업자 수']].mean().round(2).reset_index()
df_supply['전공 졸업자 수'] = df_supply['전공 졸업자 수'].round(0)

df_supply_filtered = df_supply[df_supply['LQ지수'] <= 2.0].copy()

print( df_supply )

plt.figure(figsize=(14, 6))

plt.bar(df_supply_filtered['전공'], df_supply_filtered['LQ지수'], label='LQ지수', color="skyblue")
# # Y축 1.0에 기준선 추가
plt.axhline(1.0, color='red', linestyle='--', linewidth=2, label='전국 평균 LQ지수 (1.0)')
plt.xlabel('전공')
plt.ylabel('LQ지수')
plt.title('전공별 LQ지수 (2.0 이하 전공만)')
plt.legend()
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


# 가설2. 2022~2024년 관련 직종의 채용수요가 증가한 전공계열은 취업률도 개선되는 경향을 보일 것이다.
# 변화량을 가운데 선으로 두고 + - 된 것만큼 2022 -> 2023 / 2023 -> 2024
# 34개의 전공에 대하여 각각 2개씩(2023년까지 변화량, 2024년까지 변화량)
# 구인인원 수가 증가한 전공계열
# 실제로 전공에서 취업률도 개선되는 지 확인
# 해석결과: 대부분 채용수요가 높아져도 취업률이 낮아지는 걸로 보아, 



df_pivot = totalDf.pivot(index='전공', columns='년도', values='총 구인인원')

df_pivot['2023-2022 차이'] = df_pivot[2023] - df_pivot[2022]
df_pivot['2024-2023 차이'] = df_pivot[2024] - df_pivot[2023]

df_pivot['2023 변화율(%)'] = ((df_pivot[2023] - df_pivot[2022]) / df_pivot[2022] * 100).round(2)
df_pivot['2024 변화율(%)'] = ((df_pivot[2024] - df_pivot[2023]) / df_pivot[2023] * 100).round(2)

df_pivot = df_pivot.reset_index()

print( df_pivot.head() )
print( df_pivot.isnull().sum() )

lq_mean = df_supply[['전공', 'LQ지수']].rename(columns={'LQ지수': '평균_LQ지수'})

df_pivot = df_pivot.merge(
    lq_mean,
    on='전공',
    how='left'
)

df_pivot = df_pivot[df_pivot['평균_LQ지수'] <= 2.0].copy()

graduates_all = pd.concat(
    [df_graduates2022, df_graduates2023, df_graduates2024],
    ignore_index=True
)

graduates_all['조사년도'] = graduates_all['조사년도'].astype(int)

emp_pivot = graduates_all.pivot(
    index='전공',
    columns='조사년도',
    values='취업률'
).reset_index()

emp_pivot['취업률차이_2023'] = emp_pivot[2023] - emp_pivot[2022]
emp_pivot['취업률차이_2024'] = emp_pivot[2024] - emp_pivot[2023]

df_pivot = df_pivot.merge(
    emp_pivot[['전공', '취업률차이_2023', '취업률차이_2024']],
    on='전공',
    how='left'
)

print(df_pivot[['전공', '2023 변화율(%)', '2024 변화율(%)', '취업률차이_2023', '취업률차이_2024', '평균_LQ지수']].head())

# 그래프

df_plot = df_pivot.dropna(
    subset=[
        '2023 변화율(%)',
        '2024 변화율(%)',
        '취업률차이_2023',
        '취업률차이_2024'
    ]
).copy()

df_plot = df_plot.sort_values('2023 변화율(%)', ascending=False).reset_index(drop=True)

x = np.arange(len(df_plot['전공']))
bar_width = 0.35

# -------------------------------------------------
# 그래프 그리기
# -------------------------------------------------

fig, ax1 = plt.subplots(figsize=(18, 9))

plt.title('2022~2024 전공별 채용수요 변화율 vs 취업률 변화량', fontsize=18, pad=20)

# 왼쪽 막대: 2022 -> 2023 채용수요 변화율
ax1.bar(
    x - bar_width / 2,
    df_plot['2023 변화율(%)'],
    width=bar_width,
    alpha=0.5,
    color='skyblue',
    label='채용수요 변화율: 2022→2023'
)

# 오른쪽 막대: 2023 -> 2024 채용수요 변화율
ax1.bar(
    x + bar_width / 2,
    df_plot['2024 변화율(%)'],
    width=bar_width,
    alpha=0.5,
    color='lightgray',
    label='채용수요 변화율: 2023→2024'
)

ax1.axhline(0, color='gray', linestyle='-', linewidth=1)
ax1.set_ylabel('채용수요 변화율 (%)', fontsize=13, fontweight='bold')
ax1.set_xlabel('전공 계열', fontsize=13)

ax1.set_xticks(x)
ax1.set_xticklabels(df_plot['전공'], rotation=45, ha='right')

ax1.grid(axis='y', linestyle='--', alpha=0.3)


# -------------------------------------------------
# 오른쪽 y축: 취업률 변화량 점 그래프
# -------------------------------------------------

ax2 = ax1.twinx()

# 2022 -> 2023 취업률 변화량 점
ax2.scatter(
    x - bar_width / 2,
    df_plot['취업률차이_2023'],
    color='firebrick',
    s=80,
    label='취업률 변화량: 2022→2023',
    zorder=5
)

# 2023 -> 2024 취업률 변화량 점
ax2.scatter(
    x + bar_width / 2,
    df_plot['취업률차이_2024'],
    color='darkorange',
    s=80,
    label='취업률 변화량: 2023→2024',
    zorder=5
)

ax2.axhline(0, color='firebrick', linestyle='--', linewidth=1, alpha=0.5)
ax2.set_ylabel('취업률 변화량 (%p)', fontsize=13, color='firebrick', fontweight='bold')
ax2.tick_params(axis='y', labelcolor='firebrick')


# -------------------------------------------------
# 범례 통합
# -------------------------------------------------

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

ax1.legend(
    lines1 + lines2,
    labels1 + labels2,
    loc='upper right',
    fontsize=11
)

fig.tight_layout()
plt.show()