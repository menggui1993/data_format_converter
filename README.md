# data_format_converter
Deep learning dataset format converter. Convert your dataset in coco, voc, yolo format to other formats.

## YOLO
Data structure of yolo format:

```
--classes.txt
--train
  |--images
     |--001.jpg
     |--002.jpg
  |--labels
     |--001.txt
     |--002.txt
--val
  |--images
     |--101.jpg
     |--102.jpg
  |--labels
     |--101.txt
     |--102.txt
```

* **classes.txt** contains names of classes. One class name per line,
```
person
cat
dog
```
* **images** folder contain images
* **labels** folder contain labels. Label file and image file should have the same filename except extension. Labels are storing in the following format:
 
```
class_idx center_x center_y width height
```

One object per line. **center_x**, **center_y**, **width**, **height** are values in [0, 1]. Absolute values divided by the image width and height.

## Pascal Voc
Data structure of voc format:

```
--ImageSets
  |--Main
     |--train.txt
     |--val.txt
--JPEGImages
  |--train
     |--001.jpg
     |--002.jpg
  |--val
     |--101.jpg
     |--102.jpg
--Annotations
  |--train
     |--001.xml
     |--002.xml
  |--val
     |--101.xml
     |--102.xml
```

* **train.txt** and **val.txt** contain the filenames of train and val split, like this:
```
001
002
```
* **JPEGImages** contains all the image files.
* **Annotations** contains all the annotation files. XML file sample:
```xml
<annotation>
    <filename>001.jpg</filename>
    <size>
        <width>1920</width>
        <height>1080</height>
        <depth>3</depth>
    </size>
    <object>
        <name>person</name>
        <bndbox>
            <xmin>100</xmin>
            <ymin>100</ymin>
            <xmax>200</xmax>
            <ymax>500</ymax>
        </bndbox>
    </object>
</annotation>
```

## COCO
Data structure of coco format:

```
--images
  |--001.jpg
  |--002.jpg
--annotations
  |--train.json
  |--val.json
```
* **images** folder contains all the image files.
* **annotations** folder contains annotation files. Sample json file:

```json
{
    "images": [{"file_name": "001.jpg", "id": 1, "width": 1920, "height": 1080}], 
    "annotations": [{"image_id": 1, "id": 1, "category_id": 1, "bbox": [100, 100, 100, 400]}], 
    "categories": [{"name": "person", "id": 1}]
}
```
**bbox** values are [left, top, width, height].

