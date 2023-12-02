from pyproj import Proj, transform
import pandas as pd
from fuzzywuzzy import process
from pyproj import Transformer
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
    selected_columns = ['상권_코드_명_x', '엑스좌표_값', '와이좌표_값', '서비스_업종_코드_명', '분기당_매출_금액','점포수']  # 선택하려는 열 이름 목록
    selected_data = data[selected_columns]
    

    # 새로운 CSV 파일로 내보내기
    # selected_data.to_csv('sevice_data.csv', index=False)
    return selected_data


select = data_select()      #select가 seleted_data입니다.


proj_2097 = Proj(init='epsg:2097')
proj_wgs84 = Proj(init='epsg:4326')  # WGS84는 경위도 좌표체계입니다.


def transform_xy(row):
    # EPSG:2097 좌표 체계와 경위도 좌표 체계(WGS84) 정의
    # 변환할 좌표 값 입력 (EPSG:2097 좌표)

    x_2097, y_2097 = row['엑스좌표_값'], row['와이좌표_값']
    # 좌표 변환 (EPSG:2097 -> WGS84)
    lon, lat = transform(proj_2097, proj_wgs84, x_2097, y_2097)
    row['엑스좌표_값'], row['와이좌표_값'] = lon, lat
    return row

transformxy = select.copy()
transformxy = transformxy.apply(transform_xy, axis = 1)

print(transformxy)
transformxy.to_csv('service_data.csv', index=False)