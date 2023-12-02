import pandas as pd
from fuzzywuzzy import process
from geopy.distance import geodesic

# transformxy = pd.read_csv('transformxy.csv')
def merge_data():               #데이터 합치기
# 두 개의 CSV 파일 읽기
    data1 = pd.read_csv('data/seoul_commercial_district_name2.csv')
    data2 = pd.read_csv('data/seoul_commercial_district_background2.csv')
    

    # 조인할 기준이 되는 열을 기준으로 조인
    merged_data = pd.merge(data1, data2, on='상권_코드', how='inner')
    print(merged_data)
    merged_data.to_csv('merged_data.csv', index=False)


def data_select():                      #필요한 컬럼만 뽑아오는 메서드
   # CSV 파일 읽기
    data = pd.read_csv('merged_data.csv')

    # 원하는 열만 선택하여 새로운 데이터프레임 만들기
    selected_columns = ['상권_코드_명_x', '엑스좌표_값', '와이좌표_값', '서비스_업종_코드_명', '분기당_매출_금액', '점포수']  # 선택하려는 열 이름 목록
    selected_data = data[selected_columns]
    

    # 새로운 CSV 파일로 내보내기
    selected_data.to_csv('sevice_data.csv', index=False)
    return selected_data




def recommand_type_of_bussiness(char):      #

    sorted_data = select.sort_values(by='분기당_매출_금액', ascending=False)
    top_5_percent = sorted_data.head(int(len(sorted_data) * 0.05))

    # 정렬된 데이터 출력 또는 다른 작업 수행
    print(top_5_percent.head())



def string_comparison(data,input_string):               #검색한 지역명과 기존 select에 있는 지역명 유사도 계산해서 select에서 유사도 80 이상인 지역명 뽑는 메서드 입니다.
    select_data = data['상권_코드_명_x'].unique()
    # 비교할 문자열과 유사한 문자열 찾기
    similar_strings = process.extract(input_string, select_data, limit=1)
    # 유사도가 80 이상인 문자열만 필터링
    similar_strings_80_plus = [string for string, score in similar_strings if score >= 80]
    return similar_strings_80_plus



# 유사도가 80 이상인 최대 5개의 문자열 찾기
     #실질적으로 뽑는 부분 파라미터는 전처리된 select 데이터, 검색어 input_string


    



def extract_coordinates(data, target_strings):              #위에서 찾은 문자열의 xy좌표를 뽑는 머서드
    xy = []

    for target_string in target_strings:
        matches = data[data['상권_코드_명_x'] == target_string]
        for idx, row in matches.iterrows():
            x_coord = row['엑스좌표_값']
            y_coord = row['와이좌표_값']
            xy.append((target_string, x_coord, y_coord))

    return xy

# similar_strings_80_plus는 유사한 문자열이 저장된 리스트입니다.
# xy = extract_coordinates(select, similar_strings_80_plus)
# unique_xy = list(set(xy))
# # print(unique_xy)
# print(unique_xy[0][1])


#########################################유사도 계산으로 좌표 묶어서 주변상권을 같이 묶어서 추천 알고리즘에 해당 상권 코드명을 넣어서 같이 업종 추천 계산하는 코드에 넣는 코드 짜야됩니다.#############
def find(select, unique_xy):
    x_coord = str(unique_xy[0][1])
    y_coord = str(unique_xy[0][2])
    combined_values = select['엑스좌표_값'].astype(str) + select['와이좌표_값'].astype(str)
    similar_xy = process.extract(x_coord + y_coord, combined_values.unique(), limit=5)

    # similar_y = process.extract(y_coord, select['와이좌표_값'].unique().astype(str), limit=5)
    # print(similar_x)

    # 유사도가 80 이상인 문자열만 가져오기
    similar_x_80_plus = [string for string, score in similar_xy if score >= 70]
    # similar_y_80_plus = [string for string, score in similar_y if score >= 80]

    print(f"엑스 와이 좌표값 {x_coord + y_coord}의 유사도가 80 이상인 것들: {similar_x_80_plus}")
    # print(f"와이 좌표값 {y_coord}의 유사도가 80 이상인 것들: {similar_y_80_plus}")







                                #거리 계산후 가장 가까운거리 찾는코드
def caldistance(given_x, given_y, transformxy):
    trans_result = []
    # 주어진 좌표와 데이터프레임의 각 위치와의 거리 계산 후 저장
    distances = []
    for index, row in transformxy.iterrows():
        coord = (row['와이좌표_값'],row['엑스좌표_값'])  # 각 행의 좌표값
        dist = geodesic((given_y,given_x), coord).meters  # 두 좌표 간의 거리 계산 (미터 단위)
        distances.append((index, dist))
    # 거리에 따라 정렬
    distances =  list({item[1]: item for item in distances}.values())
    distances.sort(key=lambda x: x[1])
    

    
    # 가장 가까운 5개 위치 출력
    closest_points = distances[:5]
    for idx, dist in closest_points:
        trans_result.append(transformxy.loc[idx]['상권_코드_명_x'])
    return trans_result

data_select()




    
    