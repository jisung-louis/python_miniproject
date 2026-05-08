import pandas as pd 

df = pd.read_csv('./data/2산업분류별채용통계2022.csv', encoding='cp949')
print( df.head() )          # 상위 5개 출력하여 데이터 확인 
df.info()                   # 속성 타입 확인 
print( df.isnull().sum() )  # 결측치 확인 