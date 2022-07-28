# Set to oldest date from Exif meta or file name in powershell

## Step 0 - install exiftool from below

[Installing ExifTool](https://exiftool.org/install.html#Windows)

## **Step 0.1**

Save the **[oldest_datetime_config](https://github.com/pratyushtewari/exif-scripts/blob/master/oldest_datetime_config)** in the home folder `C:\Users\YOURUSERNAME`

You can find these in a script here but I have found that running the commands in the pic folder I mentioned in the options below are much much faster than running these through python script [exif-scripts/setToOldestDate.py](setToOldestDate.py) For faster processing you can run these commands directly in powershell from the pic folder you are planning.

:safety_vest: Note that these scripts are recursive and will affect all the subfolders are well. 

Well … now — pick your options:

### Option 1 - In case you need to pick the date from the file name. This is pretty flexible and fuzzy parser but if you want it to be absolutely sure then you can remane the file to include yyyymmdd_hhmmss and remove all the other number before it (after is OK).

```jsx
exiftool "-FileModifyDate<filename" −overwrite_original -S -m -progress -ee -q -q ./
```

### Option 2 - set all the dates to the oldest date

```jsx
exiftool -overwrite_original "-FileModifyDate<OldestDateTime" "-ModifyDate<OldestDateTime" "-DateTimeOriginal<OldestDateTime" "-CreateDate<OldestDateTime" "-GPSDateTime<OldestDateTime" -S -m -progress -ee -q -q ./
```

### Option 3 - set the name of the file in PXL_yyyymmdd_hhmmss-[number-if-conflict].extension

```jsx
exiftool "-filename<OldestDateTime" -d PXL_%Y%m%d_%H%M%S%%-c.%%e -S -m -ee -progress -q -q ./
```

to push all the files in the current directory use

```jsx
adb push -a . /sdcard/DCIM/Camera/
```

  -a is to preserve the attributes.

## **:hourglass_flowing_sand: Refresh Android Media Store**
As a last step, you need to refresh the android media store database to let google photos know which new files to backup. Currently it does not always detect automatically so why wait for that. Install [Refresh MediaStore](https://play.google.com/store/apps/details?id=com.kotorimura.refreshmediastore) and run it after the adb push is complete from the phone. Then you can open Google Photos and see that the backup is starting.
