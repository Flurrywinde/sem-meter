import sys
import pandas as pd

class sem:
	our_circuits = {
		"HVAC 1-35 40A(W)": .333,
		"Workshop 3-xx 50a(W)": 1,
		"Dryer 4-32 30a(W)": .25,
		"Washer 5-31 20a(W)": .25,
		"Playhouse 8-xx 50a(W)": 1,
		"Trailer 11-22 30a(W)": 1,
		#"Office 15-30 15a(W)": .5,
		}

	short_names = {
		"HVAC 1-35 40A(W)": 'HVAC',
		"Workshop 3-xx 50a(W)": 'Workshop',
		"Dryer 4-32 30a(W)": 'Dryer',
		"Washer 5-31 20a(W)": 'Washer',
		"Playhouse 8-xx 50a(W)": 'Playhouse',
		"Trailer 11-22 30a(W)": 'Trailer',
		"Office 15-30 15a(W)": 'Office',
		}

	def __init__(self, csvfile):
		self.csvfile = csvfile
		# Filter out circuits that aren't ours
		usecols = self.our_circuits.keys()
		# Retain a copy of list of our circuits (without date column added below)
		self.datacols = list(usecols).copy()
		# Add the Date column
		usecols = ['Time Bucket (Time zone in which phone used(UTC-7))'] + list(usecols)
		# Read in the data (just our circuits)
		df = pd.read_csv(self.csvfile, usecols=usecols)
		# Rename the date column for convenience
		df.rename(columns={'Time Bucket (Time zone in which phone used(UTC-7))': 'Date'}, inplace=True)
		# Convert dates to datetime type
		df['Date'] = pd.to_datetime(df['Date'])
		# Chop off the time
		df['Date'] = pd.to_datetime(df['Date']).dt.date  # , format='%Y-%m-%d'
		self.df = df

	def exe(self, start_date, end_date, duedate, charge, kwh):
		self.start_date = start_date
		self.end_date = end_date
		# Filter out date range
		#df1 = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
		self.df = self.df[self.df['Date'].between(self.start_date, self.end_date)]

		# Wh to KWh conversion
		self.df[self.datacols] = self.df[self.datacols].apply(lambda x: x / 1000)

		# Add spreadsheet formulae
		rowcount = len(self.df)
		alphabet = 'abcdefgh'
		curalpha = 0
		colnames = {}
		for series_name, series in self.df.items():
			if series_name in self.our_circuits.keys():
				colnames[curalpha+1] = series_name
				#print(f'{series_name}\t{our_circuits[series_name]}')
				# 12/13/25-now getting warning: /home/kanon/bin/sem-meterp:60: FutureWarning: Setting an item of incompatible dtype is deprecated and will raise an error in a future version of pandas. Value '=sum(f2:f32' has dtype incompatible with float64, please explicitly cast to a compatible dtype first.
				#Google says to: df['column_name'] = df['column_name'].astype('object')
				# but how? Also, maybe making new row like this is "horrible" https://stackoverflow.com/questions/10715965/create-a-pandas-dataframe-by-appending-one-row-at-a-time but for now, jerryrig it
				# self.df.loc[rowcount, series_name] = self.df.loc[rowcount, series_name].astype('str')  # didn't work ('object' type didn't either)
				self.df[series_name] = self.df[series_name].astype(object)
				self.df.loc[rowcount, series_name] = f'=sum({alphabet[curalpha]}2:{alphabet[curalpha]}{rowcount+1})'  # zero-based, so rowcount is next row after last row
				self.df.loc[rowcount+1, series_name] = self.our_circuits[series_name]
				self.df.loc[rowcount+2, series_name] = f'={alphabet[curalpha]}{rowcount+2}*{alphabet[curalpha]}{rowcount+3}'
			elif series_name == 'Date':
				self.df.loc[rowcount, series_name] = 'Subtotal'
				self.df.loc[rowcount+1, series_name] = 'Multiplier'
				self.df.loc[rowcount+2, series_name] = 'Our KWh'
			curalpha += 1
		self.df.loc[rowcount+3, 'Date'] = 'Our Total KWh'
		self.df.loc[rowcount+3, colnames[2]] = f'=sum(b{rowcount+4}:{alphabet[curalpha-1]}{rowcount+4})'
		self.df.loc[rowcount+4, 'Date'] = 'Due Date'
		self.df.loc[rowcount+4, colnames[2]] = f'{duedate}'
		self.df.loc[rowcount+5, 'Date'] = 'Amount Due'
		self.df.loc[rowcount+5, colnames[2]] = f'=dollar({charge}, 2)'
		self.df.loc[rowcount+6, 'Date'] = 'KWh Billed'
		self.df.loc[rowcount+6, colnames[2]] = f'{kwh}'
		self.df.loc[rowcount+7, 'Date'] = 'Our %'
		self.df.loc[rowcount+7, colnames[2]] = f'=b{rowcount+5}/b{rowcount+8}'
		self.df.loc[rowcount+8, 'Date'] = 'Our $'
		self.df.loc[rowcount+8, colnames[2]] = f'=dollar(b{rowcount+9}*b{rowcount+7}, 2)'
		self.df.loc[rowcount+9, 'Date'] = 'Elena $'
		self.df.loc[rowcount+9, colnames[2]] = f'=dollar(b{rowcount+7}-b{rowcount+10}, 2)'


		# Rename columns to short names
		self.df.rename(columns=self.short_names, inplace=True)
		#self.df.loc[len(df)] = [values]
		#print(df)

		# Convert to xlsx format
		xlsname = f'sem_{duedate_data} ({start_date} to {end_date}).xlsx'
		writer = pd.ExcelWriter(xlsname, engine='xlsxwriter')
		self.df.to_excel(writer, sheet_name='Sheet1', index=False)

		# Access the workbook and worksheet objects to apply formatting:
		workbook = writer.book
		worksheet = writer.sheets['Sheet1']

		# Set column widths and apply number formats. For example, set the width of the 'Score' column to 15 and format it as a number with one decimal place:

		# Set column width and format
		#worksheet.set_column('B:B', 15, workbook.add_format({'num_format': '0.0'}))

		#Apply background colors using conditional formatting. For instance, highlight cells in the 'Score' column that are above 80 with a green background:

		# Apply conditional formatting for scores above 80
		#worksheet.conditional_format('B2:B4', {'type': 'cell', 'criteria': '>', 'value': 80, 'format': workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})})

		# For alignment, use the add_format method to define alignment settings and apply them to specific columns:

		# Right-align 2nd column
		#left_align = workbook.add_format({'align': 'left'})
		right_align = workbook.add_format({'align': 'right'})
		worksheet.set_column('B:B', 20, right_align)

		# You can also apply formatting to headers. Define a header format and apply it to the first row:

		# Define header format
		header_format = workbook.add_format({
			'bold': True,
			'bg_color': '#008080',
			'font_color': '#ffffff',
			'border': 1
		})

		# Apply header format to the first row
		for col_num, value in enumerate(self.df.columns.values):
			worksheet.write(0, col_num, value, header_format)

		# Finally, save the file:
		writer.save()

		# Return data as csv
		return self.df.to_csv(sep='\t', index=False)
