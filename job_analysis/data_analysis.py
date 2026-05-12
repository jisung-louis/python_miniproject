import pandas as pd
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

print( job_demand_dict2022 )

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

# LQ지수( 비중으로 나타내는 ) 방식으로 정규화하자.
tjd2022 = job_demand2022['총 구인인원'].sum() # 전체 구인 인원
tg2022 = df_graduates2022['총 졸업자 수'].sum() # 전체 졸업자 수

newDf2022['LQ지수'] = (
    (newDf2022['총 구인인원'] / tjd2022 ) /
    (newDf2022['전공 졸업자 수'] / tg2022 )
).round(3)

plt.bar(newDf2022['전공'], newDf2022['LQ지수'], label='LQ지수', color="#0015ff")
# Y축 1.0에 기준선 추가
plt.axhline(1.0, color='red', linestyle='--', linewidth=2, label='전국 평균 (1.0)')
plt.xlabel('전공')
plt.ylabel('LQ지수')
plt.title('전공별 LQ지수')
plt.legend()
plt.xticks(rotation=45)
plt.show()



# #-------------------------------------------------2023---------------------------------------------
# # 전공계열별 직종 리스트 길이가 달라 딕셔너리를 행 단위의 리스트로 변환
# mjmList2023 = []
# for major, jobs in major_job_mapping.items():
#     for job in jobs:
#         mjmList2023.append({
#             '전공' : major,
#             '직종' : job,
#             '구인인원수' : job_demand_dict2023.get(job)
#         })

# # 전공, 직종, 구인인원
# df2023 = pd.DataFrame( mjmList2023 )

# # 결측치 재확인
# print( df2023.isnull().sum() )

# newDf2023 = df2023.groupby('전공')['구인인원수'].sum().reset_index().rename(columns={'구인인원수':'총 구인인원'})
# newDf2023['전공 졸업자 수'] = newDf2023['전공'].map(graduate_dict2023)
# newDf2023['졸업자대비구인비율'] = newDf2023['총 구인인원'] / newDf2023['전공 졸업자 수']

# #-------------------------------------------------2024---------------------------------------------
# # 전공계열별 직종 리스트 길이가 달라 딕셔너리를 행 단위의 리스트로 변환
# mjmList2024 = []
# for major, jobs in major_job_mapping.items():
#     for job in jobs:
#         mjmList2024.append({
#             '전공' : major,
#             '직종' : job,
#             '구인인원수' : job_demand_dict2024.get(job)
#         })

# # 전공, 직종, 구인인원
# df2024 = pd.DataFrame( mjmList2024 )

# # 결측치 재확인
# print( df2024.isnull().sum() )

# newDf2024 = df2024.groupby('전공')['구인인원수'].sum().reset_index().rename(columns={'구인인원수':'총 구인인원'})
# newDf2024['전공 졸업자 수'] = newDf2024['전공'].map(graduate_dict2024)
# newDf2024['졸업자대비구인비율'] = newDf2024['총 구인인원'] / newDf2024['전공 졸업자 수']

# # 전공별 갈 수 있는 직종 개수
# # df = pd.DataFrame( mjmList ).groupby('전공')['직종'].count()
# # print( df )

# # plt.bar( df.index, df.values )
# # plt.title('전공별 매핑 직종 수')
# # plt.xlabel('전공')
# # plt.ylabel('매핑된 직종 수')
# # plt.xticks(rotation=45)
# # plt.show()


# # 가설1. 산업·직종별 채용수요는 전공계열별 졸업생 공급과 일치하지 않을 것이다.
# -> 전공과 관련된 직무에 총 채용수요 / 졸업생수
# plt.bar(newDf2022['전공'], newDf2022['졸업자대비구인비율'], label='총 구인인원 / 전공 총 졸업자 수')
# plt.title('2022 전공별 졸업자대비구인비율')
# plt.xlabel('전공')
# plt.ylabel('졸업자대비구인비율')
# plt.xticks(rotation=45)
# plt.legend()
# plt.show()

# # 가설2. 2022~2024년 관련 직종의 채용수요가 증가한 전공계열은 취업률도 개선되는 경향을 보일 것이다.
# # 변화량을 가운데 선으로 두고 + - 된 것만큼 2022 -> 2023 / 2023 -> 2024
# # 35개의 전공에 대하여 각각 2개씩(2023년까지 변화량, 2024년까지 변화량)
# # 여기에 취업률에 관한 데이터 추가.

# 년도별 총 구인인원 수
volume_df = pd.DataFrame([
    {'년도' : 2022, '총 구인인원 수' : job_demand2022['총 구인인원'].sum() },
    {'년도' : 2023, '총 구인인원 수' : job_demand2023['총 구인인원'].sum() },
    {'년도' : 2024, '총 구인인원 수' : job_demand2024['총 구인인원'].sum() }
])

print( volume_df )