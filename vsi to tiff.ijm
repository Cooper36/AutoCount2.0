Dialog.create("Folder Chooser");
Dialog.addDirectory("Choose Images (.tif or .vsi)", "/jjmc1/Working/Crop Auto count/Test S2/");
Dialog.addDirectory("Choose Original Image Save Location", "/jjmc1/Working/Crop Auto count/Test D/");
Dialog.addString("Search Term:", "RB");
Dialog.show();

dir1 = Dialog.getString();
dir2 = Dialog.getString();
searchT = Dialog.getString();

//print(dir1);
//print(dir2);
//waitForUser("string");

olist = getFileList(dir1);



run("ROI Manager...");
roiManager("reset");
run("Clear Results");
close("Log");
close("Summary");
close("*");

Les_ID = 0;
for (b=0; b < olist.length; b++) {
	if (startsWith(olist[b], searchT)){
		print(olist.length);
		image_name = olist[b];
		file_name = dir1 + olist[b];
		slide_name = substring(olist[b], indexOf(olist[b], searchT), lengthOf(olist[b])-4);
		
		
		if (endsWith(olist[b], ".vsi")){
			run("Bio-Formats Importer", "open='file_name' color_mode=Composite rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT series_1");	
		}
		if (endsWith(olist[b], ".tif")){
			open(file_name);	
		}
		//print(list[i]);
		//Array.show(list);
		selectImage(1);
		run("Flip Vertically");
	
		//B&C + ROI
		run("Blue");
		run("Enhance Contrast", "saturated=0.35");
		run("Next Slice [>]");
		run("Green");
		run("Enhance Contrast", "saturated=0.35");
		run("Next Slice [>]");
		run("Cyan");
		run("Enhance Contrast", "saturated=0.35");
		run("Next Slice [>]");
		run("Red");
		run("Enhance Contrast", "saturated=0.35");
		Original = dir2 + slide_name ;
		saveAs("tiff", Original );
		close("*");
	}
}
