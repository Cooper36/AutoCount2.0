


class Settings:
    """A class to store all settings."""

    def __init__(self):
        #Define rabbits numbers
        self.RabbitDescriptions = {
        '003dpl_5ul' : [3,[ '94', '96']],
        '007dpl_5ul' : [7,[ '1', '2', '3', '5', '9', '19']],
        '014dpl_5ul' : [14,[ '4', '6', '10', '21', '23','91','92','93','70','71']],
        '021dpl_5ul' : [21,[ '7', '8', '17', '20', '22','87','89']],
        '056dpl_5ul' : [56,['13', '27', '28', '29','83', '85','86','69']],
        '180dpl_5ul' : [180,['43', '44', '45',]],

        '056dpl_5ul_Glut' : [56,['14']],
        #'180dpl_5ul_Glut' : [180,['45']],

        '007dpl_1ul' : [7,['24', '25']],


        '007dpl_0.35ul' : [7,['26', '48','49','60']],
        '014dpl_0.35ul' : [14,['35', '51','54','59']],
        '021dpl_0.35ul' : [21,['34','50','53','56']],

        '007dpl_0.35ul&5ul' : [7,['61']],
        '014dpl_0.35ul&5ul' : [14,['57']],
        '021dpl_0.35ul&5ul' : [21,['52']],

        '021dpl_5ul_Cont.Clemastine' : [21,[ '31', '32', '33','67','68','77']],
        '056dpl_5ul_Cont.Clemastine' : [56,[ '79', '80', '82','84']],
        '056dpl_5ul_EarlyClemastine' : [56,[ '73', '74', '90']],
        '056dpl_5ul_LateClemastine' : [56,[ '72', '75', '76','81']],

        '021dpl_5ul_PI-88' : [21,[ '40','41', '42',]],
        

        'Normal' : [0,['46' , '47', '58']],
        '8wk_Cup0.2' : [56,['36', '37']],
        '8wk_Cup0.5' : [56,['38' , '39']],


}

        # Define folders for input of data
        self.folder_dicts = [
            {
                'name' : '0_JCmac',

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,
            
                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' :1.5385,

                # Define the number of ROIs you want to draw
                'ROINumber' : 1,

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","CC1","594_ch","Olig2"],

                # Path to folder containing images to be analyzed
                'Path' : "/Users/jjmc/Desktop/Working Folder/Normal and Cuprizone DCO/Images",

                # Cell types to analyze
                'cell_types_to_analyze' : ['OPC', 'Oligo', 'NonOligo'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,
            },
            {
                'name' : '1_LargeLesionDCO',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 2,

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","CC1","594_ch","Olig2"],
                'gammas' : [0.75,0.75,1,0.25],
                'RelativeIntensityThreshold' : [[1,5],[1.2,2],[1.2,2],[2,3]],

                # Path to folder containing images to be analyzed
                'Path' : "\\Users\\jjmc1\\Desktop\\Python\\AutoCount2.0\\LargeLesionDCO",

                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','OPC', 'Mature Oligodendrocyte', 'NonOligo','CC1+Olig2-'],

                # Do you want to use the keras models (slow)
                'useKeras' : False,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : 'KSO_DCOLesion',

                'PercentCalcs' : [['NonOligo','DAPI'],['Mature Oligodendrocyte','OligoLineage'],['OPC','OligoLineage']]

            },
            {
                'name' : '2_FMSize calculation JCWindows',

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,
            
                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,

                # Define the number of ROIs you want to draw
                'ROINumber' : 1,

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","FM","blank","blank"],

                # Path to folder containing images to be analyzed
                'Path' : "\\Users\\jjmc1\\Documents\\Small Lesion FM",

                # Cell types to analyze
                'cell_types_to_analyze' : [],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,
            },
            {
                'name' : '3_FMSize 4x calculation JCmac',

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 4x images, pixel/micron
                'scale' : 0.615,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 3,

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","FM","blank1","blank2"],

                # Path to folder containing images to be analyzed
                'Path' : "/Users/jjmc/Desktop/Small Lesion FM/Test",

                # Cell types to analyze
                'cell_types_to_analyze' : [],

                # Do you want to use the keras models (slow)
                'useKeras' : False,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,
            },
            {
                'name' : '4_RoopaMouseWindow',

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 4x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 2,

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","CC1","Olig2"],

                # Path to folder containing images to be analyzed
                'Path' : "\\Users\\jjmc1\\Desktop\\roopa mouse",

                # Cell types to analyze
                'cell_types_to_analyze' : ['OligoLineage','OPC', 'Mature Oligodendrocyte', 'NonOligo','CC1+Olig2-'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,
            },
            {
                'name' : '5_RoopaMouseMac',

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 4x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 1,

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","CC1","Olig2"],

                # Path to folder containing images to be analyzed
                'Path' : "/Users/jjmc/Documents/Roopa Test images",

                # Cell types to analyze
                'cell_types_to_analyze' : ['OligoLineage','OPC', 'Mature Oligodendrocyte', 'NonOligo','CC1+Olig2-'],

                # Do you want to use the keras models (slow)
                'useKeras' : False,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,
            },
            {
                'name' : '6_SettingParametersDCO',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 1,

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","CC1","594_ch","Olig2"],
                'gammas' : [0.75,0.75,1,0.75],
                'RelativeIntensityThreshold' : [[1,5],[1.2,2],[1.2,2],[2,3]],

                # Path to folder containing images to be analyzed
                # Path to folder containing images to be analyzed
                #'Path' : "C:\\Users\\jjmc1\\Desktop\\Control KSO DCO\\DCO",
                #'Path' : "/Users/jjmc/Desktop/Control KSO DCO/DCO",
                'Path' : "/Users/jjmc/Documents/DCO Test",
                
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','OPC', 'Mature Oligodendrocyte', 'NonOligo','CC1+Olig2-'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : False,

                # DataOrganizer type
                'DataOrganizer' : 'KSO_DCOLesion',

                'PercentCalcs' : [['NonOligo','DAPI'],['Mature Oligodendrocyte','OligoLineage'],['OPC','OligoLineage']]


                
            },
            {
                'name' : '7_SettingParametersKSO',
                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,
                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 4x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 0,

                # Name each channel present, in order (must be consistent for all images)

                'channels' : ["DAPI_ch","Ki67","Sox2","Olig2"],
                'gammas' : [0.75,0.75,1,0.25],
                'RelativeIntensityThreshold' : [[1,5],[3,5],[3,5],[1.2,2]],

                # Path to folder containing images to be analyzed
                'Path' : "C:\\Users\\jjmc1\\Desktop\\Control KSO DCO\\KSO",

                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','ActiveOPC', 'ProlifOPC', 'NonOligo', 'Sox2Astro','ProlifNonOligo',],

                # Do you want to use the keras models (slow)
                'useKeras' : False,

                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,
                'PercentCalcs' : [],

                'PerilesionAnalysis' : False,
            },
            {
                'name' : '8_RoopaNeostigmineLesionSize',

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 4x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 1,

                # Name each channel present, in order (must be consistent for all images)

                'channels' : ["Solochrome"],

                # Path to folder containing images to be analyzed
                'Path' : "C:\\Users\\jjmc1\\Documents\\solochrome mouse lesions JC\\Tiff",

                # Cell types to analyze
                'cell_types_to_analyze' : [],

                # Do you want to use the keras models (slow)
                'useKeras' : False,

                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,
            },
            {
                'name' : '9_LargeLesionKSO',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 2,

                # Name each channel present, in order (must be consistent for all images)

                'channels' : ["DAPI_ch","Ki67","Sox2","Olig2"],
                'gammas' : [0.75,0.75,1,0.25],
                'RelativeIntensityThreshold' : [[1,5],[3,5],[3,5],[1.2,2]],

                # Path to folder containing images to be analyzed
                'Path' : "C:\\Users\\jjmc1\\Desktop\\Python\\AutoCount2.0\\LargeLesionKSO",

                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','ActiveOPC', 'ProlifOPC', 'NonOligo', 'Sox2Astro','ProlifNonOligo', 'Activated-ProliferativeOPCs'],

                # Do you want to use the keras models (slow)
                'useKeras' : False,

                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # DataOrganizer type
                'DataOrganizer' : 'KSO_DCOLesion',

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : False,

                # DataOrganizer type
                'DataOrganizer' : 'KSO_DCOLesion',
            },
            {
                'name' : '10_Rich PV Transplants',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 3,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 1,

                # Name each channel present, in order (must be consistent for all images)

                'channels' : ["DAPI_ch","MBP","mCherry","hNA"],
                'gammas' : [0.75,0.75,1,0.25],
                'RelativeIntensityThreshold' : [[1,5],[3,5],[3,5],[3,5]],

                # Path to folder containing images to be analyzed
                #'Path' : "Y:\\People\\Rich\\__Transplants\\_Transplant Master Folder\\PV-NES-GFP & PV-NLS-GFP shiverer\\IHC master folder\\Transplant 1 - PV-NES&PV-NLS_MBP-hNA IHC images\\Tiff\\New images",
                'Path' : "Y:\\People\\Rich\\__Transplants\\_Transplant Master Folder\\PV-NES-GFP & PV-NLS-GFP shiverer\\IHC master folder\\Transplant 1 - PV-NES&PV-NLS_MBP-hNA IHC images\\Tiff",
                #'Path' : "Y:\\People\\Rich\\Transplant_MBP-hNA\\Tiff",
                #'Path' : "C:\\Users\\jjmc1\\Desktop\\New folder",
                

                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'Human Cell','Myelinating Human Cell'],

                # Do you want to use the keras models (slow)
                'useKeras' : False,

                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,                

                # DataOrganizer type
                'DataOrganizer' : 'PVTransplants',

                'PercentCalcs' : [],

                'PerilesionAnalysis' : True,
            },
            {
                'name' : '11_Cuprizone MNA',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 3,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 1,

                # Name each channel present, in order (must be consistent for all images)

                'channels' : ["DAPI_ch","MBP","APP","NF"],

                # Path to folder containing images to be analyzed
                'Path' : "/Users/jjmc/Desktop/Cuprizone+Untreated MNA",

                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI'],

                # Do you want to use the keras models (slow)
                'useKeras' : False,

                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,
            },
            {
                'name' : '12_Roopa Neostigmine_7dplRNAscope',
                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 2,

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","PLP","594_ch","Olig2RS"],
                'gammas' : [0.75,0.75,1,0.75],

                # Path to folder containing images to be analyzed
                'Path' : "Y:\\People\\James\\Neo7dpl PLP Olig2 RNAscope",
                #'Path' : "/Volumes/labdata/People/James/Neo7dpl PLP Olig2 RNAscope",
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OPCRS', 'PLP Mature Oligodendrocyte','OligoLineageRS'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,
            },

            {
                'name' : '13_Roopa Neostigmine_7dplCC1',
                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,
                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,
                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,
                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
                # Define the number of ROIs you want to draw
                'ROINumber' : 2,
                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","CC1","Olig2"],
                'gammas' : [0.75,0.75,1,0.75],
                # Path to folder containing images to be analyzed
                'Path' : "Y:\\People\\Roopa\\Staining\\Neostigmine experiment\\JCanalysis",
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','OPC', 'Mature Oligodendrocyte', 'NonOligo', 'CC1+Olig2-'],
                # Do you want to use the keras models (slow)
                'useKeras' : True,
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,
            },
            {
                'name' : '14_Cuprizone DCO',
                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,
                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,
                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,
                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
                # Define the number of ROIs you want to draw
                'ROINumber' : 1,
                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","CC1","594_ch","Olig2"],
                'gammas' : [0.75,0.75,1,0.75],
                # Path to folder containing images to be analyzed
                'Path' : "/Users/jjmc/Desktop/Working Folder/Normal and Cuprizone DCO/Images",
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','OPC', 'Mature Oligodendrocyte', 'NonOligo', 'CC1+Olig2-'],
                # Do you want to use the keras models (slow)
                'useKeras' : True,
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,
            },
            {
                'name' : '15_Treatment&Small',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 2,

                # Name each channel present, in order (must be consistent for all images)
                'channels' : ["DAPI_ch","Ki67","Sox2","Olig2"],
                'gammas' : [0.75,0.75,1,0.25],
                'RelativeIntensityThreshold' : [[1,5],[3,5],[3,5],[2,3]],

                # Path to folder containing images to be analyzed
                'Path' : "Y:\\People\\James\\Large vs Small Lesion Expt\\__Cell Dynamics\\KSO Small+Treatment",

                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','ActiveOPC', 'ProlifOPC', 'NonOligo', 'Sox2Astro','ProlifNonOligo', 'Activated-ProliferativeOPCs'],

                # Do you want to use the keras models (slow)
                'useKeras' : False,

                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : 'KSO_DCOLesion',

                'PercentCalcs' : [['NonOligo','DAPI'],['ProlifNonOligo','NonOligo'],['ActiveOPC','OligoLineage'],['ProlifOPC','OligoLineage'],['Activated-ProliferativeOPCs','ActiveOPC']]
            },
            {
                'name' : '16_KSOsmallLesion2',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 2,

                # Name each channel present, in order (must be consistent for all images)

                'channels' : ["DAPI_ch","Ki67","Sox2","Olig2"],
                'gammas' : [0.75,0.75,1,0.25],
                'RelativeIntensityThreshold' : [[1,5],[3,5],[3,5],[1.2,2]],

                # Path to folder containing images to be analyzed
                'Path' : "Y:\\People\\James\\Large vs Small Lesion Expt\\__Cell Dynamics\\KSO Small lesion 2\\Tiff\\Lesion",


                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','ActiveOPC', 'ProlifOPC', 'NonOligo', 'Sox2Astro','ProlifNonOligo', 'Activated-ProliferativeOPCs'],

                # Do you want to use the CC1 keras models (slow)
                'useKeras' : False,

                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : False,

                # DataOrganizer type
                'DataOrganizer' : 'KSO_DCOLesion',
            },
            {
                'name' : '17_KSOLarge&SmallCombined',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 2,

                # Name each channel present, in order (must be consistent for all images)

                'channels' : ["DAPI_ch","Ki67","Sox2","Olig2"],
                'gammas' : [0.75,0.25,0.25,0.25],
                'RelativeIntensityThreshold' : [[1,5],[3,5],[3,5],[2,3]],
                

                # Path to folder containing images to be analyzed
                'Path' : "Y:\\People\\James\\Large vs Small Lesion Expt\\__Cell Dynamics\\KSO Large&Small Lesions",
                #'Path' : '/Volumes/labdata/People/James/Large vs Small Lesion Expt/__Cell Dynamics/KSO Large&Small Lesions',    
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','ActiveOPC', 'ProlifOPC', 'NonOligo', 'Sox2Astro','ProlifNonOligo', 'Activated-ProliferativeOPCs'],

                # Do you want to use the CC1 keras models (slow)
                'useKeras' : False,

                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : 'KSO_DCOLesion',

                'PercentCalcs' : [['NonOligo','DAPI'],['ProlifNonOligo','NonOligo'],['ActiveOPC','OligoLineage'],['ProlifOPC','OligoLineage'],['Activated-ProliferativeOPCs','ActiveOPC']],
                'PerilesionAnalysis' : True,
            },
            {
                'name' : '18_KSOUntreated',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 2,

                # Name each channel present, in order (must be consistent for all images)

                'channels' : ["DAPI_ch","Ki67","Sox2","Olig2"],
                'gammas' : [0.75,0.75,1,0.25],
                'RelativeIntensityThreshold' : [[1,5],[3,5],[3,5],[1.25,3]],

                # Path to folder containing images to be analyzed
                'Path' : "Y:\\People\\James\\Untreated Animals\\KSO",

                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','ActiveOPC', 'ProlifOPC', 'NonOligo', 'Sox2Astro','ProlifNonOligo', 'Activated-ProliferativeOPCs'],

                # Do you want to use the CC1 keras models (slow)
                'useKeras' : False,

                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : 'KSO_DCOLesion',

                'PercentCalcs' : [['NonOligo','DAPI'],['ProlifNonOligo','NonOligo'],['ActiveOPC','OligoLineage'],['ProlifOPC','OligoLineage'],['Activated-ProliferativeOPCs','ActiveOPC']],
                'PerilesionAnalysis' : False,
            },
            {
                'name' : '19_KSOLarge&SmallCombined, RB43 Retest',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 2,

                # Name each channel present, in order (must be consistent for all images)

                'channels' : ["DAPI_ch","Ki67","Sox2","Olig2"],
                'gammas' : [0.75,0.75,1,0.3],
                'RelativeIntensityThreshold' : [[1,5],[3,5],[3,5],[1.3,1.8]],

                # Path to folder containing images to be analyzed
                'Path' : "Y:\\People\\James\\Large vs Small Lesion Expt\\__Cell Dynamics\\KSO Large&Small Lesions\\RB43 Reanalysis",
                #'Path' : "/Volumes/labdata/People/James/Large vs Small Lesion Expt/__Cell Dynamics/KSO Large&Small Lesions/RB43 Reanalysis",
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','ActiveOPC', 'ProlifOPC', 'NonOligo', 'Sox2Astro','ProlifNonOligo', 'Activated-ProliferativeOPCs'],

                # Do you want to use the CC1 keras models (slow)
                'useKeras' : False,

                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : 'KSO_DCOLesion',

                'PercentCalcs' : [['NonOligo','DAPI'],['ProlifNonOligo','NonOligo'],['ActiveOPC','OligoLineage'],['ProlifOPC','OligoLineage'],['Activated-ProliferativeOPCs','ActiveOPC']],
                'PerilesionAnalysis' : True,
            },
            {
                'name' : '20_DCOLarge&SmallCombined',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 2,

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","CC1","594_ch","Olig2"],
                'gammas' : [0.75,0.75,1,0.25],
                'RelativeIntensityThreshold' : [[1,5],[1.2,2],[1.2,2],[2,3]],
                #'RelativeIntensityThreshold' : [[1,5],[1.2,2],[1.2,2],[1.7,3]],

                # Path to folder containing images to be analyzed
                #'Path' : "Y:\\People\\James\\Large vs Small Lesion Expt\\__Cell Dynamics\\DCO Large&Small Lesions\\Lesion",
                'Path' : '/Volumes/LABDATA/People/James/Large vs Small Lesion Expt/__Cell Dynamics/DCO Large&Small Lesions/Lesion',
               
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','OPC', 'Mature Oligodendrocyte', 'NonOligo','CC1+Olig2-'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : 'KSO_DCOLesion',

                'PercentCalcs' : [['NonOligo','DAPI'],['Mature Oligodendrocyte','OligoLineage'],['OPC','OligoLineage']],
                'PerilesionAna20lysis' : True,

                'threshmethod' : 2,

            },
            {
                'name' : '21_DCOUntreated',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 2,

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","CC1","594_ch","Olig2"],
                'gammas' : [0.75,0.75,1,0.25],
                'RelativeIntensityThreshold' : [[1,5],[1.2,2],[1.2,2],[1.25,3]],

                # Path to folder containing images to be analyzed
                #'Path' : "Y:\\People\\James\\Untreated Animals\\DCO",
                #'Path' : "/Volumes/labdata/People/James/Untreated Animals/DCO",
                'Path' : "/Users/jjmc/Desktop/DCO",
                
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','OPC', 'Mature Oligodendrocyte', 'NonOligo','CC1+Olig2-'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : 'KSO_DCOLesion',

                'PercentCalcs' : [['NonOligo','DAPI'],['Mature Oligodendrocyte','OligoLineage'],['OPC','OligoLineage']]

            },
            {
                'name' : '22_DCO43 reanalysis',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 2,

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","CC1","594_ch","Olig2"],
                'gammas' : [0.75,0.75,1,0.25],
                'RelativeIntensityThreshold' : [[1,5],[1.2,2],[1.2,2],[1.3,1.8]],

                # Path to folder containing images to be analyzed
                'Path' : "Y:\\People\\James\\Large vs Small Lesion Expt\\__Cell Dynamics\\DCO Large&Small Lesions\\Lesion\\43 reanalysis",
                #'Path' : '/Volumes/labdata/People/James/Large vs Small Lesion Expt/__Cell Dynamics/DCO Large&Small Lesions/Lesion',
                #'Path' : "/Volumes/labdata/People/James/Large vs Small Lesion Expt/__Cell Dynamics/DCO Large&Small Lesions/Lesion/43 reanalysis",   
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','OPC', 'Mature Oligodendrocyte', 'NonOligo','CC1+Olig2-'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : 'KSO_DCOLesion',

                'PercentCalcs' : [['NonOligo','DAPI'],['Mature Oligodendrocyte','OligoLineage'],['OPC','OligoLineage']],

                'PerilesionAnalysis' : True,
            },
            {
                'name' : '23_DGISmall and Large',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 2,

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","GFAP","IBA1","Blank"],
                'gammas' : [0.75,0.75,1,0.25],
                'RelativeIntensityThreshold' : [[1,5],[1.2,2],[1.2,2],[1.3,1.8]],

                # Path to folder containing images to be analyzed
                'Path' : "Y:\\People\\James\\Large vs Small Lesion Expt\\Inflammation\\DGI small and Large",
                #'Path' : "/Volumes/labdata/People/James/Large vs Small Lesion Expt/Inflammation/DGI small and Large",   
                
                # Cell types to analyze
                'cell_types_to_analyze' : [],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : 'DGILesion',

                'PercentCalcs' : [],
                'PerilesionAnalysis' : False,

            },
             {
                'name' : '24_Test',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 2,

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","CC1","594_ch","Olig2"],
                'gammas' : [0.75,0.75,1,0.25],
                'RelativeIntensityThreshold' : [[1,5],[1.2,2],[1.2,2],[1.25,3]],

                # Path to folder containing images to be analyzed
                #'Path' : "Y:\\People\\James\\Untreated Animals\\DCO",
                #'Path' : "/Volumes/labdata/People/James/Untreated Animals/DCO",
                'Path' : "/Users/jjmc/Desktop/DCO/Test",
                
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','OPC', 'Mature Oligodendrocyte', 'NonOligo','CC1+Olig2-'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : 'KSO_DCOLesion',

                'PercentCalcs' : [['NonOligo','DAPI'],['Mature Oligodendrocyte','OligoLineage'],['OPC','OligoLineage']],

                'PerilesionAnalysis' : True,

            },
             {
                'name' : '25_JC-Lck-EGFP-Plate',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 1,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 140,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 3.0769,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 0,

                # Name each channel present (must be consistent for all images)
                'channels' : ["Phase","DAPI_ch","EGFP"],
                'gammas' : [1,0.75,1],
                'RelativeIntensityThreshold' : [[200,200],[1,5],[200,200]],

                # Path to folder containing images to be analyzed
                #'Path' : "Y:\\People\\James\\Transplant Expt\\Lck EGFP Titer",
                'Path' : "/Volumes/labdata/People/James/Transplant Expt/Lck EGFP Titer",
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'Alive', 'Dead','EGFP Tagged'],

                # Do you want to use the keras models (slow)
                'useKeras' : False,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : "Plates",

                'PercentCalcs' : [['Alive','DAPI'],['Dead','DAPI'],['EGFP Tagged','Alive']],

                'PerilesionAnalysis' : False,

                'threshmethod' : 1,

            },
             {
                'name' : '26_Cuprizone_8and8+2',
                
                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 1,

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","CC1","Olig2"],
                'gammas' : [0.75,0.75,1,0.25],
                'RelativeIntensityThreshold' : [[1,5],[1.2,2],[1.2,2],[2,3]],
                #'RelativeIntensityThreshold' : [[1,5],[1.2,2],[1.2,2],[1.7,3]],

                # Path to folder containing images to be analyzed
                'Path' : "/Users/jjmc/Desktop/8 and 8+2/DCO",   
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','OPC', 'Mature Oligodendrocyte', 'NonOligo','CC1+Olig2-'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : 'Cuprizone',

                'PercentCalcs' : [['NonOligo','DAPI'],['Mature Oligodendrocyte','OligoLineage'],['OPC','OligoLineage']],
                'PerilesionAnalysis' : True,

                'threshmethod' : 2,
                },
                {
                'name' : '27_Clemastine',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 2,

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","CC1","594_ch","Olig2"],
                'gammas' : [0.75,0.75,1,0.25],
                'RelativeIntensityThreshold' : [[1,5],[1.2,2],[1.2,2],[1.25,3]],

                # Path to folder containing images to be analyzed
                'Path' : "/Volumes/LABDATA/People/James/Remyelination Expt (Drugz)/PI88_Clemastine DCO_KSO",               
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','OPC', 'Mature Oligodendrocyte', 'NonOligo','CC1+Olig2-'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : 'KSO_DCOLesion',

                'PercentCalcs' : [['NonOligo','DAPI'],['Mature Oligodendrocyte','OligoLineage'],['OPC','OligoLineage']],

                'PerilesionAnalysis' : True,

                'threshmethod' : 2,
            },
            {
                'name' : '28_pTrip-Ef1a-Noggin-p2A-H2B-mCherry Titration',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 140,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 3.0769,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 0,

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","Phase","488-blank","H2B-mCherry"],
                'gammas' : [0.75,1,0.75,0.75],
                'RelativeIntensityThreshold' : [[1,5],[200,200],[1.2,5],[1.2,5]],

                # Path to folder containing images to be analyzed
                'Path' : "/Volumes/LABDATA/People/James/Transplant Expt/pTrip-Ef1a-Noggin-p2A-H2B-mCherry Titration",
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'Alive', 'Dead','mCherry Tagged'],

                # Do you want to use the keras models (slow)
                'useKeras' : False,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : "Plates",

                'PercentCalcs' : [['Alive','DAPI'],['Dead','DAPI'],['mCherry Tagged','Alive']],

                'PerilesionAnalysis' : False,

                'threshmethod' : 1,

            },            
            {
                'name' : '29_AxonalLossCalculations',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 2,

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","MBP","NF"],
                'gammas' : [0.75,0.75,0.75],
                'RelativeIntensityThreshold' : [[1,5],[1.2,5],[1.2,5]],

                # Path to folder containing images to be analyzed
                'Path' : "/Users/jjmc/Desktop/Axon MBP quantification",
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI'],

                # Do you want to use the keras models (slow)
                'useKeras' : False,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : "KSO_DCOLesion",

                'PercentCalcs' : [],

                'PerilesionAnalysis' : True,

                'threshmethod' : 1,

                'MFIPercAreaAnalysis' : True,

            },
            {
                'name' : '30_pTrip-Ef1a-Noggin-p2A-H2B-mCherry Titration',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 0,

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","Phase","O4_GFAPCh","H2B-mCherry"],
                'gammas' : [0.75,1,0.75,0.75],
                'RelativeIntensityThreshold' : [[1,5],[200,200],[2,5],[2,5]],

                # Path to folder containing images to be analyzed
                'Path' : "/Volumes/LABDATA/People/James/Transplant Expt/noggin virus validation/GFAP",
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI','mCherry Tagged', 'O4_GFAP'],

                # Do you want to use the keras models (slow)
                'useKeras' : False,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : "Plates",

                'PercentCalcs' : [['mCherry Tagged','DAPI'],['O4_GFAP','DAPI'],['O4_GFAP','mCherry Tagged']],

                'PerilesionAnalysis' : False,

                'threshmethod' : 1,

                'MFIPercAreaAnalysis' : False,

            },
                {
                'name' : '31_pTrip-Ef1a-Noggin-p2A-H2B-mCherry BMP Dose Response',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 1,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 1,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 2,
                'ROITitles' : [''],

                # Name each channel present (must be consistent for all images)
                'channels' : ["Phase","DAPI_ch","O4_GFAPCh","H2B-mCherry"],
                'gammas' : [0.75,0.75,0.75,0.75],
                'RelativeIntensityThreshold' : [[200,200],[1,5],[2,5],[1.05,5]],

                # Path to folder containing images to be analyzed
                'Path' : "/Users/jjmc/Library/CloudStorage/Box-Box/NewLabData/People/Greg/TIF images from 01242023/Test",
                #'Path' : "/Users/jjmc/Library/CloudStorage/Box-Box/NewLabData/People/Greg/20230201",
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI','mCherry Tagged', 'O4_GFAP'],

                # Do you want to use the keras models (slow)
                'useKeras' : False,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : False,

                # DataOrganizer type
                'DataOrganizer' : "Plates",

                'PercentCalcs' : [['mCherry Tagged','DAPI'],['O4_GFAP','DAPI'],['O4_GFAP','mCherry Tagged']],

                'PerilesionAnalysis' : False,

                'threshmethod' : 1,

                'MFIPercAreaAnalysis' : False,

            },                
            {
                'name' : '32_STIM2 KO EDU-OLIG2',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 2,
                'ROITitles' : ['Dorsal', 'Ventral'],

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","EDU","Olig2"],
                'gammas' : [1.5,1,1],
                'RelativeIntensityThreshold' : [[1.5,5],[1.7,5],[1.6,5]],

                # Path to folder containing images to be analyzed
                #'Path' : "Y:\\People\\Farah\\STIM 2 (KO & wild type) EDU-Olig2 staining\\Combined",
                'Path' : "/Users/jjmc/Library/CloudStorage/Box-Box/NewLabData/People/Farah/STIM 2 (KO & wild type) EDU-Olig2 staining/Combined",
                #'Path' : "/Volumes/LABDATA/People/Farah/STIM 2 (KO & wild type) EDU-Olig2 staining/Combined",
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI','EDU+', 'EDU+Olig2-','OligoLineage', 'EDU+Olig2+'],

                # Do you want to use the keras models (slow)
                'useKeras' : False,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : "Farah",

                'PercentCalcs' : [['EDU+Olig2+','OligoLineage'],['EDU+','DAPI']],

                'PerilesionAnalysis' : False,

                'threshmethod' : 2,

                'MFIPercAreaAnalysis' : False,

            },
            {
                'name' : '33_KSOClemAndSpatial',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 3,
                'ROITitles' : ['Core', 'Lesion', 'PLWM'],

                # Name each channel present, in order (must be consistent for all images)

                'channels' : ["DAPI_ch","Ki67","Sox2","Olig2"],
                'gammas' : [0.75,0.75,0.75,0.75],

                'RelativeIntensityThreshold' : [[1,5],[2.5,5],[1.8,5],[1.5,3]],
                

                # Path to folder containing images to be analyzed
                #'Path' : "/Volumes/LABDATA/People/James/Remyelination Expt (Drugz)/KSO",
                'Path' : "/Users/jjmc/Library/CloudStorage/Box-Box/NewLabData/People/James/Remyelination Expt (Drugz)/KSO",
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','ActiveOPC', 'ProlifOPC', 'NonOligo', 'Sox2Astro','ProlifNonOligo', 'Activated-ProliferativeOPCs'],

                # Do you want to use the CC1 keras models (slow)
                'useKeras' : False,

                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : False,

                # DataOrganizer type
                'DataOrganizer' : 'KSO_DCOLesion',

                'PercentCalcs' : [['NonOligo','DAPI'],['ProlifNonOligo','NonOligo'],['ActiveOPC','OligoLineage'],['ProlifOPC','OligoLineage'],['Activated-ProliferativeOPCs','ActiveOPC']],
                
                'PerilesionAnalysis' : False,

                'threshmethod' : 2,

                'MFIPercAreaAnalysis' : False,
            }, 
            {
                'name' : '34_AxonalLossCalculationsClemAndSpatial',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 3,
                'ROITitles' : ['Core', 'Lesion', 'PLWM'],

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch",'NF'],
                'gammas' : [0.75,0.75],
                'RelativeIntensityThreshold' : [[1,5],[1.2,5]],

                # Path to folder containing images to be analyzed
                'Path' : "/Users/jjmc/Library/CloudStorage/Box-Box/NewLabData/People/James/Remyelination Expt (Drugz)/NF",
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI'],

                # Do you want to use the keras models (slow)
                'useKeras' : False,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : "KSO_DCOLesion",

                'PercentCalcs' : [],

                'PerilesionAnalysis' : False,

                'threshmethod' : 1,

                'MFIPercAreaAnalysis' : True,

            },
            {
                'name' : '35_NAWMAxonalLossCalculationsClemAndSpatial',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 1,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 1,
                'ROITitles' : ['NAWM'],

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch",'NF'],
                'gammas' : [0.75,0.75],
                'RelativeIntensityThreshold' : [[1,5],[1.2,5]],

                # Path to folder containing images to be analyzed
                'Path' : "/Users/jjmc/Library/CloudStorage/Box-Box/NewLabData/People/James/Remyelination Expt (Drugz)/NF/NAWM",
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI'],

                # Do you want to use the keras models (slow)
                'useKeras' : False,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : "KSO_DCOLesion",

                'PercentCalcs' : [],

                'PerilesionAnalysis' : False,

                'threshmethod' : 1,

                'MFIPercAreaAnalysis' : True,

            },

            {
                'name' : '36_NAWMDGIClemAndSpatial',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 1,
                #'ROITitles' : ['Core','Lesion', 'PLWM'],
                'ROITitles' : ['NAWM'],


                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch",'IBA1','GFAP'],
                'gammas' : [0.75, 0.75, 0.75],
                'RelativeIntensityThreshold' : [[1,5],[1.2,5],[1.2,5]],

                # Path to folder containing images to be analyzed
                'Path' : "/Users/jjmc/Library/CloudStorage/Box-Box/NewLabData/People/James/Remyelination Expt (Drugz)/DGI/NAWM",
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI'],

                # Do you want to use the keras models (slow)
                'useKeras' : False,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : "KSO_DCOLesion",

                'PercentCalcs' : [],

                'PerilesionAnalysis' : False,

                'threshmethod' : 1,

                'MFIPercAreaAnalysis' : True,

            },

            {
                'name' : '37_DGIClemAndSpatial',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 3,
                'ROITitles' : ['Core','Lesion', 'PLWM'],
                #'ROITitles' : ['NAWM'],


                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch",'IBA1','GFAP'],
                'gammas' : [0.75,0.75, 0.75],
                'RelativeIntensityThreshold' : [[1,5],[1.2,5],[1.2,5]],

                # Path to folder containing images to be analyzed
                'Path' : "/Users/jjmc/Library/CloudStorage/Box-Box/NewLabData/People/James/Remyelination Expt (Drugz)/DGI",
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI'],

                # Do you want to use the keras models (slow)
                'useKeras' : False,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : "KSO_DCOLesion",

                'PercentCalcs' : [],

                'PerilesionAnalysis' : False,

                'threshmethod' : 1,

                'MFIPercAreaAnalysis' : True,

            },
            {
                'name' : '38_DCOClemAndSpatialOLD',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 3,
                'ROITitles' : ['Core','Lesion', 'PLWM'],
                #'ROITitles' : ['NAWM'],


                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch",'CC1','Olig2'],
                'gammas' : [0.75,0.75, 0.75],
                'RelativeIntensityThreshold' : [[1,5],[1.2,5],[2,5]],

                # Path to folder containing images to be analyzed
                'Path' : "/Volumes/LABDATA/People/James/Remyelination Expt (Drugz)/DCO/Oldimages",
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','OPC', 'Mature Oligodendrocyte', 'NonOligo','CC1+Olig2-'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : "KSO_DCOLesion",

                'PercentCalcs' : [['NonOligo','DAPI'],['Mature Oligodendrocyte','OligoLineage'],['OPC','OligoLineage']],

                'PerilesionAnalysis' : False,

                'threshmethod' : 1,

                'MFIPercAreaAnalysis' : False,

            },
            {
                'name' : '39_DCOClemAndSpatialNEW',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 3,
                'ROITitles' : ['Core','Lesion', 'PLWM'],
                #'ROITitles' : ['NAWM'],


                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch",'CC1','Olig2'],
                'gammas' : [1.1,0.75, 0.75],
                'RelativeIntensityThreshold' : [[1,5],[1.2,5],[1.8,3]],

                # Path to folder containing images to be analyzed
                'Path' : "/Volumes/LABDATA/People/James/Remyelination Expt (Drugz)/DCO",
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','OPC', 'Mature Oligodendrocyte', 'NonOligo','CC1+Olig2-'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : "KSO_DCOLesion",

                'PercentCalcs' : [['NonOligo','DAPI'],['Mature Oligodendrocyte','OligoLineage'],['OPC','OligoLineage']],

                'PerilesionAnalysis' : False,

                'threshmethod' : 1,

                'MFIPercAreaAnalysis' : False,

            },
            {
                'name' : '40_DCOClemAndSpatialNEW_Refined',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 3,
                'ROITitles' : ['Core','Lesion', 'PLWM'],
                #'ROITitles' : ['NAWM'],


                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch",'CC1','Olig2'],
                'gammas' : [1.1,0.75, 0.75],
                'RelativeIntensityThreshold' : [[1,5],[1.2,5],[1.8,3]],

                # Path to folder containing images to be analyzed
                'Path' : "/Volumes/LABDATA/People/James/Remyelination Expt (Drugz)/DCO",
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','OPC', 'Mature Oligodendrocyte', 'NonOligo','CC1+Olig2-'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : "KSO_DCOLesion",

                'PercentCalcs' : [['NonOligo','DAPI'],['Mature Oligodendrocyte','OligoLineage'],['OPC','OligoLineage']],

                'PerilesionAnalysis' : False,

                'threshmethod' : 2,

                'MFIPercAreaAnalysis' : False,

            },
            {
                'name' : '41_DCOClemAndSpatialNEW_Conservative',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 3,
                'ROITitles' : ['Core','Lesion', 'PLWM'],
                #'ROITitles' : ['NAWM'],


                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch",'CC1','Olig2'],
                'gammas' : [1.1,1, 0.75],
                'RelativeIntensityThreshold' : [[1,5],[1.2,5],[1.8,3]],

                # Path to folder containing images to be analyzed
                'Path' : "/Volumes/LABDATA/People/James/Remyelination Expt (Drugz)/DCO",
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','OPC', 'Mature Oligodendrocyte', 'NonOligo','CC1+Olig2-'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : "KSO_DCOLesion",

                'PercentCalcs' : [['NonOligo','DAPI'],['Mature Oligodendrocyte','OligoLineage'],['OPC','OligoLineage']],

                'PerilesionAnalysis' : False,

                'threshmethod' : 2,

                'MFIPercAreaAnalysis' : False,

            },
            {
                'name' : '42_PlP1_Olig2_PDGFRa',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 3,
                'ROITitles' : ['Core','Lesion', 'PLWM'],
                #'ROITitles' : ['NAWM'],


                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch",'RS_PLP1','RS_Olig2','RS_PDGFRa'],
                'gammas' : [1.1,0.75, 0.5, 0.5],
                'RelativeIntensityThreshold' : [[1,5],[1.8,5],[1.5,5], [1.5,5]],

                # Path to folder containing images to be analyzed
                'Path' : "/Volumes/LABDATA/People/James/Remyelination Expt (Drugz)/RNAscope",
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'RS_Oligodendrocyte', 'RS_OPC', 'RS_Olig2Only', "RS_OL-OPCMixed", "RS_PDGFRaOnly"],

                # Do you want to use the keras models (slow)
                'useKeras' : False,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : "KSO_DCOLesion",

                'PercentCalcs' : [['NonOligo','DAPI'],['Mature Oligodendrocyte','OligoLineage'],['OPC','OligoLineage'], ['RS_PDGFRaOnly',"RS_OPC"]],

                'PerilesionAnalysis' : False,

                'threshmethod' : 2,

                'MFIPercAreaAnalysis' : False,

            },
            {
                'name' : '43_NAWMPlP1_Olig2_PDGFRa', #Added "NAWM" to the title after the analysis

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 1,
                'ROITitles' : ['NAWM'],


                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch",'RS_PLP1','RS_Olig2','RS_PDGFRa'],
                'gammas' : [1.1,0.75, 0.5, 0.5],
                'RelativeIntensityThreshold' : [[1,5],[1.8,5],[1.5,5], [1.5,5]],

                # Path to folder containing images to be analyzed
                'Path' : "Y:\\People\\James\\Remyelination Expt (Drugz)\\RNAscope\\NAWM",
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'RS_Oligodendrocyte', 'RS_OPC', 'RS_Olig2Only', "RS_OL-OPCMixed"],

                # Do you want to use the keras models (slow)
                'useKeras' : False,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : "KSO_DCOLesion",

                'PercentCalcs' : [['NonOligo','DAPI'],['Mature Oligodendrocyte','OligoLineage'],['OPC','OligoLineage']],

                'PerilesionAnalysis' : False,

                'threshmethod' : 2,

                'MFIPercAreaAnalysis' : False,

            },
            {
                'name' : '44_PDGFRa_p21_Olig2',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 3,
                'ROITitles' : ['Core',"Lesion","PLWM"],


                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch",'RS_PDGFRa','RS_p21','RS_Olig2'],
                'gammas' : [1.1,0.75, 0.5, 0.5],
                'RelativeIntensityThreshold' : [[1,5],[1.8,5],[1.5,5], [1.5,5]],

                # Path to folder containing images to be analyzed
                #'Path' : "Y:\\People\\James\\Remyelination Expt (Drugz)\\RNAscope\\p21",
                'Path' : "/Volumes/LABDATA/People/James/Remyelination Expt (Drugz)/RNAscope/p21",
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'RS_OPC', "RS_p21-Olig2", "RS_p21-OPC"],

                # Do you want to use the keras models (slow)
                'useKeras' : False,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : "KSO_DCOLesion",

                'PercentCalcs' : [['NonOligo','DAPI']],

                'PerilesionAnalysis' : False,

                'threshmethod' : 2,

                'MFIPercAreaAnalysis' : False,

            },

                {
                'name' : '45_NAWM_PDGFRa_p21_Olig2',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 1,
                'ROITitles' : ['NAWM'],


                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch",'RS_PDGFRa','RS_p21','RS_Olig2'],
                'gammas' : [1.1,0.75, 0.5, 0.5],
                'RelativeIntensityThreshold' : [[1,5],[1.8,5],[1.5,5], [1.5,5]],

                # Path to folder containing images to be analyzed
                #'Path' : "Y:\\People\\James\\Remyelination Expt (Drugz)\\RNAscope\\p21",
                'Path' : "/Volumes/LABDATA/People/James/Remyelination Expt (Drugz)/RNAscope/p21/NAWM",
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'RS_OPC', "RS_p21-Olig2", "RS_p21-OPC"],

                # Do you want to use the keras models (slow)
                'useKeras' : False,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : "KSO_DCOLesion",

                'PercentCalcs' : [['NonOligo','DAPI']],

                'PerilesionAnalysis' : False,

                'threshmethod' : 2,

                'MFIPercAreaAnalysis' : False,

            },
            {
                'name' : '46_DCOLarge&SmallCoreExclusion',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 3,
                'ROITitles' : ['Core',"Lesion","PLWM"],

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","CC1","594_ch","Olig2"],
                'gammas' : [0.75,0.75,1,0.25],
                'RelativeIntensityThreshold' : [[1,5],[1.2,2],[1.2,2],[2,3]],
                #'RelativeIntensityThreshold' : [[1,5],[1.2,2],[1.2,2],[1.7,3]],

                # Path to folder containing images to be analyzed
                #'Path' : "Y:\\People\\James\\Large vs Small Lesion Expt\\__Cell Dynamics\\DCO Large&Small Lesions\\Lesion",
                'Path' : '/Volumes/LABDATA/People/James/Large vs Small Lesion Expt/__Cell Dynamics/DCO Large&Small Lesions/Lesion/Clemastine paper Core exclusion',
               
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','OPC', 'Mature Oligodendrocyte', 'NonOligo','CC1+Olig2-'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : 'KSO_DCOLesion',

                'PercentCalcs' : [['NonOligo','DAPI'],['Mature Oligodendrocyte','OligoLineage'],['OPC','OligoLineage']],
                
                'PerilesionAnalysis' : False,

                'threshmethod' : 2,

                'MFIPercAreaAnalysis' : False,
                },
                {
                'name' : '47_KSOLarge&SmallCombined',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 3,
                'ROITitles' : ['Core',"Lesion","PLWM"],

                # Name each channel present, in order (must be consistent for all images)

                'channels' : ["DAPI_ch","Ki67","Sox2","Olig2"],
                'gammas' : [0.75,0.25,0.25,0.25],
                'RelativeIntensityThreshold' : [[1,5],[3,5],[3,5],[2,3]],
                

                # Path to folder containing images to be analyzed
                'Path' : "/Volumes/LABDATA/People/James/Large vs Small Lesion Expt/__Cell Dynamics/KSO Large&Small Lesions/Core Exclusion for clemastine paper",
                #'Path' : '/Volumes/labdata/People/James/Large vs Small Lesion Expt/__Cell Dynamics/KSO Large&Small Lesions',    
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','ActiveOPC', 'ProlifOPC', 'NonOligo', 'Sox2Astro','ProlifNonOligo', 'Activated-ProliferativeOPCs'],

                # Do you want to use the CC1 keras models (slow)
                'useKeras' : False,

                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : 'KSO_DCOLesion',

                'PercentCalcs' : [['NonOligo','DAPI'],['ProlifNonOligo','NonOligo'],['ActiveOPC','OligoLineage'],['ProlifOPC','OligoLineage'],['Activated-ProliferativeOPCs','ActiveOPC']],
                
                'PerilesionAnalysis' : False,

                'threshmethod' : 2,

                'MFIPercAreaAnalysis' : False,
            },             
            {
                'name' : '48_Sox2_h2ax_Olig2',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 3,
                'ROITitles' : ['Core',"Lesion","PLWM"],


                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch",'Sox2','yh2ax','Olig2'],
                'gammas' : [0.75,0.65, 0.5, 0.5],
                'RelativeIntensityThreshold' : [[1,5],[1.8,5],[999,999], [1.2,5]],

                # Path to folder containing images to be analyzed
                #'Path' : "Y:\\People\\James\\Remyelination Expt (Drugz)\\Sox2-h2ax-olig2",
                'Path' : "/Volumes/LABDATA/People/James/Remyelination Expt (Drugz)/Sox2-h2ax-olig2",
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage', 'ActiveOPC', "yh2ax-ActiveOPC", "yh2ax-Olig2", "yh2ax-Olig2Nonactive", "yh2ax-NonOlig2"],

                # Do you want to use the keras models (slow)
                'useKeras' : False,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : "KSO_DCOLesion",

                'PercentCalcs' : [['NonOligo','DAPI']],

                'PerilesionAnalysis' : False,

                'threshmethod' : 2,

                'MFIPercAreaAnalysis' : False,

            },
            {
                'name' : '49_Sox2_h2ax_Olig2NAWM',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 1,
                'ROITitles' : ['NAWM'],


                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch",'Sox2','yh2ax','Olig2'],
                'gammas' : [0.75,0.65, 0.5, 0.5],
                'RelativeIntensityThreshold' : [[1,5],[1.8,5],[999,999], [1.2,5]],

                # Path to folder containing images to be analyzed
                #'Path' : "Y:\\People\\James\\Remyelination Expt (Drugz)\\Sox2-h2ax-olig2",
                'Path' : "/Volumes/LABDATA/People/James/Remyelination Expt (Drugz)/Sox2-h2ax-olig2/NAWM",
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage', 'ActiveOPC', "yh2ax-ActiveOPC", "yh2ax-Olig2", "yh2ax-Olig2Nonactive", "yh2ax-NonOlig2"],

                # Do you want to use the keras models (slow)
                'useKeras' : False,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : "KSO_DCOLesion",

                'PercentCalcs' : [['NonOligo','DAPI']],

                'PerilesionAnalysis' : False,

                'threshmethod' : 2,

                'MFIPercAreaAnalysis' : False,

            },
            {
                'name' : '50_Sox2_Ki67_Pdgfra',

                # Which channel to use for drawing ROIs, base 0. So channel 1 is 0, channel 2 is 1 etc.
                'ROI_Draw_Channel' : 0,

                # Which channel to use for identifying nuclei, base 0
                'Nuclei_Identification_Channel' : 0,

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 3,
                'ROITitles' : ['Core',"Lesion","PLWM"],

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch",'RS_Sox2','RS_PDGFRa','RS_KI67'],
                'gammas' : [0.75,0.5, 0.5, 0.5],
                'RelativeIntensityThreshold' : [[1,5],[1.8,5],[1.8,5],[999,999]],

                # Path to folder containing images to be analyzed
                #'Path' : "Y:\\People\\James\\Remyelination Expt (Drugz)\\Sox2-h2ax-olig2",
                'Path' : "/Volumes/LABDATA/People/James/Remyelination Expt (Drugz)/Sox2-Ki67-Pdgfra RNAscope",
                
                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'RS_ProlifOPC', 'RS_ActiveOPC'],

                # Do you want to use the keras models (slow)
                'useKeras' : False,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # if true, does not pull images during the ProcessRawResults
                'FastProcess' : True,

                # DataOrganizer type
                'DataOrganizer' : "KSO_DCOLesion",

                'PercentCalcs' : [],

                'PerilesionAnalysis' : False,

                'threshmethod' : 2,

                'MFIPercAreaAnalysis' : False,

            },

        ]



