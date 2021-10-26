


class Settings:
    """A class to store all settings."""

    def __init__(self):

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

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 2,

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","CC1","594_ch","Olig2"],

                # Path to folder containing images to be analyzed
                'Path' : "\\Users\\jjmc1\\Desktop\\Python\\AutoCount2.0\\LargeLesionDCO",

                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','OPC', 'Mature Oligodendrocyte', 'NonOligo','CC1+Olig2-'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
                
                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,
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

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 4x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 1,

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","CC1","Blank","Olig2"],

                # Path to folder containing images to be analyzed
                'Path' : "C:\\Users\\jjmc1\\Desktop\\Control KSO DCO\\DCO",

                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','OPC', 'Mature Oligodendrocyte', 'NonOligo', 'CC1+Olig2-'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,

                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,
            },
            {
                'name' : '7_SettingParametersKSO',

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 4x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 1,

                # Name each channel present, in order (must be consistent for all images)

                'channels' : ["DAPI_ch","Ki67","Sox2","Olig2"],

                # Path to folder containing images to be analyzed
                'Path' : "C:\\Users\\jjmc1\\Desktop\\Control KSO DCO\\KSO",

                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','ActiveOPC', 'ProlifOPC', 'NonOligo', 'Sox2Astro','ProlifNonOligo',],

                # Do you want to use the keras models (slow)
                'useKeras' : True,

                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,
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

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 10x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 2,

                # Name each channel present, in order (must be consistent for all images)

                'channels' : ["DAPI_ch","Ki67","Sox2","Olig2"],

                # Path to folder containing images to be analyzed
                'Path' : "C:\\Users\\jjmc1\\Desktop\\Python\\AutoCount2.0\\LargeLesionKSO",

                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'OligoLineage','ActiveOPC', 'ProlifOPC', 'NonOligo', 'Sox2Astro','ProlifNonOligo', 'Activated-ProliferativeOPCs'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,

                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,
            },
            {
                'name' : '10_Transplant Test',

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

                # Path to folder containing images to be analyzed
                #'Path' : "C:\\Users\\jjmc1\\Desktop\\Rich Transplants",
                'Path' : "Y:\\People\\Rich\\Transplant_MBP-hNA\\Tiff",

                # Cell types to analyze
                'cell_types_to_analyze' : ['DAPI', 'Human Cell','Myelinating Human Cell'],

                # Do you want to use the keras models (slow)
                'useKeras' : False,

                # Check files for uniformity? Good idea to do once
                'checkfiles' : False,
            },
        ]



