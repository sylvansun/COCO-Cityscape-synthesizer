# coco-cityscape-synthesizer
Tools of extracting targets from the COCO dataset and synthesizing them into the Cityscapes dataset.

## Explanation of the scripts
These codes are developed based on the official PythonAPI provided by the COCO dataset. The basic functions are as follows:
```python
extractor.py # Extract polygon targets from the COCO dataset.
synthesizer.py # Synthesize polygon targets into the Cityscapes dataset.
```
You can run these scripts directly to get the results. Note that to run the synthesizer, you should first get the polygons extracted from the COCO dataset.

## Usage
You can either use the syntehsized images provided by our scripts, or implement your own dataset based on the polygon targets.
