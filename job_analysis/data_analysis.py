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
job_demand2022 = pd.read_csv('./data/job_demand2022.csv', encoding='utf-8')
job_demand2023 = pd.read_csv('./data/job_demand2023.csv', encoding='utf-8')
job_demand2024 = pd.read_csv('./data/job_demand2024.csv', encoding='utf-8')

print( "=====2022 전공별 총 졸업자 수=====")
print( df_graduates2022 )
print( "=====2023 전공별 총 졸업자 수=====")
print( df_graduates2023 )
print( "=====2024 전공별 총 졸업자 수=====")
print( df_graduates2024 )
print()
print()
print( "=====2022 직종별 채용인원 수=====")
print( job_demand2022 )
print( "=====2023 직종별 채용인원 수=====")
print( job_demand2023 )
print( "=====2024 직종별 채용인원 수=====")
print( job_demand2024 )

df_graduates2022.info()
job_demand2022.info()


graduate_dict2022 = df_graduates2022.set_index('전공')['총 졸업자 수'].to_dict()
graduate_sum = 0
for i in graduate_dict2022.values():
    graduate_sum += i
job_demand_dict2022 = job_demand2022.set_index('직종')['총 구인인원'].to_dict()
job_sum = 0
for i in job_demand_dict2022.values():
    job_sum += i

print( f'총 졸업자 수:{graduate_sum} vs 총 구인구직자 수: {job_sum}')

# 전공계열별 직종 리스트 길이가 달라 딕셔너리를 행 단위의 리스트로 변환
mjmList2022 = []
for major, jobs in major_job_mapping.items():
    for job in jobs:
        mjmList2022.append({
            '전공' : major,
            '직종' : job,
            '구인인원수' : job_demand_dict2022.get(job)
        })

# 전공, 직종, 구인인원
df2022 = pd.DataFrame( mjmList2022 )
newDf2022 = df2022.groupby('전공')['구인인원수'].sum().reset_index().rename(columns={'구인인원수':'총 구인인원'})
newDf2022['전공 졸업자 수'] = newDf2022['전공'].map(graduate_dict2022)
newDf2022['졸업자대비구인비율'] = newDf2022['총 구인인원'] / newDf2022['전공 졸업자 수']

plt.bar(newDf2022['전공'], newDf2022['졸업자대비구인비율'], label='총 구인인원 / 전공 총 졸업자 수')
plt.title('2022 전공별 졸업자대비구인비율')
plt.xlabel('전공')
plt.ylabel('졸업자대비구인비율')
plt.xticks(rotation=45)
plt.legend()
plt.show()



# 전공별 총 직업 수요와 졸업률 비교


# # 결측치 재확인
# print( df.isnull().sum() )
    


# 전공별 갈 수 있는 직종 개수
# df = pd.DataFrame( mjmList ).groupby('전공')['직종'].count()
# print( df )


# plt.bar( df.index, df.values )
# plt.title('전공별 매핑 직종 수')
# plt.xlabel('전공')
# plt.ylabel('매핑된 직종 수')
# plt.xticks(rotation=45)
# plt.show()


# 가설1. 산업·직종별 채용수요는 전공계열별 졸업생 공급과 일치하지 않을 것이다.
# -> 전공과 관련된 직무에 총 채용수요 / 졸업생수
# 가설2. 2022~2024년 관련 직종의 채용수요가 증가한 전공계열은 취업률도 개선되는 경향을 보일 것이다.