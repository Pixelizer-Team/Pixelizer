Using this repository you can pixelize your images into hexagon grid!

### Samples
Normal image

Hexagonal             | Square          |       Splited
:-------------------------:|:-------------------------:|:-------------------------:
![Normal](samples/sample.jpg) | ![Normal](samples/monroe.jpg)  |  ![Normal](samples/sprited.jpg)
![R=5](samples/pixelized_5.jpg) | ![R=30](samples/monroe_30.jpg)  |  ![R=5](samples/split_5.jpg)
![R=15](samples/pixelized_15.jpg) | ![R=20](samples/monroe_20.jpg)  |  ![R=50](samples/split_50.jpg)
![R=30](samples/pixelized_30.jpg) | ![R=10](samples/monroe_10.jpg)  |  ![R=100](samples/split_100.jpg)



### Requirements
Python 3+

You will need Numpy, Pillow, Shapely, and Tqdm to run this code.
You can install the requirements easily using 
```bash
pip install -r requirements.txt
```

### How to run
```bash
python main.py your_image.jpg output_image.jpg mode Radius
```
For example to generate the samples you can run
```bash
python3 main.py samples/sample.jpg samples/pixelized_5.jpg hex 5
```

Thanks to Stephan Hügel for hexgrid.py code.
