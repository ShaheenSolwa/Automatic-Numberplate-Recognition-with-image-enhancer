from alyn3 import Deskew
from alyn3 import SkewDetect


sd = SkewDetect(
    input_file = r'C:\Users\ssolwa001\PycharmProjects\PwC_ANPR\ocr_images\image.jpg',
    output_file=None,
    display_output='Yes',
    plot_hough=False
)

if_skewed = sd.determine_skew(sd.input_file)
print(if_skewed.keys())

d = Deskew(
	input_file = r'C:\Users\ssolwa001\PycharmProjects\PwC_ANPR\ocr_images\image.jpg',
	display_image='True',
	output_file='deskew.jpg',
	r_angle=if_skewed['Average Deviation from pi/4'],
    crop_image=False
)

d.run()