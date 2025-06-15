import openpyxl

# 파일 경로를 입력하세요
input_file = 'La_liga_Data.xlsx'
output_file = 'no_hyperlinks_La_liga_Data.xlsx'

# 엑셀 파일 열기
wb = openpyxl.load_workbook(input_file)

for ws in wb.worksheets:
    for row in ws.iter_rows():
        for cell in row:
            if cell.hyperlink:
                cell.hyperlink = None  # 하이퍼링크만 삭제, 텍스트는 그대로

wb.save(output_file)
print(f"하이퍼링크가 모두 제거된 파일이 저장되었습니다: {output_file}")