import pandas as pd
# 1. 학교전공별취업진학통계
df_employment2022 = pd.read_excel('./data/1학교전공별취업진학통계2022.xlsx', skiprows=13)
df_employment2023 = pd.read_excel('./data/1학교전공별취업진학통계2022.xlsx', skiprows=13)
df_employment2024 = pd.read_excel('./data/1학교전공별취업진학통계2022.xlsx', skiprows=13)
print("-2022년 한교전공별취업진학통계-")
print( df_employment2022.head() )
print()
print("-2023년 한교전공별취업진학통계-")
print( df_employment2022.head() )
print()
print("-2024년 한교전공별취업진학통계-")
print( df_employment2022.head() )
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
        
print("-전공 리스트-")
print( major_list )



# 2. 산업분류별채용통계
df_hire_by_industry2022 = pd.read_csv('./data/2산업분류별채용통계2022.csv', encoding='cp949')
df_hire_by_industry2023 = pd.read_csv('./data/2산업분류별채용통계2023.csv', encoding='cp949')
df_hire_by_industry2024 = pd.read_csv('./data/2산업분류별채용통계2024.csv', encoding='cp949')
print("-2022년 산업분류별채용통계-")
print( df_hire_by_industry2022.head() )
print()
print("-2023년 산업분류별채용통계-")
print( df_hire_by_industry2023.head() )
print()
print("-2024년 산업분류별채용통계-")
print( df_hire_by_industry2024.head() )
print()
df_hire_by_industry2022.info()
df_hire_by_industry2023.info()
df_hire_by_industry2024.info()

# 3. 직종분류별채용통계( encoding = cp949 )
df_hire_by_job2022 = pd.read_csv('./data/3직종분류별채용통계2022.csv', encoding='cp949')
df_hire_by_job2023 = pd.read_csv('./data/3직종분류별채용통계2023.csv', encoding='cp949')
df_hire_by_job2024 = pd.read_csv('./data/3직종분류별채용통계2024.csv', encoding='cp949')
# print("-2022년 직종분류별채용통계-")
# print( df_hire_by_job2022.head() )
# print()
# print("-2023년 직종분류별채용통계-")
# print( df_hire_by_job2023.head() )
# print()
# print("-2024년 직종분류별채용통계-")
# print( df_hire_by_job2024.head() )
# print()
df_hire_by_job2022.info()
df_hire_by_job2023.info()
df_hire_by_job2024.info()

# 결측치 마지막 Unnamed 삭제
df_list = [df_hire_by_industry2022, df_hire_by_industry2023, df_hire_by_industry2024,
           df_hire_by_job2022, df_hire_by_job2023, df_hire_by_job2024 ]
for df in df_list:
    df.drop(columns=['Unnamed: 11'], inplace=True, errors='ignore')
    print( df.isnull().sum() ) # 결측치 확인
    print() # 보기 쉽게 한 줄 띄움

job_list = [] # 직종 리스트

for job in df_hire_by_job2022['직종별']:
    if job not in job_list:
        job_list.append(job)
        
for job in df_hire_by_job2023['직종별']:
    if job not in job_list:
        job_list.append(job)
        
for job in df_hire_by_job2024['직종별']:
    if job not in job_list:
        job_list.append(job)

print('--직업 종류--')
print( job_list )

# 리스트끼리 비교한 결과: 다 대 다 관계로 전공과 직무가 매핑된다.
# 매핑 딕셔너리(major_job_mapping)를 따로 파일에 저장시킨 뒤 꺼내오는 방식으로 진행!