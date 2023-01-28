class DataOrganizer(object):
	"""A class to organize data for graphpad and make preview graphs"""
	def __init__(self, df, channel_names, cell_types):

		self.df = df

		self.channel_names = channel_names

		self.cell_types = cell_types

		self.columns = list(df.columns)

		self.filenameCol = self.columns[0]




	def strfinder(self, string, term, looklen):
		#find a number in a substring of length looklen that trails term
		if looklen > 0:
			start = string.index(term) + len(term)
			substring = string[start : start+looklen]

		if looklen < 0:
			start = string.index(term)
			substring = string[start+looklen : start]

		return substring

	def strfindUntil(self, string, term, end):
		#find a values between the end of term, until end
		try:
			start = string.index(term) + len(term)
			until = string.index(end,start) 
			substring = string[start : until]
		except:
			substring = "Not found"

		return substring

	def strfindBefore(self, string, term, until):
		#find a values between the end of term, until end
		#Reverse string
		Rstring = string[::-1]
		
		
		
		try:
			Rterm = term[::-1]
			end = Rstring.index(Rterm) + len(Rterm)
			untilval = Rstring.index(until, end) 
			substring = Rstring[end : untilval]
			substring = substring[::-1]
		except:
			substring = "Not found"

		return substring

	'''
	def name_plot(pivotdf,, name):
	    data = pivotdf.loc[sex, name]
	    DataFrame.plot.bar(x=None, y=None, **kwargs)
	'''
	def Neostigmine7dplRoopa(self):
		term = 'Slide'
		search = 2
		self.df['Slide'] = self.df.apply(lambda row : row[self.filenameCol][row[self.filenameCol].index(term)+len(term):row[self.filenameCol].index(term)+len(term)+search].lstrip('0').strip(), axis = 1)
		
		self.df['Treatment'] = 'Not Found'

		termHD = "HighDose"
		self.df['Treatment'] = self.df.apply(lambda row : termHD if termHD in row[self.filenameCol] else row['Treatment']  , axis = 1)

		term = "HD"
		self.df['Treatment'] = self.df.apply(lambda row : termHD if term in row[self.filenameCol] else row['Treatment']  , axis = 1)

		term = "LowDose"
		self.df['Treatment'] = self.df.apply(lambda row : term if term in row[self.filenameCol] else row['Treatment']  , axis = 1)

		term = "Ctrl"
		self.df['Treatment'] = self.df.apply(lambda row : term if term in row[self.filenameCol] else row['Treatment']  , axis = 1)

		Savename = Dataname +"_For Excel.csv"
		CsvSave = os.path.join(SaveLoc, Savename)
		self.df.to_csv(CsvSave, index=True)

	
	def CuprizoneMNA(self):
		
		# Get RB number from filename
		term = 'RB'
		search = 2
		self.df['RB'] = self.df.apply(lambda row : row[self.filenameCol][row[self.filenameCol].index(term)+len(term):row[self.filenameCol].index(term)+len(term)+search].lstrip('0').strip(), axis = 1)
		
		term = 'MNA_S2'
		self.df['AP'] = self.df.apply(lambda row : 'Anterior' if term in row[self.filenameCol] else 'Posterior'  , axis = 1)

		term = 'Section'
		search = 1
		self.df['Section'] = self.df.apply(lambda row : row[self.filenameCol][row[self.filenameCol].index(term)+len(term):row[self.filenameCol].index(term)+len(term)+search], axis = 1)

		self.df['Hemisphere'] = 'NA'

		term = "LH"
		self.df['Hemisphere'] = self.df.apply(lambda row : term if term in row[self.filenameCol] else row['Hemisphere']  , axis = 1)

		term = "RH"
		self.df['Hemisphere'] = self.df.apply(lambda row : term if term in row[self.filenameCol] else row['Hemisphere']  , axis = 1)


		self.df['Location'] = 'Not Found'

		term = "CC"
		self.df['Location'] = self.df.apply(lambda row : term if term in row[self.filenameCol] else row['Location']  , axis = 1)

		term = "CR"
		self.df['Location'] = self.df.apply(lambda row : term if term in row[self.filenameCol] else row['Location']  , axis = 1)

		term = "IC"
		self.df['Location'] = self.df.apply(lambda row : term if term in row[self.filenameCol] else row['Location']  , axis = 1)
		
		term = "ICfas"
		self.df['Location'] = self.df.apply(lambda row : term if term in row[self.filenameCol] else row['Location']  , axis = 1)

		self.df['Treatment'] = 'Not Specified'
		self.df['dpl'] = 'Not Specified'

		for RBGroup in RabbitDescriptions.keys():
			term = RBGroup
			self.df['Treatment'] = self.df.apply(lambda row : term if row['RB'] in RabbitDescriptions[RBGroup][1] else row['Treatment']  , axis = 1)
			self.df['dpl'] = self.df.apply(lambda row : RabbitDescriptions[RBGroup][0] if row['RB'] in RabbitDescriptions[RBGroup][1] else row['dpl']  , axis = 1)
		
		self.df['Treatment'] = self.df.apply(lambda row : "NP Ctrl" if row['NP Ctrl'] == 'Yes' else row['Treatment']  , axis = 1)
		

		Savename = Dataname +"_For Excel.csv"
		CsvSave = os.path.join(SaveLoc, Savename)
		self.df.to_csv(CsvSave, index=True)
		
		
	def PVTransplants(self):
		
		term = 'Animal'
		search = 1
		self.df['Animal'] = self.df.apply(lambda row : row[self.filenameCol][row[self.filenameCol].index(term)+len(term):row[self.filenameCol].index(term)+len(term)+search].lstrip('0').strip(), axis = 1)
		
		term = 'Slide'
		search = 2
		self.df['Slide'] = self.df.apply(lambda row : row[self.filenameCol][row[self.filenameCol].index(term)+len(term):row[self.filenameCol].index(term)+len(term)+search].lstrip('0').strip(), axis = 1)
		
		term = 'Section'
		search = 1
		self.df['Section'] = self.df.apply(lambda row : row[self.filenameCol][row[self.filenameCol].index(term)+len(term):row[self.filenameCol].index(term)+len(term)+search].lstrip('0').strip(), axis = 1)
		
	
		Savename = Dataname +"_For Excel.csv"
		CsvSave = os.path.join(SaveLoc, Savename)
		self.df.to_csv(CsvSave, index=True)

	def Cuprizone(self):
		# Get RB number from filename
		term = 'RB'
		search = 2
		self.df['RB'] = self.df.apply(lambda row : row[self.filenameCol][row[self.filenameCol].index(term)+len(term):row[self.filenameCol].index(term)+len(term)+search].lstrip('0').strip(), axis = 1)

		"""term = ' S'
		search = 2
		self.df['Section Number'] = df.apply(lambda row : row[self.filenameCol][row[self.filenameCol].index(term)+len(term):row[self.filenameCol].index(term)+len(term)+search], axis = 1)"""

		self.df['Location'] = 'Not Found'

		term = "LH"
		self.df['Location'] = self.df.apply(lambda row : term if term in row[self.filenameCol] else row['Location']  , axis = 1)

		term = "RH"
		self.df['Location'] = self.df.apply(lambda row : term if term in row[self.filenameCol] else row['Location']  , axis = 1)

		term = "CC"
		self.df['Location'] = self.df.apply(lambda row : term if term in row[self.filenameCol] else row['Location']  , axis = 1)
		
		self.df['Location cont'] = 'NA'
		self.df['Location cont'] = self.df.apply(lambda row : self.strfinder(row[self.filenameCol],"_c",-1) if self.strfinder(row[self.filenameCol],"_c",-1).isnumeric() else row['Location cont']  , axis = 1)
		Normal = ['46' , '47']
		Cup02 = ['36', '37']
		Cup05 = ['38' , '39']
		CupRecov = ['63' , '64', '65']

		self.df['Treatment'] = 'Not Specified'
		
		term = "WT"
		self.df['Treatment'] = self.df.apply(lambda row : term if row['RB'] in Normal else row['Treatment']  , axis = 1)

		term = "Cuprizone_0.2"
		self.df['Treatment'] = self.df.apply(lambda row : term if row['RB'] in Cup02 else row['Treatment']  , axis = 1)
		
		term = "Cuprizone_0.5"
		self.df['Treatment'] = self.df.apply(lambda row : term if row['RB'] in Cup05 else row['Treatment']  , axis = 1)

		term = "Cuprizone_8+2"
		self.df['Treatment'] = self.df.apply(lambda row : term if row['RB'] in CupRecov else row['Treatment']  , axis = 1)

		Savename = Dataname +"_For Excel.csv"
		CsvSave = os.path.join(SaveLoc, Savename)
		self.df.to_csv(CsvSave, index=True)



	def KSO_DCOLesion(self):
		# Get RB number from filename
		term = 'RB'
		search = 2
		self.df['RB'] = self.df.apply(lambda row : row[self.filenameCol][row[self.filenameCol].index(term)+len(term):row[self.filenameCol].index(term)+len(term)+search].lstrip('0').strip(), axis = 1)
		
		"""term = ' S'
		search = 2
		self.df['Section Number'] = df.apply(lambda row : row[self.filenameCol][row[self.filenameCol].index(term)+len(term):row[self.filenameCol].index(term)+len(term)+search], axis = 1)"""

		self.df['Location'] = 'Not Found'

		term = "LH"
		self.df['Location'] = self.df.apply(lambda row : term if term in row[self.filenameCol] else row['Location']  , axis = 1)

		term = "RH"
		self.df['Location'] = self.df.apply(lambda row : term if term in row[self.filenameCol] else row['Location']  , axis = 1)

		self.df['Treatment'] = 'Not Specified'
		self.df['dpl'] = 'Not Specified'

		for RBGroup in RabbitDescriptions.keys():
			term = RBGroup
			self.df['Treatment'] = self.df.apply(lambda row : term if row['RB'] in RabbitDescriptions[RBGroup][1] else row['Treatment']  , axis = 1)
			self.df['dpl'] = self.df.apply(lambda row : RabbitDescriptions[RBGroup][0] if row['RB'] in RabbitDescriptions[RBGroup][1] else row['dpl']  , axis = 1)
		
		Savename = Dataname +"_For Excel.csv"
		CsvSave = os.path.join(SaveLoc, Savename)
		self.df.to_csv(CsvSave, index=True)



	def DGILesion(self):
		# Get RB number from filename
		term = 'RB'
		end = '_'
		self.df['RB'] = self.df.apply(lambda row :self.strfindUntil(string = row[self.filenameCol], term = term, end = end) , axis = 1)
		
		term = '_Section_'
		search = 1
		self.df['Section Number'] = self.df.apply(lambda row : row[self.filenameCol][row[self.filenameCol].index(term)+len(term):row[self.filenameCol].index(term)+len(term)+search], axis = 1)

		self.df['Location'] = 'Not Found'

		term = "LH"
		self.df['Location'] = self.df.apply(lambda row : term if term in row[self.filenameCol] else row['Location']  , axis = 1)

		term = "RH"
		self.df['Location'] = self.df.apply(lambda row : term if term in row[self.filenameCol] else row['Location']  , axis = 1)

		term = "CC"
		self.df['Location'] = self.df.apply(lambda row : term if term in row[self.filenameCol] else row['Location']  , axis = 1)


		self.df['Treatment'] = 'Not Specified'
		self.df['dpl'] = 'Not Specified'

		for RBGroup in RabbitDescriptions.keys():
			term = RBGroup
			self.df['Treatment'] = self.df.apply(lambda row : term if row['RB'] in RabbitDescriptions[RBGroup][1] else row['Treatment']  , axis = 1)
			self.df['dpl'] = self.df.apply(lambda row : RabbitDescriptions[RBGroup][0] if row['RB'] in RabbitDescriptions[RBGroup][1] else row['dpl']  , axis = 1)
		
		Savename = Dataname +"_For Excel.csv"
		CsvSave = os.path.join(SaveLoc, Savename)
		self.df.to_csv(CsvSave, index=True)

			
	def Plates(self):
			# Get RB number from filename
			term = '_ImageID'
			until = '_'
			self.df['Well'] = self.df.apply(lambda row :self.strfindBefore(string = row[self.filenameCol], term = term, until = until) , axis = 1)

			term = '_BMP'
			end = '_'
			self.df['BMP Dose'] = self.df.apply(lambda row :self.strfindUntil(string = row[self.filenameCol], term = term, end = end) , axis = 1)
			
			term = '_Virus'
			end = '_'
			self.df['Virus'] = self.df.apply(lambda row :self.strfindUntil(string = row[self.filenameCol], term = term, end = end) , axis = 1)
			
			"""self.df['Virus'] = 'Not Found'
			self.df['BMP'] = 'Not Found'


			BMP0 = ['A4','B4','C1','D1', 'F2', 'F4']
			BMP5 = ['A5','B5','C2', 'D2']
			BMP50 = ['A6', 'B6', 'C3', 'D3']

			Ctrl = ['A4','A5','A6','B4','B5','B6']
			Noggin = ['C1','C2','C3', 'D1','D2','D3']
			GFminus = ['F2']
			GFplus = ['F4']
			
			term = "0"
			self.df['BMP'] = self.df.apply(lambda row : term if row['Well'] in BMP0 else row['BMP']  , axis = 1)

			term = "5"
			self.df['BMP'] = self.df.apply(lambda row : term if row['Well'] in BMP5 else row['BMP']  , axis = 1)

			term = "50"
			self.df['BMP'] = self.df.apply(lambda row : term if row['Well'] in BMP50 else row['BMP']  , axis = 1)

			term = "Ctrl"
			self.df['Virus'] = self.df.apply(lambda row : term if row['Well'] in Ctrl else row['Virus']  , axis = 1)

			term = "Noggin"
			self.df['Virus'] = self.df.apply(lambda row : term if row['Well'] in Noggin else row['Virus']  , axis = 1)

			term = "GFminus"
			self.df['Virus'] = self.df.apply(lambda row : term if row['Well'] in GFminus else row['Virus']  , axis = 1)

			term = "GFplus"
			self.df['Virus'] = self.df.apply(lambda row : term if row['Well'] in GFplus else row['Virus']  , axis = 1)
			"""
			Savename = Dataname +"_For Excel.csv"
			CsvSave = os.path.join(SaveLoc, Savename)
			self.df.to_csv(CsvSave, index=True)


	def Farah(self):
			# Get RB number from filename

			term = '_ImageID-'
			end = '.'
			self.df['ImageID'] = self.df.apply(lambda row :self.strfindUntil(string = row[self.filenameCol], term = term, end = end) , axis = 1)
			
			self.df['Condition'] = 'Not Found'

			term = "KO"
			search = 'KO'
			self.df['Condition'] = self.df.apply(lambda row : term if search in row[self.filenameCol] else row['Condition']  , axis = 1)

			term = "WT"
			search = '(wild type)'
			self.df['Condition'] = self.df.apply(lambda row : term if search in row[self.filenameCol] else row['Condition']  , axis = 1)

			term = '_AN'
			end = '_'
			self.df['Animal'] = self.df.apply(lambda row :self.strfindUntil(string = row[self.filenameCol], term = term, end = end) , axis = 1)
			
			Savename = Dataname +"_For Excel.csv"
			CsvSave = os.path.join(SaveLoc, Savename)
			self.df.to_csv(CsvSave, index=True)

from settings import Settings
settings = Settings()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pathlib
import os

debug = False 

setup = settings.folder_dicts[32]
RabbitDescriptions = settings.RabbitDescriptions
Dataname = setup['name']
imagefolpath = setup['Path']
DataOrganizerType = setup['DataOrganizer']
Resultsfolpath = os.path.join(imagefolpath,'Results')
Summarypath = os.path.join(Resultsfolpath,Dataname+'_Summary.csv')

head, tail = os.path.split(Summarypath)
SaveLoc = os.path.join(head,"Summary_DataVis")
if not os.path.exists(SaveLoc):
	os.mkdir(SaveLoc)

ChannelSave = os.path.join(SaveLoc,"Channel Densities")
if not os.path.exists(ChannelSave):
	os.mkdir(ChannelSave)

Cell_type_Save = os.path.join(SaveLoc,"Cell Types Densities")
if not os.path.exists(Cell_type_Save):
	os.mkdir(Cell_type_Save)

PercentCalcSave = os.path.join(SaveLoc,"Percentage Calculations")
if not os.path.exists(PercentCalcSave):
	os.mkdir(PercentCalcSave)

ScatterPlots = os.path.join(SaveLoc,"ScatterPlots")
if not os.path.exists(ScatterPlots):
	os.mkdir(ScatterPlots)

namChannels = setup['channels']
cell_types_to_analyze = setup['cell_types_to_analyze']
ROINumber = setup['ROINumber']

Summary = pd.read_csv(Summarypath)	
dO = DataOrganizer(df = Summary, channel_names=namChannels , cell_types = cell_types_to_analyze )

if DataOrganizerType == 'KSO_DCOLesion':
	dO.KSO_DCOLesion()

elif DataOrganizerType == 'Cuprizone':
	dO.Cuprizone()

elif DataOrganizerType == 'PVTransplants':
	dO.PVTransplants()

elif DataOrganizerType == 'CuprizoneMNA':
	dO.CuprizoneMNA()

elif DataOrganizerType == 'Neostigmine7dplRoopa':
	dO.Neostigmine7dplRoopa()

elif DataOrganizerType == 'DGILesion':
	dO.DGILesion()

elif DataOrganizerType == 'Plates':
	dO.Plates()

elif DataOrganizerType == 'Farah':
	dO.Farah()

else:
	print('DataOrganizer type not selected')