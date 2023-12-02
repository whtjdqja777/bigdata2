with open('data/merged_data.csv', 'r', encoding='utf-8') as file:
    content = file.read()

with open('data/merged_data2.csv', 'w', encoding='EUC-KR') as file:
    file.write(content)