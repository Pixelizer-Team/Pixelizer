Using this repository you can pixelize your images into hexagon grid!

### Samples
Normal image

Hexagonal             | Square          |       Splited      
:-------------------------:|:-------------------------:|:-------------------------:
![Normal](samples/hex/light.jpg) | ![Normal](samples/sq/monroe.jpg)  |  ![Normal](samples/split/sprited.jpg) 
![R=5](samples/hex/hex_5.jpg) | ![R=30](samples/sq/monroe_30.jpg)  |  ![R=5](samples/split/split_2.jpg)
![R=15](samples/hex/hex_15.jpg) | ![R=20](samples/sq/monroe_20.jpg)  |  ![R=50](samples/split/split_7.jpg) | 
![R=30](samples/hex/hex_30.jpg) | ![R=10](samples/sq/monroe_10.jpg)  |  ![R=200](samples/split/split_23.jpg) | 

Pyramid                   |         Cubical         |   Double Cubical
:-------------------------:|:-------------------------:|:-------------------------:
  | ![Normal](samples/pyramid/wave.jpg) | ![Normal](samples/dcube/gogh.jpg)
 ![R=300](samples/pyramid/wave_30.jpg) | ![R=10](samples/cube/scream_5.jpg) | ![R=15](samples/dcube/gogh_15.jpg)
 ![R=1000](samples/pyramid/wave_50.jpg) | ![R=30](samples/cube/scream_10.jpg) | ![R=30](samples/dcube/gogh_30.jpg)
 ![R=4000](samples/pyramid/wave_80.jpg) | ![R=50](samples/cube/scream_30.jpg) | ![R=50](samples/dcube/gogh_50.jpg)
 
 
Blob                    |   Voronoi    |
:-------------------------:|:-------------------------:|
![Normal](samples/blob/gothic.jpg) | ![Normal](samples/vor/mona.jpg)
![R=5](samples/blob/gothic_5.jpg) | ![R=300](samples/vor/mona_300.jpg) 
![R=10](samples/blob/gothic_10.jpg) |  ![R=1000](samples/vor/mona_1000.jpg)
![R=20](samples/blob/gothic_20.jpg) | ![R=4000](samples/vor/mona_4000.jpg)

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
