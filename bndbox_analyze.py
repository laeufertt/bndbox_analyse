import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import os

# import all files from Annotations
path = "/Users/weijt606/dataset/Annotations"
files = os.listdir(path)
df_list = []
for file in files:
    xml_data = open(path+'/'+file).read()

    def xml2df(xml_data):
        tree = ET.XML(xml_data) # element tree, you can also use ET.fromstring
        all_records = [] # convert all record list into a dataframe
        for i, child in enumerate(tree): # from root tree to extract child tree
            record = {} # place hold for record
            for subchild in child: # iterate through the subchildren
                for subsubchild in subchild:  # iterate through the child of subchilden
                    record[subsubchild.tag] = subsubchild.text # extract the element from "bnbbox and create a new dictionary key
                    all_records.append(record) # append this record to all_records.
        return pd.DataFrame(all_records) #return records as DataFrame

    ss = {}
    df = xml2df(xml_data)
    df = df.drop_duplicates()  #delete repeated data
    df = df.sort_index()  # sort data as ascending
    df = df.reset_index()  # sort out new oder of columns
    del df['index']
    # df = df.convert_objects(convert_numeric=True).dtypes  # data type: object to int
    df = df.applymap(int)  #global transform data from object to int

    df["size_x"] = df["xmax"] - df["xmin"]
    df["size_y"] = df["ymax"] - df["ymin"]
    df = df[['xmax','xmin','size_x','ymax','ymin','size_y']] #order the index as: xmax xmin size_x ymax ymin size_y
    # print df.dtypes  # check data type
    df_list.append(df) # append every dataframe to df_list
    df = pd.concat(df_list, ignore_index=True)  #concatenation all DataFrames to one DataFrame


print(df)

plt.subplot(121)
# plt.hist(df["size_x"], normed=1, bins= range(0,120,5))  # probability
plt.hist(df["size_x"], bins= range(0,120,5))
# plt.plot(df["size_x"])
plt.xlabel('size')
plt.ylabel('scalar')
# plt.ylabel('probability')
plt.title('Length of BoundingBox')

plt.subplot(122)
# plt.hist(df["size_y"], normed=1, bins= range(0,120,5), facecolor='red') # probability
plt.hist(df["size_y"], bins= range(0,120,5), facecolor='red')
# plt.plot(df["size_y"])
plt.xlabel('size')
plt.ylabel('scalar')
# plt.ylabel('probability')
plt.title('Height of BoundingBox')

plt.show()
