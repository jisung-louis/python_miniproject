import pandas as pd
# 1. 학교전공별취업진학통계
# 조사기준일, 중계열, 졸업자_계, 졸업자_남, 졸업자_여, 취업률_계, 취업률_남, 취업률_여 만 뽑아옴
df_employment2022 = pd.read_excel('./data/1학교전공별취업진학통계2022.xlsx', skiprows=13
                                  ,usecols=['조사기준일', '중계열', '졸업자_계', '취업자_합계_계']
                                  )
df_employment2023 = pd.read_excel('./data/1학교전공별취업진학통계2023.xlsx', skiprows=14 
                                  ,usecols=['조사기준일', '중계열', '졸업자_계', '취업자_합계_계']
                                  )
df_employment2024 = pd.read_excel('./data/1학교전공별취업진학통계2024.xlsx', skiprows=14
                                  ,usecols=['조사기준일', '중계열', '졸업자_계', '취업자_합계_계']
                                  )
print("-2022년 한교전공별취업진학통계-")
print( df_employment2022.head() )
print()
print("-2023년 한교전공별취업진학통계-")
print( df_employment2023.head() )
print()
print("-2024년 한교전공별취업진학통계-")
print( df_employment2024.head() )
print()
df_employment2022.info()
df_employment2023.info()
df_employment2024.info()

major_list = [] # 대계열/중계열/소계열/학과명 중에 중계열로 전공 리스트 생성

for major in df_employment2022['중계열']:
    if major not in major_list:
        major_list.append(major)
        
for major in df_employment2023['중계열']:
    if major not in major_list:
        major_list.append(major)
        
for major in df_employment2024['중계열']:
    if major not in major_list:
        major_list.append(major)
        
print("-전공 리스트-") # 35개의 전공
print( major_list )
print( f'전공 개수:{len(major_list)}개')



# 2. 산업분류별채용통계
# df_hire_by_industry2022 = pd.read_csv('./data/2산업분류별채용통계2022.csv', encoding='cp949')
# df_hire_by_industry2023 = pd.read_csv('./data/2산업분류별채용통계2023.csv', encoding='cp949')
# df_hire_by_industry2024 = pd.read_csv('./data/2산업분류별채용통계2024.csv', encoding='cp949')
# print("-2022년 산업분류별채용통계-")
# print( df_hire_by_industry2022.head() )
# print()
# print("-2023년 산업분류별채용통계-")
# print( df_hire_by_industry2023.head() )
# print()
# print("-2024년 산업분류별채용통계-")
# print( df_hire_by_industry2024.head() )
# print()
# df_hire_by_industry2022.info()
# df_hire_by_industry2023.info()
# df_hire_by_industry2024.info()

# 3. 직종분류별채용통계( encoding = cp949 )
df_hire_by_job2022 = pd.read_csv('./data/3직종분류별채용통계2022.csv', encoding='cp949')
df_hire_by_job2023 = pd.read_csv('./data/3직종분류별채용통계2023.csv', encoding='cp949')
df_hire_by_job2024 = pd.read_csv('./data/3직종분류별채용통계2024.csv', encoding='cp949')
print("-2022년 직종분류별채용통계-")
print( df_hire_by_job2022.head() )
print()
print("-2023년 직종분류별채용통계-")
print( df_hire_by_job2023.head() )
print()
print("-2024년 직종분류별채용통계-")
print( df_hire_by_job2024.head() )
print()
df_hire_by_job2022.info()
df_hire_by_job2023.info()
df_hire_by_job2024.info()

# 결측치 마지막 Unnamed 삭제
# df_hire_by_industry2022, df_hire_by_industry2023, df_hire_by_industry2024
df_list = [ df_hire_by_job2022, df_hire_by_job2023, df_hire_by_job2024 ]
for df in df_list:
    df.drop(columns=['Unnamed: 11'], inplace=True, errors='ignore')
    print( df.isnull().sum() ) # 결측치 확인
    print() # 보기 쉽게 한 줄 띄움

job_list = [] # 직종 리스트

# for job in df_hire_by_job2022['직종별']:
#     if job not in job_list:
#         job_list.append(job)
        
# for job in df_hire_by_job2023['직종별']:
#     if job not in job_list:
#         job_list.append(job)
        
# for job in df_hire_by_job2024['직종별']:
#     if job not in job_list:
#         job_list.append(job)

# print('--직업 종류--') # 182개의 직업이 존재한다.
# print( job_list )
# print( f'직업 개수:{len(job_list)}개')


# 필요한 데이터만 따로 csv 파일로 저장하기

# 1.전공 졸업자 수만 따로 저장
df_graduates2022 =(
    df_employment2022
    .groupby('중계열')[['졸업자_계', '취업자_합계_계' ]]
    .sum()
    .reset_index()
    .rename(columns={
        '중계열' : '전공',
        '졸업자_계' : '총 졸업자 수',
        '취업자_합계_계' : '총 취업자 수' 
        })
)
# 취업률 파생속성 만들기
df_graduates2022['취업률'] = ( df_graduates2022['총 취업자 수'] / df_graduates2022['총 졸업자 수'] * 100 ).round(2)
# 조사년도 넣기
df_graduates2022['조사년도'] = df_employment2022['조사기준일'].str[:4]

df_graduates2023 =(
    df_employment2023
    .groupby('중계열')[['졸업자_계', '취업자_합계_계' ]]
    .sum()
    .reset_index()
    .rename(columns={
        '중계열' : '전공',
        '졸업자_계' : '총 졸업자 수',
        '취업자_합계_계' : '총 취업자 수' 
        })
)
# 취업률 파생속성 만들기
df_graduates2023['취업률'] = ( df_graduates2023['총 취업자 수'] / df_graduates2023['총 졸업자 수'] * 100 ).round(2)
# 조사년도 넣기
df_graduates2023['조사년도'] = df_employment2023['조사기준일'].str[:4]

df_graduates2024 =(
    df_employment2024
    .groupby('중계열')[['졸업자_계', '취업자_합계_계' ]]
    .sum()
    .reset_index()
    .rename(columns={
        '중계열' : '전공',
        '졸업자_계' : '총 졸업자 수',
        '취업자_합계_계' : '총 취업자 수' 
        })
)
# 취업률 파생속성 만들기
df_graduates2024['취업률'] = ( df_graduates2024['총 취업자 수'] / df_graduates2024['총 졸업자 수'] * 100 ).round(2)
# 조사년도 넣기
df_graduates2024['조사년도'] = df_employment2024['조사기준일'].str[:4]

df_graduates2022.to_csv('./data/df_graduates2022.csv', index=False, encoding='utf-8')
df_graduates2023.to_csv('./data/df_graduates2023.csv', index=False, encoding='utf-8')
df_graduates2024.to_csv('./data/df_graduates2024.csv', index=False, encoding='utf-8')

target_scales = ['5규모(300인이상)', '중소규모(5~299인)']
# 2. 직무별 채용수요만 따로 저장
job_demand2022 = (
    df_hire_by_job2022[ df_hire_by_job2022['시도별(17개)'] == '전국' ]
    .groupby('직종별')['구인인원[명]']
    .sum().reset_index()
    .rename(columns={'직종별' : '직종', '구인인원[명]' : '총 구인인원'})
)
job_demand2022['조사년도'] = df_hire_by_job2022['시점'].str[:4]

job_demand2023 = (
    df_hire_by_job2023[ df_hire_by_job2022['시도별(17개)'] == '전국' ]
    .groupby('직종별')['구인인원[명]']
    .sum().reset_index()
    .rename(columns={'직종별' : '직종', '구인인원[명]' : '총 구인인원'})
)
job_demand2023['조사년도'] = df_hire_by_job2023['시점'].str[:4]

job_demand2024 = (
    df_hire_by_job2024[ df_hire_by_job2022['시도별(17개)'] == '전국' ]
    .groupby('직종별')['구인인원[명]']
    .sum().reset_index()
    .rename(columns={'직종별' : '직종', '구인인원[명]' : '총 구인인원'})
)
job_demand2024['조사년도'] = df_hire_by_job2024['시점'].str[:4]

job_demand2022.to_csv('./data/job_demand2022.csv', index=False, encoding='utf-8')
job_demand2023.to_csv('./data/job_demand2023.csv', index=False, encoding='utf-8')
job_demand2024.to_csv('./data/job_demand2024.csv', index=False, encoding='utf-8')


# 리스트끼리 비교한 결과: 다 대 다 관계로 전공과 직무가 매핑된다.
# 매핑 딕셔너리(major_job_mapping)를 따로 파일에 저장시킨 뒤 꺼내오는 방식으로 진행!
