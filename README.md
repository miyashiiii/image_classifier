# image_classifier

<img src="asset/screenshot.png" width="320px" alt="screenshot">


## start command
```
python main.py <input dir> \
  -i <image dir> \
  -c <class names csv path> \
  -l <label csv path> \
  -o <output dir>
```  

example:  
```
python main.py sample \
 -i image \
 -c class_names.csv \
 -l label.csv \
 -o result
```

### usage
- Exec start command, then open the window and display first image. 
- You can classify the image by pressing number key.
- Labels are saved in a csv.

#### Keymap
```
  [number key]: classify
  [x]: remove label of current file
  [j]: next image
  [k]: previous image
  [p]: print label of all images
  [s]: save csv
  [q]: quit
```
