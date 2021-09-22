

class DataOrganizer(object):
	"""A class to organize data for graphpad and make preview graphs"""
	def __init__(self, df, channel_names, cell_types):

		self.df = df

		self.channel_names = channel_names

		self.cell_types = cell_types

		self.columns = list(df.columns)

		self.filenameCol = self.columns[0]

		# Get RB number from filename
		term = 'RB'
		search = 2
		self.df['RB'] = df.apply(lambda row : row[self.filenameCol][row[self.filenameCol].index(term)+len(term):row[self.filenameCol].index(term)+len(term)+search], axis = 1)
		
		term = ' S'
		search = 2
		self.df['Section Number'] = df.apply(lambda row : row[self.filenameCol][row[self.filenameCol].index(term)+len(term):row[self.filenameCol].index(term)+len(term)+search], axis = 1)

		self.df['Location'] = 'Not Found'

		term = "LH"
		self.df['Location'] = df.apply(lambda row : term if term in row[self.filenameCol] else row['Location']  , axis = 1)

		term = "RH"
		self.df['Location'] = df.apply(lambda row : term if term in row[self.filenameCol] else row['Location']  , axis = 1)
		
		term = "CC"
		self.df['Location'] = df.apply(lambda row : term if term in row[self.filenameCol] else row['Location']  , axis = 1)


	def strfinder(self, string, term, looklen):
		#find a number in a substring of length looklen that trails term
		if looklen > 0:
			start = string.index(term) + len(term)
			substring = string[start : start+looklen]

		if looklen < 0:
			start = string.index(term)
			substring = string[start+looklen : start]

		return substring

	'''
	def name_plot(pivotdf,, name):
	    data = pivotdf.loc[sex, name]
	    DataFrame.plot.bar(x=None, y=None, **kwargs)
	'''
	def Cuprizone(self):
		self.df['Location cont'] = 'NA'
		self.df['Location cont'] = self.df.apply(lambda row : self.strfinder(row[self.filenameCol],"_c",-1) if self.strfinder(row[self.filenameCol],"_c",-1).isnumeric() else row['Location cont']  , axis = 1)
		Normal = ['46' , '47']
		Cup02 = ['36', '37']
		Cup05 = ['38' , '39']

		self.df['Treatment'] = 'Not Specified'
		
		term = "WT"
		self.df['Treatment'] = self.df.apply(lambda row : term if row['RB'] in Normal else row['Treatment']  , axis = 1)

		term = "Cuprizone_0.2"
		self.df['Treatment'] = self.df.apply(lambda row : term if row['RB'] in Cup02 else row['Treatment']  , axis = 1)
		
		term = "Cuprizone_0.5"
		self.df['Treatment'] = self.df.apply(lambda row : term if row['RB'] in Cup05 else row['Treatment']  , axis = 1)


		
		for stain in self.channel_names:

			Densitytitle = "Lesion 1 "+stain+" Positive Cells Density (cells/mm^2)"

			data = [self.df['Treatment'],self.df['RB'], self.df['Section Number'], self.df['Location'], self.df[Densitytitle]]

			CCgraphdf = pd.concat(data, axis=1)
			index = ["Treatment", "RB"]
			pivoted = CCgraphdf.pivot_table(index=index, columns = 'Location', values =  Densitytitle, aggfunc='mean')
			
			Savename = stain + " Average_Density_per_Loc.csv"
			CsvSave = os.path.join(SaveLoc, Savename)
			pivoted.to_csv(CsvSave, index=True)

			index = ["Treatment"]
			pivoted = CCgraphdf.pivot_table(index=index, columns = 'Location', values =  Densitytitle, aggfunc='mean')
			
			Savename = stain + " Average_Density_per_Loc.png"
			ax = pivoted.plot(kind="bar")
			ax.set_title(Savename)
			plt.xticks(rotation=90)
			if debug:
				plt.show()
			figSave = os.path.join(SaveLoc, Savename)
			plt.savefig(figSave, bbox_inches='tight')


		for cell_type in self.cell_types:

			Densitytitle = "Lesion 1 "+cell_type+" Density (cells/mm^2)"

			data = [self.df['Treatment'],self.df['RB'], self.df['Section Number'], self.df['Location'], self.df[Densitytitle]]

			CCgraphdf = pd.concat(data, axis=1)
			index = ["Treatment", "RB"]
			pivoted = CCgraphdf.pivot_table(index=index, columns = 'Location', values =  Densitytitle, aggfunc='mean')
			
			Savename = cell_type + " Average_Density_per_Loc.csv"
			CsvSave = os.path.join(SaveLoc, Savename)
			pivoted.to_csv(CsvSave, index=True)

			index = ["Treatment"]
			pivoted = CCgraphdf.pivot_table(index=index, columns = 'Location', values =  Densitytitle, aggfunc='mean')
			
			Savename = cell_type + " Average_Density_per_Loc.png"
			ax = pivoted.plot(kind="bar")
			ax.set_title(Savename)
			if debug:
				plt.show()
			figSave = os.path.join(SaveLoc, Savename)
			plt.savefig(figSave, bbox_inches='tight')



			







from settings import Settings
settings = Settings()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pathlib
import os

debug = False 

path = "/Users/jjmc/Desktop/Working Folder/Normal and Cuprizone DCO/Images/Results/SummaryGood.csv"
Summary = pd.read_csv(path)	

head, tail = os.path.split(path)
SaveLoc = os.path.join(head,"SummaryData_Vis")
if not os.path.exists(SaveLoc):
	os.mkdir(SaveLoc)

setup = settings.folder_dicts[0]
namChannels = setup['channels']
cell_types_to_analyze = setup['cell_types_to_analyze']
dO = DataOrganizer(df = Summary, channel_names=namChannels , cell_types = cell_types_to_analyze )
dO.Cuprizone()





