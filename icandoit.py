import cv2
import pytesseract
import glob
import pandas as pd
import openai
import base64
import os



def append_to_excel(new_data_df, excel_path):
    if os.path.exists(excel_path):
        # 기존 엑셀 파일 불러오기
        existing_df = pd.read_excel(excel_path)
        # 기존 데이터와 새로운 데이터 병합
        combined_df = pd.concat([existing_df, new_data_df], ignore_index=True)
    else:
        # 엑셀 파일이 없으면 새로운 데이터프레임 사용
        combined_df = new_data_df
    # 엑셀 파일로 저장
    combined_df.to_excel(excel_path, index=False)
    
# Tesseract 경로 설정
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

folder_path = r"C:\Users\qkrgu\1"

# 지원할 이미지 확장자
image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.gif"]

image_files = []
for ext in image_extensions:
    image_files.extend(glob.glob(os.path.join(folder_path, ext)))

# 결과 출력

for image_path in image_files:
    image = cv2.imread(image_path)

    client = openai.OpenAI(api_key="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")

    _, buffer = cv2.imencode('.png', image)
    base64_Image = base64.b64encode(buffer).decode("utf-8")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You're the best OCR in the world."},
            {"role": "user", "content": [
                {"type": "text", "text": "Extract the table data from the provided text and return it as a DataFrame array."
                "columns = [ “Serial Number”, “Specimen Number”, “Quality”, “Thickness”, “SiO2”, “Al2O3”, “Fe2O3_T”, “MgO”, “CaO”, “Na2O”, “K2O”, “TiO2”, “MnO”, “P2O5”, “Total”, “RO2”, “RO2O3”, “RO” ]"},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{base64_Image}"}
                }
            ]}
        ],
        temperature=1.0,
    )

    data = response.choices[0].message.content

    # Create the DataFrame and rename columns

    start_index = data.find("data = {")
    end_index = data.find("\ndf = pd.DataFrame")

    # data 문자열 추출
    data_code = data[start_index:end_index].strip()

    # data 평가 (실제 Python 객체로 변환)
    data = eval(data_code.split("=", 1)[1].strip())

    # DataFrame 생성
    df = pd.DataFrame(data)

    # 결과 출력
    file_path = r'C:\Users\qkrgu\u.xlsx'

    # 데이터셋을 엑셀 파일로 저장
    append_to_excel(df, file_path)

# 폴더 경로 설정


# 폴더 내 모든 파일 처리


# 이미지 로드 및 그레이스케일 변환


# Select only the required columns
