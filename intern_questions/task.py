import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

data = pd.read_csv("customer_order_history.csv")

prod = pd.read_csv("product_order_data.csv")
prod = prod[['product_id','event_id']]

def unique(): 
	o_list = []
	c_list =[]
	for index, rows in data.iterrows(): 
	    my_list=rows.customerId 
	    c_list.append(my_list) 
	list_set = set(c_list)
	cus_list = (list(list_set))
	cus_list.sort()

	for index, rows in data.iterrows(): 
	    my_list=rows.orderId 
	    o_list.append(my_list) 
	list_set = set(o_list)
	o_list = (list(list_set))
	o_list.sort()
	return cus_list, o_list

def segment():
	for i in range(len(row_list)):
		if row_list[i][0]>=4 and row_list[i][1]>=5:
			seg[0] = seg[0]+1
		elif row_list[i][0]>=2 and row_list[i][1]>=2:
			seg[1]= seg[1]+1
		elif row_list[i][0]<=2 and row_list[i][1]<=2:
			seg[2]= seg[2]+1
		elif row_list[i][0]>=4 and row_list[i][1]<=2:
			seg[3]= seg[3]+1
		elif 3<=row_list[i][0]<=4 and row_list[i][1]<=1:
			seg[4]= seg[4]+1
		elif row_list[i][0]<=2 and row_list[i][1]<=2:
			seg[5]= seg[5]+1
		elif row_list[i][0]<=2 and row_list[i][1]>=4:
			seg[6]= seg[6]+1
		elif row_list[i][0]<=2 and row_list[i][1]>=2:
			seg[7]= seg[7]+1
		elif 2<=row_list[i][0]<=3 and row_list[i][1]<=2:
			seg[8]= seg[8]+1
		elif 2<=row_list[i][0]<=3 and 2<=row_list[i][1]<=4:
			seg[9]= seg[9]+1
		elif 3<=row_list[i][0]<=5 and 1<=row_list[i][1]<=3:
			seg[10] = seg[10]+1

#There are some 'order' in order history table for which there's no product associated in product order table.
#That is why I had used exception handling to avoid error.
best_p = []
def bestproduct(cus_list, o_list):
	for i in range(len(cus_list)): 
		c = cus_list[i]
		x = len(data1[cus_list[i]])
		d = dict()
		for j in range(x):
			order = data1[c][j]
			try:
				for k in range(len(prod[order])):
					p = prod[order][k]
					if p in d:
						d[p]+=1
					else:
						d[p]=1
			except KeyError:
				pass
		try:
			z = max(d, key=d.get)
			c_info = {'cus_id': cus_list[i], 'bestproduct_id':z}
			best_p.append(c_info)
		except ValueError:
			pass



cus_list, o_list = unique()
data1 = data[['customerId','orderId']]
data['orderDate'] = data['orderDate'].str.split(" ", n = 1, expand = True) 

data = data.drop_duplicates()

PRESENT = dt.date.today()
data['orderDate'] = pd.to_datetime(data['orderDate'])

rfm= data.groupby('customerId').agg({'orderDate':"max",
	'orderId':"count",'amount':"sum"})
rfm['day'] = (PRESENT - rfm['orderDate']).dt.days



rfm = rfm[['day','orderId','amount']]

rfm.columns=['recency','frequency','monetary']
rfm['recency'] = rfm['recency'].astype(int)


rfm['r_quartile'] = pd.qcut(rfm['recency'].rank(method='first'),5, ['1','2','3','4','5'],duplicates='raise')
rfm['f_quartile'] = pd.qcut(rfm['frequency'].rank(method='first'),5, ['1','2','3','4','5'],duplicates='raise')
rfm['m_quartile'] = pd.qcut(rfm['monetary'].rank(method='first'),5, ['1','2','3','4','5'],duplicates='raise')


rfm['r_quartile'] = rfm['r_quartile'].astype(int)
rfm['f_quartile'] = rfm['f_quartile'].astype(int)
rfm['m_quartile'] = rfm['m_quartile'].astype(int)

rfm['fm_quartile'] = (rfm['r_quartile'] + rfm['m_quartile'])/2


rfm['RFM_Score'] = rfm.r_quartile.astype(str)+ rfm.f_quartile.astype(str) + rfm.m_quartile.astype(str)

print(rfm.head)

row_list =[] 
for index, rows in rfm.iterrows(): 
    my_list =[rows.r_quartile, rows.fm_quartile] 
    row_list.append(my_list) 

# the segments customers are divided into.
cat = ['champ','loyal','lost','recent','promising','hibernate','can_not_lose','at_risk','About ro sleep','need_att','pot_loyal']
seg = [0,0,0,0,0,0,0,0,0,0,0]
segment()
data1 = data1.groupby('customerId')['orderId'].apply(list)
prod = prod.groupby('event_id')['product_id'].apply(list)


bestproduct(cus_list, o_list)
for i in range(len(best_p)):
	print(best_p[i])
plt.pie(seg, labels=cat, startangle=90, autopct='%.1f%%')
plt.show()


#There is overlapping of segments in pie chart because for some segments number of customers are zero.
