import math

# 해버사인 거리를 계산하는 함수
def haversine_distance(coord1, coord2):
    R = 6371  # 지구의 반지름 (단위: km)
    
    # 좌표를 라디안으로 변환
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

    # 위도 및 경도 간의 차이 계산
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine 공식 적용
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # 해버사인 거리 계산
    distance = R * c
    return distance

# 최근접 이웃 알고리즘을 사용하여 여행 경로를 찾는 함수
def nearest_neighbor_tsp(coords):
    num_coords = len(coords)
    unvisited = set(range(num_coords))
    current_city = 0  # 시작 도시

    tour = [current_city]
    unvisited.remove(current_city)

    # 모든 도시를 방문할 때까지 반복
    while unvisited:
        # 현재 도시에서 가장 가까운 도시 선택
        nearest_city = min(unvisited, key=lambda city: haversine_distance(coords[current_city], coords[city]))
        
        # 선택한 도시를 여행 경로에 추가하고, 방문한 도시 목록에서 제거
        tour.append(nearest_city)
        unvisited.remove(nearest_city)
        
        # 선택한 도시를 현재 도시로 업데이트
        current_city = nearest_city

    return tour

# 예제
# coords는 각 관광지의 (위도, 경도) 좌표를 담은 리스트입니다.
coords = [
    (37.5665, 126.9780),  # 서울
    (35.6895, 139.6917),  # 도쿄
    (40.7128, -74.0060),  # 뉴욕
    (51.5074, -0.1278)    # 런던
]

# 최적의 여행 경로 찾기
optimal_tour = nearest_neighbor_tsp(coords)

# 결과 출력
print("Optimal Tour:", optimal_tour)
