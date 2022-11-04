import os
import requests
import xmltodict
import pandas as pd

import time
from tqdm import tqdm

k_e_mapper = {"관광특구":"travel",
              "고궁_문화유산":"heritage",
              "인구밀집지역":"pop_main",
              "발달상권":"com_main",
              "공원":"park"}

location_dict=\
{'관광특구':["강남 MICE 관광특구", "동대문 관광특구", "명동 관광특구", "이태원 관광특구", "잠실 관광특구", "종로·청계 관광특구", "홍대 관광특구"], 
 "고궁_문화유산":["경복궁·서촌마을", "광화문·덕수궁", "창덕궁·종묘"], 
 '인구밀집지역':["가산디지털단지역", "강남역", "건대입구역", "고속터미널역", "교대역", "구로디지털단지역", "서울역", "선릉역", "신도림역", "신림역", 
            "신촌·이대역", "역삼역", "연신내역", "용산역", "왕십리역"], 
 '발달상권':["DMC(디지털미디어시티)", "창동 신경제 중심지", "노량진", "낙산공원·이화마을", "북촌한옥마을", "가로수길", "성수카페거리", "수유리 먹자골목", 
         "쌍문동 맛집거리", "압구정로데오거리", "여의도", "영등포 타임스퀘어", "인사동·익선동"], 
 "공원":["국립중앙박물관·용산가족공원", "남산공원", "뚝섬한강공원", "망원한강공원", "반포한강공원", "북서울꿈의숲", "서울대공원", "서울숲공원", "월드컵공원", 
       "이촌한강공원", "잠실종합운동장", "잠실한강공원"]}

for location_type in tqdm(location_dict.keys()):
    print(f"\n{location_type}  : start")
    locations = location_dict[location_type]
    total_dict = {}
    my_api_key = "627562616f666c793131386b78674874"
    for location in tqdm(locations):
        url=f"http://openapi.seoul.go.kr:8088/{my_api_key}/xml/citydata/1/10/{location}"
        response = requests.get(url)
        time.sleep(3)
        data_json=xmltodict.parse(response.text)
        total_dict[location] = data_json['SeoulRtd.citydata']['CITYDATA']['LIVE_PPLTN_STTS']['LIVE_PPLTN_STTS']

    df=pd.DataFrame.from_dict(total_dict,orient='index')
    df=df.reset_index().rename(columns={"index":"LOCATION"})

    if not os.path.exists(f'raw_data/df_{k_e_mapper[location_type]}.csv'):
        df.to_csv(f'raw_data/df_{k_e_mapper[location_type]}.csv',index=False, mode='w',encoding='utf-8')
    else:
        df.to_csv(f'raw_data/df_{k_e_mapper[location_type]}.csv',index=False, mode='a',encoding='utf-8',header=False)


