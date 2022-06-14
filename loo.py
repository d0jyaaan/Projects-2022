import xlsxwriter
from datetime import datetime

lst = list()

workbook = xlsxwriter.Workbook('random.xlsx')
worksheet = workbook.add_worksheet()

n = 0
while True:

    temp = input("")

    if temp == "kill":
        break
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    lst.append((temp, current_time))
    n+=1 
    if n == 3:
        break
    

print(lst)

row = 0
col = 0

for item in (lst):
    worksheet.write(row, col,     item[0])
    worksheet.write(row, col + 1, item[1])
    row += 1

workbook.close()
