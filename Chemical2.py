import bs4
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
"""
The aim of this project was to find all CAS numbers, boiling points and melting using the main website described below.
As the site contains several "subsites" that direct you to the compound, another request was required. 
Some information might have been repeated because there was more than one "subsites" that direct you to the same information. 
Neither melting point nor boiling point were possible to find for some compounds because the site didn't have that information.
The huge difficulty was to access the correct information once those "subsites" (c_links) were not displayed in the same way
"""

r= requests.get('https://www.chemeurope.com/en/encyclopedia/List_of_organic_compounds.html')
soup= BeautifulSoup(r.text,'lxml')

compounds=soup.select('ul')

#print(len(compounds)) -->39
#first element in compounds = 4
#last element = 29
site=[]
for c in range(4,30,1):
	compounds_links = compounds[c].select('.chem_internallink')
	for i in compounds_links:
		link=str(i).split('href=')[1].split(' ')[0].replace('"', '')
		site.append(link)

final=[]
for c_links in site:
	r2= requests.get(c_links)
	sou2p = BeautifulSoup(r2.text,'lxml')
	table=sou2p.find('table',{'class':'toccolours'})
	
	d={}
	final.append(d)
	try:
		for i in table:
			i=str(i)
			pat=(r'\d{2,7}-\d{2}-\d{1}')
			num = re.findall(pat,i)
			if len(num)!=0:
				d['CAS number']=str(num).replace('\n','')
				
	except:
		pass
	try:
		boiling= table.find_all('p',{'class':'chem_chapter'})[1]
		boiling=table.select('.chem_chapter')[1].get_text()
		d['boiling']=str(boiling).replace('\n','')
	except:
			pass
		
	try:
		melting=table.select('.chem_chapter')[0].get_text()
		d['melting']=str(melting).replace('\n','')	
	except:
		pass

	try:
		for i in table:
			i=str(i)
			pat=(r'\d{0,9}.\d{0,6} g/mol')
			num = re.findall(pat,i)
			if len(num)!=0:
				d['mw']=str(num).replace('\n','')		
	except:
		pass
	
all_compounds = pd.DataFrame(final)
all_compounds.to_csv('compounds_in_chemeurope.csv', index=False,header=True)

