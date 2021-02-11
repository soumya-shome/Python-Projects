import pandas

# Python code t get difference of two lists 
# Not using set() 
def Diff(li1, li2): 
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2] 
    return li_dif 


df = pandas.read_excel('Book1.xlsx', sheet_name='Sheet1')

# print whole sheet data
print(Diff(df['Following'],df['Followers']))