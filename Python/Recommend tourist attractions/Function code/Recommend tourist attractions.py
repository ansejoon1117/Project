# cx_Oracle 및 pandas, surprise 라이브러리 임포트
import cx_Oracle
import pandas as pd
from surprise import Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import SVD
from surprise import accuracy

# 오라클에 연결
conn = cx_Oracle.connect('system/0000@localhost:1521/orcl')
cursor = conn.cursor()

# 사용자 정보 입력
user_gender = int(input("성별을 입력하세요 (1: 남성, 2: 여성): "))
user_age = int(input("나이를 입력하세요: "))
user_relationship = int(input("관계를 입력하세요 (1: 혼자, 2: 가족, 3: 연인, 4: 친구): "))
user_destination = input("여행할 지역을 입력하세요: ")

# 쿼리 작성 및 실행 (예제: 사용자 정보 및 관광지 평점을 가진 테이블을 가정)
query = f"SELECT ID, 관광지, 성별, 나이, 관계, 평점, 지역 FROM GRADE WHERE 지역 = '{user_destination}'"
df_oracle = pd.read_sql(query, conn)

# Surprise 라이브러리의 Dataset 형태로 변환
reader = Reader(rating_scale=(1, 5))
surprise_data = Dataset.load_from_df(df_oracle[['ID', '관광지', '평점']], reader)

# 학습용과 테스트용 데이터셋으로 분리
trainset, testset = train_test_split(surprise_data, test_size=0.2, random_state=42)

# SVD 모델 생성
model = SVD()

# 모델 학습
model.fit(trainset)

# 사용자에게 아직 평가되지 않은 아이템을 찾아서 예측
user_id = df_oracle['ID'].max() + 1  # 새로운 사용자 ID 부여
user_recommendations = []

for attraction_id in df_oracle['관광지'].unique():
    # 이미 평가한 아이템은 제외
    if not df_oracle[(df_oracle['ID'] == user_id) & (df_oracle['관광지'] == attraction_id)].empty:
        continue

    # 예측을 위한 사용자 정보 입력
    prediction = model.predict(user_id, attraction_id, r_ui=None, clip=False)

    user_recommendations.append({'관광지': attraction_id, '예상평점': prediction.est})

# 예측된 평점을 기준으로 내림차순 정렬하여 상위 3개 아이템을 추천
user_recommendations = sorted(user_recommendations, key=lambda x: x['예상평점'], reverse=True)[:3]

# 결과 출력
print(f'\nTop 3 추천 관광지:')
for recommendation in user_recommendations:
    print(f"관광지: {recommendation['관광지']}, 평점: {recommendation['예상평점']}")

# 연결 종료
cursor.close()
conn.close()
