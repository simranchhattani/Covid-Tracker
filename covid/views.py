from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os



# Create your views here.

def count(request):
	# URL for scrapping data
	url = 'https://www.mohfw.gov.in/'

  
	# get URL html 
	page = requests.get(url) 
	soup = BeautifulSoup(page.text, 'html.parser') 


	active=soup.find_all('li', class_="bg-blue")
	for i in active:
	    active_case = i.find_all("strong", class_="mob-hide")[1].text
	    active_case=int(active_case.split()[0])
	    print("ACTIVE CASES: ",active_case)


	recover=soup.find_all('li', class_="bg-green")
	for i in recover:
	    recover_case = i.find_all("strong", class_="mob-hide")[1].text
	    recover_case=int(recover_case.split()[0])
	    print("RECOVERED: ",recover_case)


	death=soup.find_all('li', class_="bg-red")
	for i in death:
	    death = i.find_all("strong", class_="mob-hide")[1].text
	    death=int(death.split()[0])
	    print("DEATHS: ",death)

	total_cases = active_case + recover_case + death
	recovery_rate = recover_case/total_cases*100
	print("TOTAL CASES:",total_cases)
	print("RECOVERY RATE:",round(recovery_rate,2),"%")


	#Pie chart, where the slices will be ordered and plotted counter-clockwise:
	labels = 'Active', 'Recovered', 'Deaths'
	sizes = [active_case, recover_case, death]
	explode = (0.12, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

	fig1, ax1 = plt.subplots()


	theme = plt.get_cmap('hsv')
	ax1.set_prop_cycle("color", [theme(1. * i / len(sizes))
	                             for i in range(len(sizes))])
	ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
	        shadow=True, startangle=90,)
	ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
	plt.title("\n Covid-19 INDIA \n")
	plt.show()
	my_path = os.path.abspath(__file__) #figures out the absolute path for you in case your working directory moves around.
	fig1.savefig('C:\\Users\\abc\\Desktop\\covid_tracker\\covid\\static\\covid\\Covid_Pie_Chart.png', bbox_inches='tight') 
	context = {"total":total_cases,
	            "active":active_case,
	            "recovered":recover_case,
	            "deaths":death
		      }
	return render(request,"covid/frontend.html",context)
	 
