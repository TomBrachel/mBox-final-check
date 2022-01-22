# # -----for all vol product - Fix Columns
import pandas as pd
# from openpyxl import Workbook
import os, sys
from shutil import copyfile
# ===CONSTANTS:
sources_per_group_owner_dict = {
	"NMC": {
		"Cellcom": [
			"NMCFTN","NMCFT", "HEDSMN", "HEDSM", 
			"HS100N", "HS100", "NMCFUN"
			],
		"HotMobile" : [
			"HedArzi_'RBT - דמ\"ש$'", "NMC_'RBT - הורדות$'",
			 "NMC_'RBT - דמ\"ש$'", "HedArzi_'RBT - הורדות$'"
			],
		"Orange": [
			"FunTone_ATTN הד ארצי בע\"מ",
			"4U_ATTN אן. אם. סי יונייטד אנטרטיינמנט בע\"מ",
			"4U_ATTN הד ארצי בע\"מ", 
			"FunTone_ATTN אן. אם. סי יונייטד אנטרטיינמנט בע\"מ"
			],
		"Pelephone": [
			"NMC_Damash", "Hed_harzi_Damash", 
			"Hed_harzi_DT", "NMC_DT"
			]
	},
	"Helicon": {
		"Cellcom": [
			"HELFTN","HELFT", "UNIFTN", "UNIFT", 
			"HUNFDN", "EMIFTN", "ERBFTN", "EMIFT",
			"ERBFT", "HUNFD"
			],
		"Orange": [
			"FunTone_ATTN הליקון בע\"מ",
			"4U_ATTN הליקון בע\"מ",
			],
		"Pelephone": [
			"Universal_DT", "Universal_Damash", 
			"Helicon_DT", "Helicon_Damash",
			"EMI_DT", "EMI_Damash"
			]
	},
	"mBox": {
		"Cellcom": [
			"MBOX2N","MBOX2", "BOXL2N", "BOXFDN", 
			"ARBFDN", "MBXSON", "MBXSO", "BOXFD",
			"BXNA2N", "BOXL2", "ARBFD"
			],
		"HotMobile" : [
			"Hapil_'RBT - דמ\"ש$'", "Hapil_'RBT - הורדות$'",
			 "Sony_'RBT - דמ\"ש$'", "Sony_'RBT - הורדות$'",
			 "Mbox_'RBT - דמ\"ש$'", "Mbox_'RBT - הורדות$'"
			],
		"Orange": [
			"4U_ATTN אם.בוקס בע\"מ - תוכן",
			"FunTone_ATTN אם.בוקס בע\"מ - תוכן"
			],
		"Pelephone": [
			"Hapil_Damash", "Hapil_DT", "mBox_Damash",
			"mBox_DT", "Sony_Damash", "Sony_DT"
			]
	}
}

owners_per_group_owner_dict = {
		"NMC": [
			"NMC","הד-ארצי",
		],
		"Helicon": [
			"EMI2008","Helicon Hip Hop", "Helicon Label", "Universal", 
			"Universal Music", "הליקון", "ישראפון"
		],
		"mBox": [
			"Anova Music","Bolo Music", "EH Media", "Digistage", 
			"New Sound", "Music Rocket", "Kamea",
			"Elmadamin","Nassar Studios", "Kilmeh", "Mobile Streams", 
			"MBox", "Joy Records", "SonyBMG",
			"אדרת","הפיל", "היי פידליטי", "ואזאנה יורם יצחק", 
			"נענע דיסק", "Music Rocket", "Kamea",
			"Elmadamin","יריב פז", "פדי הפקות", "האוזן השלישית", 
			"ניצוצות של קדושה", "אינזימה פאבלישינג", "יהונתן גטרו",
			"TheOrchard", "יריב מהטוב", "הילה קטש", "לייבלה/אשר ביטנסקי בע\"מ"
		],
}

sums_per_group_owner_dict = {
	"NMC": {
		"Cellcom": {
					"finle_exal":[],
					"file1":[],
					"exile":[],
					"without":[],

		}
		,
		"HotMobile" : {
					"finle_exal":[],
					"file1":[],
					"exile":[],
					"without":[],
			},
		"Orange": {
					"finle_exal":[],
					"file1":[],
					"exile":[],
					"without":[],
			},
		"Pelephone": [
			'intDownloads', 'dblCharge', 'dblRevenue'
			]
	},
	"Helicon": {
		"Cellcom": [
			'intDownloads', 'dblCharge', 'dblRevenue'
			],
		"Orange": [
			'intDownloads', 'dblCharge', 'dblRevenue'
			],
		"Pelephone": [
			'intDownloads', 'dblCharge', 'dblRevenue'
			]
	},
	"mBox": {
		"Cellcom": [
			'intDownloads', 'dblCharge', 'dblRevenue'
			],
		"HotMobile" : [
			'intDownloads', 'dblCharge', 'dblRevenue'
			],
		"Orange": [
			'intDownloads', 'dblCharge', 'dblRevenue'
			],
		"Pelephone": [
			'intDownloads', 'dblCharge', 'dblRevenue'
			]
	}
}


def Sum_agri(report_file, Operator):
	df = pd.read_excel(report_file, engine='openpyxl')
	Downloads = df.loc[df['Operator'] == Operator]['Downloads'].sum()
	Operator_Revenue = df.loc[df['Operator'] == Operator]['Operator Revenue'].sum()
	mBox_Income = df.loc[df['Operator'] == Operator]['mBox Income'].sum()
	return[Downloads, Operator_Revenue, mBox_Income]

	
#Sum_agri('z_ExportToContentOwners_Final.xlsx')



def get_df_by_group_owner(missing_file, group_owner, shit_name = 0):
	df = pd.read_excel(missing_file,shit_name, engine='openpyxl')
	print(group_owner)
	GO = sources_per_group_owner_dict[group_owner].keys()

	for i in GO:
		Sources = sources_per_group_owner_dict[group_owner][i]
		sum_intDownloads = 0
		sum_dblCharge = 0
		sum_dblRevenue = 0 
		if (i == 'Cellcom'):
			print('Cellcom: \n')
			df.loc[df['Operator'] == 'Cellcom']
			month = df['intMonth'][1]
			year = df['intYear'][1]
			dayt = str(year) + str(month) + '01' ##str
			for Sor in Sources:
					table_for_filters = 'DT_' + Sor + '_' + dayt + '.csv$'
					sum_intDownloads = sum_intDownloads + df.loc[df['Source'] == table_for_filters]['intDownloads'].sum()
					sum_dblCharge = sum_dblCharge + df.loc[df['Source'] == table_for_filters]['dblCharge'].sum()
					sum_dblRevenue = sum_dblRevenue + df.loc[df['Source'] == table_for_filters]['dblRevenue'].sum()

		
		else:
 			print( i + ': \n')
 			for Sor in Sources:
 					sum_intDownloads = sum_intDownloads + df.loc[df['Source'] == Sor]['intDownloads'].sum()
 					sum_dblCharge = sum_dblCharge + df.loc[df['Source'] == Sor]['dblCharge'].sum()
 					sum_dblRevenue = sum_dblRevenue + df.loc[df['Source'] == Sor]['dblRevenue'].sum()
		print('intDownloads: ')
		print(sum_intDownloads)
		print('dblCharge: ')
		print(sum_dblCharge)
		print('dblRevenue:')
		print(sum_dblRevenue)
		print('\n')



#get_df_by_group_owner('missing.xlsx', 'NMC', 0)



def get_df_by_group_owner_operator(missing_file, group_owner, operator, shit_name = 0):
	df = pd.read_excel(missing_file,shit_name, engine='openpyxl')
	Sources = sources_per_group_owner_dict[group_owner][operator]
	sum_intDownloads = 0
	sum_dblCharge = 0
	sum_dblRevenue = 0 
	if (operator == 'Cellcom'):
		df.loc[df['Operator'] == 'Cellcom']
		month = df['intMonth'][1]
		year = df['intYear'][1]
		dayt = str(year) + str(month) + '01' ##str
		for Sor in Sources:
				table_for_filters = 'DT_' + Sor + '_' + dayt + '.csv$'
				sum_intDownloads = sum_intDownloads + df.loc[df['Source'] == table_for_filters]['intDownloads'].sum()
				sum_dblCharge = sum_dblCharge + df.loc[df['Source'] == table_for_filters]['dblCharge'].sum()
				sum_dblRevenue = sum_dblRevenue + df.loc[df['Source'] == table_for_filters]['dblRevenue'].sum()

		
	else:
 		for Sor in Sources:
 				sum_intDownloads = sum_intDownloads + df.loc[df['Source'] == Sor]['intDownloads'].sum()
 				sum_dblCharge = sum_dblCharge + df.loc[df['Source'] == Sor]['dblCharge'].sum()
 				sum_dblRevenue = sum_dblRevenue + df.loc[df['Source'] == Sor]['dblRevenue'].sum()
	
	return [sum_intDownloads, sum_dblCharge, sum_dblRevenue]


#get_df_by_group_owner_operator('missing.xlsx', 'NMC', 'Orange', 0)




def sum_Verification(ver_file, Operator, sheet_name):
		finle_exal = pd.read_excel(ver_file, sheet_name, engine='openpyxl')
		for i, trial in finle_exal.iterrows():
			if trial[0] == Operator:
				return [trial[2], trial[3], trial[4]]



#1. recive first sum
#2. recive agri
#3. recive noan
#4. recive outcast
#5. create (1-(2+3+4))
#6. if (5 == 0) print 1 - 5 and be happy
#7. if (5 != 0) print 1 - 5 and continue



def passsum_everything(gruop_owner, ver_file, Report, Missing): #str, finle exal, file1, file missing
	sheet_name = 'Check ' + gruop_owner
	Sources = sources_per_group_owner_dict[gruop_owner].keys()
	for op in Sources:
		print('Cource: ')
		print(op)
		First_sum = sum_Verification(ver_file, op, sheet_name)
		print(First_sum)
		agri = Sum_agri(Report, op)
		print(agri)
		noan = get_df_by_group_owner_operator(Missing, gruop_owner, op, 0)
		print(noan)
		out_cast = get_df_by_group_owner_operator(Missing, gruop_owner, op, 1)
		print(out_cast)
		sum_of_all_shit = [(First_sum[0] - (agri[0] + noan[0] + out_cast[0])), (First_sum[1] - (agri[1] + noan[1] + out_cast[1])), (First_sum[2] - (agri[2] + noan[2] + out_cast[2]))]
		print(sum_of_all_shit)
		print('\n')
		if ((sum_of_all_shit[0]) == 0): print(':)')
		else: print(':(')
		

#month = df['intMonth'][1]

#print(pd.read_excel('Reports Verification_10.2021.xlsx', 'Check NMC', engine='openpyxl')

passsum_everything('NMC', 'Reports Verification_10.2021.xlsx', 'z_ExportToContentOwners_Final.xlsx', 'missing.xlsx')

#print(sum_Verification('Reports Verification_10.2021.xlsx','Cellcom,' 'Check NMC', ))














