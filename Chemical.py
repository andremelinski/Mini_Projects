import bs4
from bs4 import BeautifulSoup
import requests
import pandas as pd

r= requests.get('https://www.chemeurope.com/en/encyclopedia/List_of_organic_compounds.html')
soup= BeautifulSoup(r.text,'lxml')

compounds=soup.select('ul')

#print(len(compounds)) -->39
#fir element in compounds = 4
#last element = 29

for c in range(4,30,1):
	links=(compounds[1].select('.chem_internallink'))
	compound_link=[]
	for i in links:	
		
		name=str(i).split('title=')[1].split('>')[0].replace('"', '')
		link=str(i).split('href=')[1].split(' ')[0].replace('"', '')
		compound_link.append(link)

	print(compound_link)
	''' 
	Searching inside of each compound-link
	'''
	final=[]
	for c_links in compound_link:
		
		r2= requests.get(c_links)
		sou2p = BeautifulSoup(r2.text,'lxml')
		table=sou2p.find('table',{'class':'toccolours'})
		
		d={}
		try:
			name=table.find('th', {'style':"background: #F8EABA; text-align: center;"}).get_text()
			d['name']=str(name).replace('\n','')
		except:
			pass

		try:
			#boiling= table.find_all('p',{'class':'chem_chapter'})[1]
			boiling=table.select('.chem_chapter')[1].get_text()
			d['boiling']=str(boiling).replace('\n','')
			final.append(d)

		except:
			pass
		
		try:
			melting=table.select('.chem_chapter')[0].get_text()
			d['melting']=str(melting).replace('\n','')
			final.append(d)

		except:
			pass



#print(final)
#a class="chem_internallink --> massa molar
#span class="reflink plainlinksneverexpand" -->CAS number
#p class="chem_chapter" --> melting point and boiling point
