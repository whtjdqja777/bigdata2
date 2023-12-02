import pandas as pd
from fuzzywuzzy import process
from geopy.distance import geodesic
import recommand

transformxy = pd.read_csv('service_data.csv')




def search_similar_word(transformxy, inputstring):# 거리를 기준으로 주변 상권 검색
    
    similar_word = recommand.string_comparison(transformxy,inputstring)
    findxy = recommand.extract_coordinates(transformxy,similar_word)
    make_sole =  list({item[0]: item for item in findxy}.values())
    find_near_position = recommand.caldistance(make_sole[0][1],make_sole[0][2], transformxy)
    matching_rows = transformxy[transformxy['상권_코드_명_x'].isin(find_near_position)]
    print(find_near_position)
    # matching_rows.to_csv('sample', index = False)
    
    return matching_rows
    



def final_recommand(a):
    select = ['서비스_업종_코드_명', '분기당_매출_금액', '점포수']

    service_codes = a[select]
    service_codes = service_codes[~service_codes.apply(lambda row: row.astype(str).str.contains('\*', na=False)).any(axis=1)]
    service_codes.to_csv('cut.csv', index=False)


    service_code_counts = service_codes.groupby('서비스_업종_코드_명').size().reset_index(name='카운트')
    service_codes['점포수'] = service_codes['점포수'].astype(int)
    # service_code_counts2 = service_codes.groupby('점포수').size().reset_index(name='점포수_카운트')

    # print(service_codes)
    total_sales_by_service = service_codes.groupby('서비스_업종_코드_명')['분기당_매출_금액'].sum().reset_index()
    total_sales_by_service2 = service_codes.groupby('서비스_업종_코드_명')['점포수'].sum().reset_index()

    # print(total_sales_by_service2)

    merged_df = pd.merge(total_sales_by_service, service_code_counts, on='서비스_업종_코드_명', how='left')
    merged_df = pd.merge(merged_df,total_sales_by_service2, on ='서비스_업종_코드_명', how ='left' )
    # print(merged_df)
    cal_average = merged_df['분기당_매출_금액']/merged_df['점포수']
    merged_df['평균_매출'] = cal_average  
    merged_df['평균_매출_10진수'] = merged_df['평균_매출'].apply(lambda x: '{:.10f}'.format(x))
    merged_df = merged_df.sort_values(by = ['평균_매출'], ascending=False)
    recommand_top_5 = merged_df.head(5)

    print(recommand_top_5)



    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm

    font_path = "D:\\ttf\\13151B114AE7E3A025\\malgun.ttf"  
    fontprop = fm.FontProperties(fname=font_path).get_name()
    plt.rcParams['font.family'] = fontprop



    
    # 시각화
    plt.figure(figsize=(10, 6))
    plt.bar(recommand_top_5['서비스_업종_코드_명'], recommand_top_5['평균_매출'], color='skyblue')
    plt.xlabel('서비스 업종 코드명')
    plt.ylabel('평균 매출')
    plt.title('서비스 업종별 평균 매출')
    plt.xticks(rotation=45)  # x축 레이블 회전
    plt.tight_layout()
    plt.show()



import tkinter as tk

def save_entry_text():
    text = entry.get()  # Entry에 입력된 텍스트 가져오기
    print(f"입력된 텍스트: {text}")
    final_recommand(search_similar_word(transformxy, text))
    return text  # 텍스트 출력 또는 원하는 변수에 저장하는 등의 작업 수행

def run_save():
    save_entry_text()

window = tk.Tk()
window.geometry("400x300") 
entry = tk.Entry(window)
entry.pack()

button = tk.Button(window, text="입력", command=run_save)
button.pack()

window.mainloop()
