import sys
import ast

f = open("List.txt","r+")
old_f = f.read()
f.close()
old_f = ast.literal_eval(old_f)

print(len(old_f))