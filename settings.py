class Settings:
    """A class to store all settings."""

    def __init__(self):

        # Define folders for input of data
        self.folder_dicts = [
            {
                'name' : 'JCmac',

                # Define size of individual cell images (in pixels, defines both height and width, so a square)
                'cropsize' : 46,
            
                # Define the number of ROIs you want to draw
                'ROINumber' : 1,

                # Name each channel present (must be consistent for all images)
                'channels' : ["DAPI_ch","CC1","594_ch","Olig2"],

                # Path to folder containing images to be analyzed
                'Path' : "/Users/jjmc/Desktop/Working Folder/Normal and Cuprizone DCO/Images"
            },
        ]





