class Settings:
    """A class to store all settings."""

    def __init__(self):

        # Define folders for input of data
        self.folder_dicts = [
            {
                'name' : 'JCmac',

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
            },
            {
                'name' : 'LargeLesionDCO',

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
                'cell_types_to_analyze' : ['OPC', 'Oligo', 'NonOligo'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
            },
            {
                'name' : 'FMSize calculation JCWindows',

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
            },
            {
                'name' : 'FMSize 4x calculation JCmac',

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
            },
            {
                'name' : 'RoopaMouseWindow',

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
                'cell_types_to_analyze' : ['OPC', 'Oligo', 'NonOligo', 'CC1+Olig2-'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
            },
            {
                'name' : 'RoopaMouseMac',

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
                'cell_types_to_analyze' : ['OPC', 'Oligo', 'NonOligo', 'CC1+Olig2-'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
            },
            {
                'name' : 'SettingParametersDCO',

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
                'cell_types_to_analyze' : ['OPC', 'Oligo', 'NonOligo', 'CC1+Olig2-'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
            },
            {
                'name' : 'SettingParametersKSO',

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,

                #Change if using anything other then 10x
                #Average scale for 4x images, pixel/micron
                'scale' : 1.5385,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 1,

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","CC1","Olig2","Olig2"],

                # Path to folder containing images to be analyzed
                'Path' : "C:\\Users\\jjmc1\\Desktop\\Control KSO DCO\\DCO",

                # Cell types to analyze
                'cell_types_to_analyze' : ['OPC', 'Oligo', 'NonOligo', 'CC1+Olig2-'],

                # Do you want to use the keras models (slow)
                'useKeras' : True,
            },
        ]





