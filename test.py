import cv2
import pytesseract
import re
import pandas as pd
import openai
import base64
import json

def process_value(value):
    try:
        # Check if the value contains a dot (decimal point)
        if '.' in value:
            return value
        else:
            # Insert a decimal point two places from the end
            return f"{value[:-2]}.{value[-2:]}"
    except:
        # Return non-numeric values as-is
        return value
    
# Tesseract 경로 설정
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 폴더 경로 설정
image_path = r"C:\\Users\\qkrgu\\1 (1).png" 


# 폴더 내 모든 파일 처리


# 이미지 로드 및 그레이스케일 변환
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 전처리: 대비 조정 및 이진화
gray = cv2.convertScaleAbs(gray, alpha=3.0, beta=0)  # 대비 극대화
gray = cv2.medianBlur(gray, 5)  # 블러링으로 노이즈 제거
_, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)  # 이진화

# 테이블 외곽선 감지
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

table_contours = sorted(contours, key=cv2.contourArea, reverse=True)[0]
x, y, w, h = cv2.boundingRect(table_contours)

table_image = image[y:y+h, 0:200]
gray_table = cv2.cvtColor(table_image, cv2.COLOR_BGR2GRAY)  
upscaled_image = cv2.resize(gray_table, None, fx=1, fy=1, interpolation=cv2.INTER_CUBIC)
ocr_result = pytesseract.image_to_string(upscaled_image)
client = openai.OpenAI(api_key="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")

_, buffer = cv2.imencode('.png', upscaled_image)
base64_Image = base64.b64encode(buffer).decode("utf-8")
_, buffer = cv2.imencode('.png', image)
base64_Image = base64.b64encode(buffer).decode("utf-8")
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You're the best OCR in the world."},
        {"role": "user", "content": [
            {"type": "text", "text": "Extract the table data from the provided text and return it as a JSON array."},
            {"type": "image_url", "image_url": {
                "url": f"data:image/png;base64,{base64_Image}"}
            }
        ]}
    ],
    temperature=1.0,
)


# ChatCompletion 객체에서 데이터 추출


print(response.choices[0].message.content)
# 테이블 영역 크롭
table_image = image[y:y+h, 200:500]
gray_table = cv2.cvtColor(table_image, cv2.COLOR_BGR2GRAY)  
upscaled_image = cv2.resize(gray_table, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)


# OCR 수행
ocr_result = pytesseract.image_to_string(upscaled_image)

# 행별로 분리
lines = ocr_result.split("\n")
Names = [
    line for line in lines
    if line.strip() 
    and line.strip()[0].isalpha() 
    and not re.search(r'[^\w\s-]', line) 
    and '-' in line
]

data = pytesseract.image_to_data(gray_table, output_type=pytesseract.Output.DICT)

rows = [
    {key: data[key][i] for key in data.keys()}  # 각 행의 데이터를 딕셔너리로 저장
    for i in range(len(data['text']))          # 데이터의 각 행을 순회
    if data['text'][i].strip()                 # 텍스트가 비어 있지 않은 경우
    and data['text'][i].strip()[0].isalpha()   # 첫 글자가 알파벳인 경우
    and not re.search(r'[^\w\s-]', data['text'][i])  # 특수문자("-" 제외)가 없는 경우
]
values = []
for row in rows:
    if row['text'].strip():  # 빈 텍스트 제외
        row_x, row_y, row_w, row_h = row['left'], row['top'], row['width'], row['height']
        table_image = image[row_y-10:row_y+row_h+50, 1000:x+w]
        if row_y-10 < y : 
            table_image = image[y:row_y+row_h+50, 1000:x+w]
        elif row_y+row_h+50 > y+h:
            table_image = image[row_y-10:y+h, 1000:x+w]

        #upscaled_image = cv2.resize(table_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        cv2.imwrite("upscaled_image.png", table_image)
        gray_table = cv2.cvtColor(table_image, cv2.COLOR_BGR2GRAY)   
        ocr_result = pytesseract.image_to_string(gray_table)
        #print(ocr_result)
        lines = ocr_result.split("\n")
        value = [line for line in lines if line.strip()]
        values.append(value[0])

processed_data = []  
    

 
for i,row in enumerate(values):
    # Split the row into individual values and process each
    processed_row = [process_value(value) for value in row.split()]
    processed_data.append(processed_row)
while(True) :
    if len(Names) < len(processed_data):
        Names.append("Null")
    else:
        break



# Create a DataFrame
df = pd.DataFrame(processed_data)
df = df.replace(to_replace=r'[Oo]', value='0', regex=True)
df = df.replace(to_replace=r'[^0-9\.]', value='', regex=True)
df.insert(0, "Specimen Number", Names)

columns = [
    "Serial Number", "SiO2", 
    "Al2O3", "Fe2O3_T", "MgO", "CaO", "Na2O", "K2O", "TiO2", 
    "MnO", "P2O5", "Total", "RO2", "RO2O3", "RO"
]

# 데이터프레임 열 수와 컬럼 이름 리스트 길이가 맞지 않을 경우 조정
columns_extended = columns[:len(df.columns)] if len(columns) >= len(df.columns) else columns

# 데이터프레임에 컬럼 이름 적용
df.columns = columns_extended

# Extend the rows list with None values if it's shorter than the number of dataframe rows

print(df)

