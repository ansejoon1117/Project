import pandas as pd
import googlemaps
from IPython.display import HTML

# CSV 파일 읽기
file_path = 'example.csv'
file = pd.read_csv(file_path)

# 이름과 주소 컬럼 이름에 따라 수정
name_column_name = '이름'
address_column_name = '주소'

# Google Maps API 키 설정
api_key = 'AIzaSyDYdGKN8N1u_U_jbfN56Qq4LN1bjcmDmFg'
gmaps = googlemaps.Client(key=api_key)

# 사용자로부터 출발지와 도착지 이름 입력 받기
start_name = input("출발지 이름을 입력하세요: ")
end_name = input("도착지 이름을 입력하세요: ")

# 입력받은 이름에 해당하는 출발지와 도착지 주소 가져오기
start_address = file[file[name_column_name] == start_name][address_column_name].values[0]
end_address = file[file[name_column_name] == end_name][address_column_name].values[0]

# 출발지와 도착지 주소 확인
print(f"{start_name}의 출발지 주소: {start_address}")
print(f"{end_name}의 도착지 주소: {end_address}")

# 사용자로부터 모드 입력 받기
mode = input("이동 모드를 선택하세요 (driving 또는 transit): ").lower()

# 입력된 모드에 따라 경로 및 예상 소요 시간, 거리 정보 가져오기
directions_result = gmaps.directions(start_address, end_address, mode=mode)

# 예상 소요 시간 및 거리 출력
duration = directions_result[0]['legs'][0]['duration']['text']
distance = directions_result[0]['legs'][0]['distance']['text']

print(f"예상 소요 시간: {duration}")
print(f"총 거리: {distance}")

# 대중교통 모드일 때만 세부 경로 출력
if mode == "transit":
    # 대중교통 모드로 경로 및 예상 소요 시간, 거리 정보 가져오기
    directions_result_transit = gmaps.directions(start_address, end_address, mode="transit")

    # 예상 소요 시간 및 거리 출력
    duration_transit = directions_result_transit[0]['legs'][0]['duration']['text']
    distance_transit = directions_result_transit[0]['legs'][0]['distance']['text']

    # 대중교통 모드에서의 세부 경로 출력
    steps_transit = directions_result_transit[0]['legs'][0]['steps']
    print("\n세부 경로 (대중교통):")
    for step in steps_transit:
        # 세부 정보에서 필요한 내용을 파싱하여 출력
        instructions = step.get('html_instructions', '')

        # Check if the step starts with "Walk to"
        if not instructions.startswith("Walk to"):
            transit_details = step.get('transit_details', {})
            line_name = transit_details.get('line', {}).get('short_name', '')
            transit_stop = transit_details.get('arrival_stop', {}).get('name', '')
            print(f"{instructions} ({line_name} 탑승, {transit_stop} 하차)")
        else:
            print(instructions)
            
# Google Maps에서 경로 표시 (입력된 모드, HTML 출력)
route_html = f"<iframe width='600' height='450' frameborder='0' style='border:0'" \
             f"src='https://www.google.com/maps/embed/v1/directions?key={api_key}" \
             f"&origin={start_address}&destination={end_address}&mode={mode}'></iframe>"

display(HTML(route_html))
