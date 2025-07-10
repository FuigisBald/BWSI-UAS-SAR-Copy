import json
radardatalist = [[1,[3,4,5]],[2,[2,2,4]]]
temp = str(radardatalist[0][0])

with open("datalist"+temp+".json","w") as f:
    json.dump(radardatalist,f)

