import matplotlib as mpl

# # 차트 내 한글 꺠짐 방지 코드( + 한글 폰트 )
mpl.rc('font', family='AppleGothic')        # 한글 폰트 설정
mpl.rcParams['axes.unicode_minus'] = False  # 음수 기호 깨짐 방지