


class Settings:
    """A class to store all settings."""

    def __init__(self):
        #Define rabbits numbers
        self.RabbitDescriptions = {
        '007dpl_5ul' : [7,[ '1', '2', '3', '5', '9', '16', '19']],
        '014dpl_5ul' : [14,[ '4', '6', '10', '21', '23']],
        '021dpl_5ul' : [21,[ '7', '8', '17', '20', '22']],
        '056dpl_5ul' : [56,['13', '27', '28', '29']],
        '180dpl_5ul' : [180,['43', '44', '45',]],

        '056dpl_5ul_Glut' : [56,['14']],
        '180dpl_5ul_Glut' : [180,['45']],

        '007dpl_1ul' : [7,['24', '25']],

        '007dpl_0.35ul' : [7,['26', '48','60']],
        '014dpl_0.35ul' : [14,['35', '51','54','59']],
        '021dpl_0.35ul' : [21,['34','50','53','56']],

        '014dpl_0.35ul&5ul' : [7,['61']],
        '014dpl_0.35ul&5ul' : [14,['57']],
        '021dpl_0.35ul&5ul' : [21,['52']],

        '021dpl_5ul_Clemastine' : [21,[ '31', '32', '33']],
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
                'RelativeIntensityThreshold' : [[1,5],[1.2,2],[1.2,2],[1.2,2]],

                # Path to folder containing images to be analyzed
                'Path' : "\\Users\\jjmc1\\Desktop\\Python\\AutoCount2.0\\LargeLesionDCO",

                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','OPC', 'Mature Oligodendrocyte', 'NonOligo','CC1+Olig2-'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                # DataOrganizer type
                'DataOrganizer' : 'KSO_DCOLesion',

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
                #Average scale for 4x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 1,

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","CC1","Blank","Olig2"],
                'gammas' : [0.75,0.75,1,0.75],

                # Path to folder containing images to be analyzed
                #'Path' : "C:\\Users\\jjmc1\\Desktop\\Control KSO DCO\\DCO",
                'Path' : "/Users/jjmc/Desktop/Control KSO DCO/DCO",

                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','OPC', 'CC1+', 'NonOligo', 'CC1+Olig2-'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,

                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,

                
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
                'ROINumber' : 1,

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
                'RelativeIntensityThreshold' : [[1,5],[3,5],[3,5],[4,5]],

                # Path to folder containing images to be analyzed
                'Path' : "Y:\\People\\Rich\\__Transplants\\_____Transplant Master Folder\\D\\IHC master folder\\PV-NES-NLS-Transplant1_MBP-hNA IHC images\\Tiff\\New images",
                #'Path' : "Y:\\People\\Rich\\Transplant_MBP-hNA\\Tiff",
                #'Path' : "C:\\Users\\jjmc1\\Desktop\\New folder",
                

                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'Human Cell','Myelinating Human Cell'],

                # Do you want to use the keras models (slow)
                'useKeras' : False,

                # Check files for uniformity? Good idea to do once
                'checkfiles' : True,

                # DataOrganizer type
                'DataOrganizer' : 'PVTransplants',
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
                'RelativeIntensityThreshold' : [[1,5],[3,5],[3,5],[1.2,2]],

                # Path to folder containing images to be analyzed
                'Path' : "Y:\\People\\James\\KSO Small+Treatment",

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
            },
        ]



