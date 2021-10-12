

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
		self.df['RB'] = df.apply(lambda row : row[self.filenameCol][row[self.filenameCol].index(term)+len(term):row[self.filenameCol].index(term)+len(term)+search].lstrip('0'), axis = 1)
		
		term = ' S'
		search = 2
		self.df['Section Number'] = df.apply(lambda row : row[self.filenameCol][row[self.filenameCol].index(term)+len(term):row[self.filenameCol].index(term)+len(term)+search], axis = 1)

		self.df['Location'] = 'Not Found'

		term = "LH"
		self.df['Location'] = df.apply(lambda row : term if term in row[self.filenameCol] else row['Location']  , axis = 1)

		term = "RH"
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
		term = "CC"
		self.df['Location'] = df.apply(lambda row : term if term in row[self.filenameCol] else row['Location']  , axis = 1)
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


	def KSOLesion(self):

		self.df['Treatment'] = 'Not Specified'
		self.df['dpl'] = 'Not Specified'

		for RBGroup in RabbitDescriptions.keys():
			term = RBGroup
			self.df['Treatment'] = self.df.apply(lambda row : term if row['RB'] in RabbitDescriptions[RBGroup][1] else row['Treatment']  , axis = 1)
			self.df['dpl'] = self.df.apply(lambda row : RabbitDescriptions[RBGroup][0] if row['RB'] in RabbitDescriptions[RBGroup][1] else row['dpl']  , axis = 1)
		
		
		print(self.df.columns)
		for i in range(ROINumber+1):

			for stain in self.channel_names:
				if i == 0:
					Densitytitle = 'Background ' + stain + " Positive Cells Density (cells/mm^2)"
				else :	
					Densitytitle = 'Lesion '+ str(i) +' ' + stain + ' Positive Cells Density (cells/mm^2)'

				data = [self.df['Treatment'],self.df['RB'],self.df['dpl'], self.df['Section Number'],self.df['Location'], self.df[Densitytitle]]

				CCgraphdf = pd.concat(data, axis=1)
				index = ['dpl', "RB", 'Location']
				pivoted = CCgraphdf.pivot_table(index=index, values =  Densitytitle, aggfunc='mean')
				
				Savename = stain + " Average_Density_per_dpl.csv"
				CsvSave = os.path.join(SaveLoc, Savename)
				pivoted.to_csv(CsvSave, index=True)

				index = ["Treatment"]
				pivoted = CCgraphdf.pivot_table(index=index, columns = 'Location', values =  Densitytitle, aggfunc='mean')
				
				Savename = stain + " Average_Density_per_Loc.png"
				ax = pivoted.plot(kind="bar")
				ax.set_title(Savename)
				plt.xticks(rotation=45)
				if debug:
					plt.show()
				figSave = os.path.join(SaveLoc, Savename)
				plt.savefig(figSave, bbox_inches='tight')




RabbitDescriptions = {
		'007dpl_5ul' : [7,[ '1', '2', '3', '5', '9', '16', '19']],
		'014dpl_5ul' : [14,[ '4', '6', '10', '21', '23']],
		'021dpl_5ul' : [21,[ '7', '8', '17', '20', '22']],
		'056dpl_5ul' : [56,['13', '27', '28', '29']],
		'180dpl_5ul' : [180,['43', '44']],

		'056dpl_5ul_Glut' : [56,['14']],
		'180dpl_5ul_Glut' : [180,['45']],

		'007dpl_1ul' : [7,['24', '25']],

		'007dpl_0.35ul' : [7,['26', '48']],
		'014dpl_0.35ul' : [14,['35', '51']],
		'021dpl_0.35ul' : [21,['34','50']],

		'021dpl_0.35ul&5ul' : [21,['52']],

		'021dpl_5ul_Clemastine' : [21,[ '31', '32', '33']],
		'021dpl_5ul_PI-88' : [21,[ '41', '42', '43']],

		'Normal' : [0,['46' , '47']],
		'8wk_Cup0.2' : [56,['36', '37']],
		'8wk_Cup0.5' : [56,['38' , '39']],
}



			







from settings import Settings
settings = Settings()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pathlib
import os

debug = False 

setup = settings.folder_dicts[7]
imagefolpath = setup['Path']
Resultsfolpath = os.path.join(imagefolpath,'Results')
Summarypath = os.path.join(Resultsfolpath,'SummaryGood.csv')

head, tail = os.path.split(Summarypath)
SaveLoc = os.path.join(head,"Summary_DataVis")
if not os.path.exists(SaveLoc):
	os.mkdir(SaveLoc)

namChannels = setup['channels']
cell_types_to_analyze = setup['cell_types_to_analyze']
ROINumber = setup['ROINumber']

Summary = pd.read_csv(Summarypath)	
dO = DataOrganizer(df = Summary, channel_names=namChannels , cell_types = cell_types_to_analyze )
#dO.Cuprizone()
dO.KSOLesion()





