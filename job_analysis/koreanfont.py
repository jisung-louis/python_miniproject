# [*] 차트내 한글 깨짐 방지 코드( +한글폰트 ) , 항상 차트 사용하는 파일 상단에 복붙
import matplotlib as mpl
mpl.rc( 'font' , family='Malgun Gothic' )       # 한글 폰트 설정( 윈도우 기준 설치된 폰트 )
mpl.rcParams['axes.unicode_minus'] = False      # 음수 기호 깨짐 방지