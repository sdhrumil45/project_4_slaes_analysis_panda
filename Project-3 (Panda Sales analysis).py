#imprt useful library
import pandas as pd
import os
import matplotlib.pyplot as plt

#1)  merge 12 month data in single file
#list all file in particular folder
'''
# Now we Get all file in single array
files = [ file for file in os.listdir("E:/python/video/data analysis/Project-3 (Sales analysis Pandas)/SalesAnalysis/Sales_Data")]

# Create empty data frame
all_month_data = pd.DataFrame()


#concate all month file 

for file in files:
    df = pd.read_csv("E:/python/video/data analysis/Project-3 (Sales analysis Pandas)/SalesAnalysis/Sales_Data/" + file)

    all_month_data = pd.concat([all_month_data,df])

all_month_data.to_csv("all_data.csv",index=False) '''



#2)  from above code we get all month excel in single sheet so we use this sheet for other work

df = pd.read_csv("E:/python/video/data analysis/Project-3 (Sales analysis Pandas)/all_data.csv")
print(df)


#in all data there is some empty row so we remove this row and create new csv file which have no empty row 

# nan_df = df[df.isna().any(axis=1)]

df = df.dropna(how='all')
print(df)


# df_cleaned = df.dropna(how='all')
# df_cleaned.to_csv('cleaned_file.csv', index=False)
# df = pd.read_csv("cleaned_file.csv")


#we merge 12 month file in one so also in merge file we get heading repetately so we delete duplicate row


df = df[df["Order Date"].str[0:2] != "Or"]


#add month colum
df["month"] = df["Order Date"].str[0:2]


## #convert month data type str to int
df["month"] = df["month"].astype('int32')


#question no1: what was the best month for sales? how much we earned on that month?

#we first multiply quntity & price so we get total sale for order

df["Quantity Ordered"] = pd.to_numeric(df["Quantity Ordered"])
df["Price Each"] =  pd.to_numeric(df["Price Each"]) 

df["sales"] = df["Quantity Ordered"] * df["Price Each"]

#groupby month and sum sales monthaly


monthly_sale = df.groupby(["month"]).sum(["sales"])

x = range(1,13)
y = monthly_sale["sales"]
plt.bar(x,y)
plt.xticks(x)
plt.xlabel("Month")
plt.ylabel("sales value in Million $")
plt.show()


#question no2: which city get highest sales

#we define function to get city & state from address

def state(address):
    a =  address.split(",")[2]
    return a.split(" ")[1]

    
def city(address):
    return address.split(",")[1]


df["city"] = df["Purchase Address"].apply(lambda x : f"{city(x)}[{state(x)}]")

# #groupby city and sum sales cityvise
sale_city = df.groupby(["city"]).sum("sales")


x = df["city"].unique()
y = sale_city["sales"]
plt.bar(x,y)
plt.xticks(x,rotation = "vertical" , size = 8)
plt.xlabel("city")
plt.ylabel("sales value in Million $")
plt.show()


#question no3: which time is best to put advertisment

#first we convert date into datetime object

df["Order Date"] = pd.to_datetime(df["Order Date"])
df["hour"] = df["Order Date"].dt.hour

hours = [hour for hour, d in df.groupby(["hour"])]
hours = [t[0] for t in hours]
count = df.groupby(["hour"]).count()
plt.plot(hours,count)
plt.xticks(hours)
plt.grid()
plt.show()


#question no4: which product are most sold togeteher

combine_order = df[df["Order ID"].duplicated(keep=False)]
combine_order = combine_order.copy()


combine_order["product_group"] = combine_order.groupby(["Order ID"])["Product"].transform(lambda x: ",".join(x))


# combine_order["product_group"] = combine_order.groupby(["Order ID"])["Product"].transform(lambda x: ",".join(x))

combine_order = combine_order.drop_duplicates(["Order ID","product_group"])


# Step 1: Sort the product combinations in each row
combine_order["product_group"] = combine_order["product_group"].apply(lambda x: ','.join(sorted(x.split(','))))

# Step 2: Count the occurrences of each combination
combination_counts = combine_order["product_group"].value_counts()

top_combinations = combination_counts.head(5)  # Top 5 combinations

top_combinations.plot(kind='bar')
plt.xlabel('Product Combinations')
plt.ylabel('Number of Orders')
plt.title('Top Selling Product Combinations')
plt.show()


#question no5: which product sold the most? why do you think sold most?

most_sold = df.drop("Order Date",axis="columns")

most_sold = most_sold.groupby("Product")
quntity = most_sold.sum()["Quantity Ordered"]


products = [product for product,df in most_sold ]
avg_price =  most_sold.sum()["Price Each"]/most_sold.sum()["Quantity Ordered"]


fig,ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.bar(products,quntity)
ax2.plot(products,avg_price,"red")

ax1.set_xlabel("product name")
ax1.set_ylabel("selling qty")
ax2.set_ylabel("avg selling price",color="red")

ax1.set_xticks(range(len(products)))
ax1.set_xticklabels(products,rotation = "vertical" , size = 8)

plt.show()
