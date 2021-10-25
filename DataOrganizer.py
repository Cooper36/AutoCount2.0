

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
		self.df['RB'] = df.apply(lambda row : row[self.filenameCol][row[self.filenameCol].index(term)+len(term):row[self.filenameCol].index(term)+len(term)+search].lstrip('0').strip(), axis = 1)
		
		"""term = ' S'
		search = 2
		self.df['Section Number'] = df.apply(lambda row : row[self.filenameCol][row[self.filenameCol].index(term)+len(term):row[self.filenameCol].index(term)+len(term)+search], axis = 1)"""

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


	def KSO_DCOLesion(self):

		self.df['Treatment'] = 'Not Specified'
		self.df['dpl'] = 'Not Specified'

		for RBGroup in RabbitDescriptions.keys():
			term = RBGroup
			self.df['Treatment'] = self.df.apply(lambda row : term if row['RB'] in RabbitDescriptions[RBGroup][1] else row['Treatment']  , axis = 1)
			self.df['dpl'] = self.df.apply(lambda row : RabbitDescriptions[RBGroup][0] if row['RB'] in RabbitDescriptions[RBGroup][1] else row['dpl']  , axis = 1)
		
		
		CCgraphdf = self.df
		print(CCgraphdf['dpl'].values)
		dpl = sorted(set(CCgraphdf['dpl'].values))
		CCgraphdf.reset_index(inplace=True)
		CCgraphdf['ValueNumber'] = "Not Stratified"
		
		#add individual value numbers for stratification
		for i in dpl:
			dpldf = CCgraphdf[CCgraphdf['dpl'] == i]
			val = 1

			for index in dpldf.index:
				CCgraphdf.loc[index,'ValueNumber'] = val
				val = val+1
		
		CCgraphdf.reset_index(inplace=True)
		CCgraphdf.set_index(['dpl', "RB"], inplace=True)		

		"""_____________________________________________________________________________________________________________________________"""

		#Organize and display Area data for each lesion
		values = []
		SEMTitles = []
		SEMs = []
		countsTitles = []
		counts = []
		#get column titles for all ROIs and calculate SEM/count for summarized csv
		for i in range(ROINumber+1):
			if i == 0:
				Densitytitle = 'Background Area (mm^2)'
				Series = CCgraphdf[Densitytitle]
				SEMTitles.append('Bkg Area SEM')
				SEMs.append(Series.groupby(by=['dpl']).sem())
				countsTitles.append('Bkg Area counts')
				counts.append(Series.groupby(by=['dpl']).size())
			else :	
				Densitytitle = 'Lesion '+ str(i) +' Area (mm^2)'
				Series = CCgraphdf[Densitytitle]
				SEMTitles.append('Lesion '+str(i)+' SEM')
				SEMs.append(Series.groupby(by=['dpl']).sem())
				countsTitles.append('Lesion '+str(i)+' Area counts')
				counts.append(Series.groupby(by=['dpl']).size())
			values.append(Densitytitle)


		#make pivot table
		pivoted = CCgraphdf.pivot_table(index=['dpl'], values = values, aggfunc='mean')

		#save graph with mean and SEM
		ax = pivoted.plot(kind="bar", yerr=SEMs,capsize=5)
		Savename = "Average Area_per_dpl.png"
		ax.set_title(Savename)
		plt.xticks(rotation=0)
		plt.legend(loc ='lower left')
		plt.ylabel('Area (mm^2)')
		if debug:
			plt.show()
		figSave = os.path.join(SaveLoc, Savename)
		plt.savefig(figSave, bbox_inches='tight')

		#Add SEMs and counts to Summary csv
		for i in range(len(SEMTitles)):
			pivoted[SEMTitles[i]] = SEMs[i]
			pivoted[countsTitles[i]] = counts[i]
		#Reorder columns for easy copy and paste into Prism
		reorder = []
		RelativeTitles = []
		RelativeSEMTitles = []
		RelativeCountTitles = []
		Relreorder = []
		for i in range(len(values)):
			reorder.extend([values[i], SEMTitles[i], countsTitles[i]])
			RelativeTitles.append('Relative: ' + values[i])
			RelativeSEMTitles.append('Relative SEM: ' + values[i])
			RelativeCountTitles.append('Relative count: ' + values[i])
			Relreorder.extend([RelativeTitles[i], RelativeSEMTitles[i], RelativeCountTitles[i]])



		pivoted = pivoted.reindex(reorder, axis=1)

		#Create Relative Summary csv from specified ROI, 0 is Background, 1 is ROI 1 ... etc.
		Rel_to_ROI = 0
		for i in range(len(RelativeTitles)):
			pivoted[RelativeTitles[i]] = pivoted[values[i]] / pivoted[values[Rel_to_ROI]]
			pivoted[RelativeSEMTitles[i]] = (pivoted[SEMTitles[i]] / pivoted[values[i]]) * pivoted[RelativeTitles[i]]
			pivoted[RelativeCountTitles[i]] = counts[i]


		#Save Relative Summay csv
		Savename = "Average Area Summary stats.csv"
		CsvSave = os.path.join(SaveLoc, Savename)
		pivoted.to_csv(CsvSave, index=True)


		#Create individual values csv
		Pivcolumns = ['ValueNumber']
		pivoted = CCgraphdf.pivot_table(index=['dpl'], columns = Pivcolumns,  values = values, aggfunc='mean')

		#Save individual value csv
		Savename = "Average Area individual values.csv"
		CsvSave = os.path.join(SaveLoc, Savename)
		pivoted.to_csv(CsvSave, index=True)










		"""_____________________________________________________________________________________________________________________________"""

		#Per channel density over time
		for stain in self.channel_names:
			values = []
			SEMTitles = []
			SEMs = []
			countsTitles = []
			counts = []


			#get column titles for all ROIs and calculate SEM/count for summarized csv
			for i in range(ROINumber+1):
				if i == 0:
					Densitytitle = 'Background ' + stain + " Positive Cells Density (cells/mm^2)"
					Series = CCgraphdf[Densitytitle]
					SEMTitles.append('Bkg '+stain+' SEM')
					SEMs.append(Series.groupby(by=['dpl']).sem())
					countsTitles.append('Bkg '+stain+' counts')
					counts.append(Series.groupby(by=['dpl']).size())
				else :	
					Densitytitle = 'Lesion '+ str(i) +' ' + stain + ' Positive Cells Density (cells/mm^2)'
					Series = CCgraphdf[Densitytitle]
					SEMTitles.append('Lesion '+str(i)+' SEM')
					SEMs.append(Series.groupby(by=['dpl']).sem())
					countsTitles.append('Lesion '+str(i)+' '+stain+' counts')
					counts.append(Series.groupby(by=['dpl']).size())
				values.append(Densitytitle)


			#make pivot table
			pivoted = CCgraphdf.pivot_table(index=['dpl'], values = values, aggfunc='mean')

			#save graph with mean and SEM
			ax = pivoted.plot(kind="bar", yerr=SEMs,capsize=5)
			Savename = stain + " Average_Density_per_dpl.png"
			ax.set_title(Savename)
			plt.xticks(rotation=0)
			plt.legend(loc ='lower left')
			plt.ylabel( stain +' Density (cell/mm^2)')
			if debug:
				plt.show()
			figSave = os.path.join(ChannelSave, Savename)
			plt.savefig(figSave, bbox_inches='tight')

			#Add SEMs and counts to Summary csv
			for i in range(len(SEMTitles)):
				pivoted[SEMTitles[i]] = SEMs[i]
				pivoted[countsTitles[i]] = counts[i]
			#Reorder columns for easy copy and paste into Prism
			reorder = []
			RelativeTitles = []
			RelativeSEMTitles = []
			RelativeCountTitles = []
			Relreorder = []
			for i in range(len(values)):
				reorder.extend([values[i], SEMTitles[i], countsTitles[i]])
				RelativeTitles.append('Relative: ' + values[i])
				RelativeSEMTitles.append('Relative SEM: ' + values[i])
				RelativeCountTitles.append('Relative count: ' + values[i])
				Relreorder.extend([RelativeTitles[i], RelativeSEMTitles[i], RelativeCountTitles[i]])



			pivoted = pivoted.reindex(reorder, axis=1)

			#Create Relative Summary csv from specified ROI, 0 is Background, 1 is ROI 1 ... etc.
			Rel_to_ROI = 0
			for i in range(len(RelativeTitles)):
				pivoted[RelativeTitles[i]] = pivoted[values[i]] / pivoted[values[Rel_to_ROI]]
				pivoted[RelativeSEMTitles[i]] = (pivoted[SEMTitles[i]] / pivoted[values[i]]) * pivoted[RelativeTitles[i]]
				pivoted[RelativeCountTitles[i]] = counts[i]


			#Save Relative Summay csv
			Savename = stain + " Summary stats.csv"
			CsvSave = os.path.join(ChannelSave, Savename)
			pivoted.to_csv(CsvSave, index=True)


			#Create individual values csv
			Pivcolumns = ['ValueNumber']
			pivoted = CCgraphdf.pivot_table(index=['dpl'], columns = Pivcolumns,  values = values, aggfunc='mean')

			#Save individual value csv
			Savename = stain + " individual values.csv"
			CsvSave = os.path.join(ChannelSave, Savename)
			pivoted.to_csv(CsvSave, index=True)

		"""_____________________________________________________________________________________________________________________________"""
		#Repeat the above for cell types
		for cell_type in self.cell_types:
			values = []
			SEMTitles = []
			SEMs = []
			countsTitles = []
			counts = []
			

			#get column titles for all ROIs and calculate SEM/count for summarized csv
			for i in range(ROINumber+1):
				if i == 0:
					Densitytitle = 'Background '+ cell_type +  ' Density (cells/mm^2)'
					Series = CCgraphdf[Densitytitle]
					SEMTitles.append('Bkg '+cell_type+' SEM')
					SEMs.append(Series.groupby(by=['dpl']).sem())
					countsTitles.append('Bkg '+cell_type+' counts')
					counts.append(Series.groupby(by=['dpl']).size())
				else :	
					Densitytitle = 'Lesion '+ str(i) + ' ' + cell_type +  ' Density (cells/mm^2)'
					Series = CCgraphdf[Densitytitle]
					SEMTitles.append('Lesion '+str(i)+' SEM')
					SEMs.append(Series.groupby(by=['dpl']).sem())
					countsTitles.append('Lesion '+str(i)+' '+stain+' counts')
					counts.append(Series.groupby(by=['dpl']).size())
				values.append(Densitytitle)


			#make pivot table
			pivoted = CCgraphdf.pivot_table(index=['dpl'], values = values, aggfunc='mean')

			#save graph with mean and SEM
			ax = pivoted.plot(kind="bar", yerr=SEMs,capsize=5)
			Savename = cell_type + " Average_Density_per_dpl.png"
			ax.set_title(Savename)
			plt.xticks(rotation=90)
			plt.legend(loc ='lower left')
			plt.ylabel( cell_type +' Density (cell/mm^2)')
			if debug:
				plt.show()
			figSave = os.path.join(Cell_type_Save, Savename)
			plt.savefig(figSave, bbox_inches='tight')

			#Add SEMs and counts to Summary csv
			for i in range(len(SEMTitles)):
				pivoted[SEMTitles[i]] = SEMs[i]
				pivoted[countsTitles[i]] = counts[i]
			#Reorder columns for easy copy and paste into Prism
			reorder = []
			RelativeTitles = []
			RelativeSEMTitles = []
			RelativeCountTitles = []
			Relreorder = []
			for i in range(len(values)):
				reorder.extend([values[i], SEMTitles[i], countsTitles[i]])
				RelativeTitles.append('Relative: ' + values[i])
				RelativeSEMTitles.append('Relative SEM: ' + values[i])
				RelativeCountTitles.append('Relative count: ' + values[i])
				Relreorder.extend([RelativeTitles[i], RelativeSEMTitles[i], RelativeCountTitles[i]])



			pivoted = pivoted.reindex(reorder, axis=1)

			#Create Relative Summary csv from specified ROI, 0 is Background, 1 is ROI 1 ... etc.
			Rel_to_ROI = 0
			for i in range(len(RelativeTitles)):
				pivoted[RelativeTitles[i]] = pivoted[values[i]] / pivoted[values[Rel_to_ROI]]
				pivoted[RelativeSEMTitles[i]] = (pivoted[SEMTitles[i]] / pivoted[values[i]]) * pivoted[RelativeTitles[i]]
				pivoted[RelativeCountTitles[i]] = counts[i]


			#Save Relative Summay csv
			Savename = cell_type + " Summary stats.csv"
			CsvSave = os.path.join(Cell_type_Save, Savename)
			pivoted.to_csv(CsvSave, index=True)


			#Create individual values csv
			Pivcolumns = ['ValueNumber']
			pivoted = CCgraphdf.pivot_table(index=['dpl'], columns = Pivcolumns,  values = values, aggfunc='mean')

			#Save individual value csv
			Savename = cell_type + " individual values.csv"
			CsvSave = os.path.join(Cell_type_Save, Savename)
			pivoted.to_csv(CsvSave, index=True)




		"""_____________________________________________________________________________________________________________________________"""

		#compute calculated Fields, specific to staining protocol (need to specify)
		Staintype = "DCO"

		if Staintype == "KSO":
			calculated_FieldsTitles = {
									"Percent Olig2Lineage_per_DAPI" : ['OligoLineage','DAPI'],
									"Percent NonOligo_per_DAPI" : ['NonOligo','DAPI'],
									"Percent Sox2Astro_per_DAPI" : ['Sox2Astro','DAPI'],
									"Percent ProlifNonOligo_per_DAPI" : ['ProlifNonOligo','DAPI'],
									"Percent ActiveOPC_per_OligoLineage" : ['ActiveOPC','OligoLineage'],
									"Percent ProlifOPC_per_OligoLineage" : ['ProlifOPC','OligoLineage'],
									#"Percent Activated&ProliferativeOPCs_per_ActiveOPC" : ['Activated&ProliferativeOPCs','ActiveOPC'],
			}
		if Staintype == "DCO":
			calculated_FieldsTitles = {
									"Percent Olig2Lineage_per_DAPI" : ['OligoLineage','DAPI'],
									"Percent NonOligo_per_DAPI" : ['NonOligo','DAPI'],
									"Percent Mature Oligodendrocyte_per_OligoLineage" : ['Mature Oligodendrocyte','OligoLineage'],
									"Percent OPC_per_OligoLineage" : ['OPC','OligoLineage'],
									"Percent CC1+Olig2-_per_Mature Oligodendrocyte" : ['CC1+Olig2-',''],
			}

		for CalcField in calculated_FieldsTitles.keys():
			values = []
			SEMTitles = []
			SEMs = []
			countsTitles = []
			counts = []
			for i in range(ROINumber+1):
				if i == 0:
					
					CalcDensitytitle = 'Background '+ CalcField
					NumoratorDensitytitle = 'Background '+ calculated_FieldsTitles[CalcField][0] +  ' Density (cells/mm^2)'
					DenominatorDensitytitle = 'Background '+ calculated_FieldsTitles[CalcField][1] +  ' Density (cells/mm^2)'
					CalcSeries = CCgraphdf[NumoratorDensitytitle]/CCgraphdf[DenominatorDensitytitle] * 100
					CCgraphdf[CalcDensitytitle] = CalcSeries
					SEMTitles.append('Bkg '+CalcField+' SEM')
					SEMs.append(CalcSeries.groupby(by=['dpl']).sem())
					countsTitles.append('Bkg '+CalcField+' counts')
					counts.append(CalcSeries.groupby(by=['dpl']).size())
				else :	
					CalcDensitytitle = 'Lesion '+ str(i) + CalcField
					NumoratorDensitytitle = 'Lesion '+ str(i) + ' ' + calculated_FieldsTitles[CalcField][0] +  ' Density (cells/mm^2)'
					DenominatorDensitytitle = 'Lesion '+ str(i) + ' ' + calculated_FieldsTitles[CalcField][1] +  ' Density (cells/mm^2)'
					CalcSeries = CCgraphdf[NumoratorDensitytitle]/CCgraphdf[DenominatorDensitytitle] * 100
					CCgraphdf[CalcDensitytitle] = CalcSeries
					SEMTitles.append('Lesion '+str(i)+' '+CalcField+' SEM')
					SEMs.append(CalcSeries.groupby(by=['dpl']).sem())
					countsTitles.append('Lesion '+str(i)+' '+CalcField+' counts')
					counts.append(CalcSeries.groupby(by=['dpl']).size())
				values.append(CalcDensitytitle)
			
			pivoted = CCgraphdf.pivot_table(index=['dpl'], values = values, aggfunc='mean')

			#save graph with mean and SEM
			ax = pivoted.plot(kind="bar", yerr=SEMs,capsize=5)
			Savename = CalcField + " per_dpl.png"
			ax.set_title(Savename)
			plt.xticks(rotation=0)
			plt.legend(loc ='lower left')
			plt.ylabel( CalcField +' ('+calculated_FieldsTitles[CalcField][0]+'/'+calculated_FieldsTitles[CalcField][1]+')')
			if debug:
				plt.show()
			figSave = os.path.join(PercentCalcSave, Savename)
			plt.savefig(figSave, bbox_inches='tight')

			#Add SEMs and counts to Summary csv
			for i in range(len(SEMTitles)):
				pivoted[SEMTitles[i]] = SEMs[i]
				pivoted[countsTitles[i]] = counts[i]
			#Reorder columns for easy copy and paste into Prism
			reorder = []
			RelativeTitles = []
			RelativeSEMTitles = []
			RelativeCountTitles = []
			Relreorder = []
			for i in range(len(values)):
				reorder.extend([values[i], SEMTitles[i], countsTitles[i]])
				RelativeTitles.append('Relative: ' + values[i])
				RelativeSEMTitles.append('Relative SEM: ' + values[i])
				RelativeCountTitles.append('Relative count: ' + values[i])
				Relreorder.extend([RelativeTitles[i], RelativeSEMTitles[i], RelativeCountTitles[i]])



			pivoted = pivoted.reindex(reorder, axis=1)


			#Save Relative Summay csv
			Savename = CalcField + " Summary stats.csv"
			CsvSave = os.path.join(PercentCalcSave, Savename)
			pivoted.to_csv(CsvSave, index=True)


			#Create individual values csv
			Pivcolumns = ['ValueNumber']
			pivoted = CCgraphdf.pivot_table(index=['dpl'], columns = Pivcolumns,  values = values, aggfunc='mean')

			#Save individual value csv
			Savename = CalcField + " individual values.csv"
			CsvSave = os.path.join(PercentCalcSave, Savename)
			pivoted.to_csv(CsvSave, index=True)

		"""_____________________________________________________________________________________________________________________________"""
			

				
		for stain in self.channel_names:
			values = []
			forgraph = []
			AreaTitles = []
			ROITitles = []
			for i in range(ROINumber+1):
				AreaTitles = []
				if i == 0:
					AreaTitles = ('Background Area (mm^2)')
					Densitytitle = 'Background ' + stain + " Positive Cells Density (cells/mm^2)"
					ROItitle = 'Background'

					
				else :
					AreaTitles = 'Lesion '+ str(i) +' Area (mm^2)'
					Densitytitle = 'Lesion '+ str(i) +' ' + stain + ' Positive Cells Density (cells/mm^2)'
					ROItitle = 'Lesion '+ str(i)
				values.extend([AreaTitles, Densitytitle])
				forgraph.append([AreaTitles, Densitytitle])
				ROITitles.append(ROItitle)
				
			print(values)
			pivoted = CCgraphdf.pivot_table(index=['dpl','ValueNumber'],  values = values, aggfunc='mean')


			#Save Relative Summay csv
			Savename = stain + " vs Area Scatterplot.csv"
			CsvSave = os.path.join(ScatterPlots, Savename)
			pivoted.to_csv(CsvSave, index=True)










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

setup = settings.folder_dicts[1]
imagefolpath = setup['Path']
Resultsfolpath = os.path.join(imagefolpath,'Results')
Summarypath = os.path.join(Resultsfolpath,'Summary.csv')

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
#dO.Cuprizone()
dO.KSO_DCOLesion()





