import json
student = {"first_name": "Jake","last_name": "Doyle"}
json_data = json.dumps(student, indent=2)
print(json_data)
#print(json.loads(json_data))