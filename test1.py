from mock_data import mock_data


# dictionary
me = {
    "name": "Jake",
    "last": "Schultz",
    "age": 31,
    "hobbies":[],
    "address": {
        "street": "Alturas",
        "city": "Pflugerville"
    }
}

# print full name
print(me["name"]+" "+me["last"])

# print city
print(me["address"]["city"])

# modify existing 
me["age"] = 32

# create new
me["new"] = 1
print(me)

# list
names = []

names.append("Guillermo")
names.append("Jake")
names.append("Krystle")

print(names)

# get elements
print(names[0])

# for loop
for name in names:
    print(name)




ages = [12,32,456,10,23,678,4356,2,46,789,23,67,13]

# find the lowest number
ages.sort()
print(ages[:1])

# OR
youngest = ages[-1]
for age in ages:
    if age < youngest:
        youngest = age
    
print(youngest)


# print the title for every product
for item in mock_data:
    print(item["title"])