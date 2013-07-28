# python
import os

# django/tastypie/libs
from PIL import Image
from django.conf import settings
from django.test import TestCase

# snapable
from data.images import SnapImage

class SnapImageTestCase(TestCase):

    def setUp(self):
        """Setup the necessary objects for testing."""
        
        self.file_basename_1 = 'trashcat_1'
        self.file_basename_3 = 'trashcat_3'
        self.file_basename_6 = 'trashcat_6'
        self.file_basename_8 = 'trashcat_8'
        self.file_basename_lenna = 'lenna'

        # generate filename
        filename_1 = '%s.jpg' % self.file_basename_1
        filename_3 = '%s.jpg' % self.file_basename_3
        filename_6 = '%s.jpg' % self.file_basename_6
        filename_8 = '%s.jpg' % self.file_basename_8
        filename_normalized = 'trashcat_normalized.jpg'
        filename_logo = 'logo.png'
        filename_lenna = 'lenna.png'

        # get the filepath
        filepath_1 = os.path.join(settings.PROJECT_PATH, 'api', 'assets', filename_1)
        filepath_3 = os.path.join(settings.PROJECT_PATH, 'api', 'assets', filename_3)
        filepath_6 = os.path.join(settings.PROJECT_PATH, 'api', 'assets', filename_6)
        filepath_8 = os.path.join(settings.PROJECT_PATH, 'api', 'assets', filename_8)
        filepath_normalized = os.path.join(settings.PROJECT_PATH, 'api', 'assets', filename_normalized)
        filepath_logo = os.path.join(settings.PROJECT_PATH, 'api', 'assets', filename_logo)
        filepath_lenna = os.path.join(settings.PROJECT_PATH, 'api', 'assets', filename_lenna)

        # get the image
        self.img_1 = Image.open(filepath_1)
        self.img_3 = Image.open(filepath_3)
        self.img_6 = Image.open(filepath_6)
        self.img_8 = Image.open(filepath_8)
        self.img_normalized = Image.open(filepath_normalized)
        self.img_logo = Image.open(filepath_logo)
        self.img_lenna = Image.open(filepath_lenna)

    def test_image_exists(self):
        # make sure it's not null
        self.assertNotEqual(self.img_1, None)
        self.assertNotEqual(self.img_3, None)
        self.assertNotEqual(self.img_6, None)
        self.assertNotEqual(self.img_8, None)

        # make sure the orientation matches
        self.assertEqual(self.img_1._getexif()[0x0112], 1)
        self.assertEqual(self.img_3._getexif()[0x0112], 3)
        self.assertEqual(self.img_6._getexif()[0x0112], 6)
        self.assertEqual(self.img_8._getexif()[0x0112], 8)

    def test_snapimage(self):
        snapimg_1 = SnapImage(image=self.img_1)
        snapimg_3 = SnapImage(image=self.img_3)
        snapimg_6 = SnapImage(image=self.img_6)
        snapimg_8 = SnapImage(image=self.img_8)

        # make sure it's not null
        self.assertNotEqual(snapimg_1, None)
        self.assertNotEqual(snapimg_1.img, None)
        self.assertNotEqual(snapimg_3, None)
        self.assertNotEqual(snapimg_3.img, None)
        self.assertNotEqual(snapimg_6, None)
        self.assertNotEqual(snapimg_6.img, None)
        self.assertNotEqual(snapimg_8, None)
        self.assertNotEqual(snapimg_8.img, None)

        # assert they are the same
        self.assertEqual(snapimg_1.img, self.img_1)
        self.assertEqual(snapimg_1.exif, dict(self.img_1._getexif().items()))
        self.assertEqual(snapimg_1.exif[0x0112], 1)
        self.assertEqual(snapimg_3.img, self.img_3)
        self.assertEqual(snapimg_3.exif, dict(self.img_3._getexif().items()))
        self.assertEqual(snapimg_3.exif[0x0112], 3)
        self.assertEqual(snapimg_6.img, self.img_6)
        self.assertEqual(snapimg_6.exif, dict(self.img_6._getexif().items()))
        self.assertEqual(snapimg_6.exif[0x0112], 6)
        self.assertEqual(snapimg_8.img, self.img_8)
        self.assertEqual(snapimg_8.exif, dict(self.img_8._getexif().items()))
        self.assertEqual(snapimg_8.exif[0x0112], 8)
    
    def test_snapimage_normalized(self):
        snapimg_1 = SnapImage(image=self.img_1)
        snapimg_3 = SnapImage(image=self.img_3)
        snapimg_6 = SnapImage(image=self.img_6)
        snapimg_8 = SnapImage(image=self.img_8)
        snapimg_normalized = SnapImage(image=self.img_normalized)

        # make sure it's in the correct position
        self.assertEqual(snapimg_1.exif[0x0112], 1)
        self.assertEqual(snapimg_3.exif[0x0112], 3)
        self.assertEqual(snapimg_6.exif[0x0112], 6)
        self.assertEqual(snapimg_8.exif[0x0112], 8)

        # apply rotation
        snapimg_1.rotate_upright()
        snapimg_3.rotate_upright()
        snapimg_6.rotate_upright()
        snapimg_8.rotate_upright()

        # check to make sure exif is changed
        self.assertFalse(0x0112 in snapimg_3.exif)
        self.assertFalse(0x0112 in snapimg_6.exif)
        self.assertFalse(0x0112 in snapimg_8.exif)

        # save copy
        filepath_1 = os.path.join(settings.PROJECT_PATH, 'api', 'assets', '%s_test.jpg' % self.file_basename_1)
        filepath_3 = os.path.join(settings.PROJECT_PATH, 'api', 'assets', '%s_test.jpg' % self.file_basename_3)
        filepath_6 = os.path.join(settings.PROJECT_PATH, 'api', 'assets', '%s_test.jpg' % self.file_basename_6)
        filepath_8 = os.path.join(settings.PROJECT_PATH, 'api', 'assets', '%s_test.jpg' % self.file_basename_8)
        snapimg_1.img.save(filepath_1, 'JPEG')
        snapimg_3.img.save(filepath_3, 'JPEG')
        snapimg_6.img.save(filepath_6, 'JPEG')
        snapimg_8.img.save(filepath_8, 'JPEG')

        # open the test file
        snapimg_1_test = SnapImage(image=Image.open(filepath_1))
        snapimg_3_test = SnapImage(image=Image.open(filepath_3))
        snapimg_6_test = SnapImage(image=Image.open(filepath_6))
        snapimg_8_test = SnapImage(image=Image.open(filepath_8))

        # make sure the orientation matches or is null
        if 0x0112 in snapimg_1_test.exif and 0x0112 in snapimg_normalized.exif:
            self.assertEqual(snapimg_1_test.exif[0x0112], snapimg_normalized.exif[0x0112])
        if 0x0112 in snapimg_3_test.exif and 0x0112 in snapimg_normalized.exif:
            self.assertEqual(snapimg_3_test.exif[0x0112], snapimg_normalized.exif[0x0112])
        if 0x0112 in snapimg_6_test.exif and 0x0112 in snapimg_normalized.exif:
            self.assertEqual(snapimg_6_test.exif[0x0112], snapimg_normalized.exif[0x0112])
        if 0x0112 in snapimg_8_test.exif and 0x0112 in snapimg_normalized.exif:
            self.assertEqual(snapimg_8_test.exif[0x0112], snapimg_normalized.exif[0x0112])

        # make sure the dimensions match
        self.assertEqual(snapimg_1.size, snapimg_1_test.size)
        self.assertEqual(snapimg_3.size, snapimg_3_test.size)
        self.assertEqual(snapimg_6.size, snapimg_6_test.size)
        self.assertEqual(snapimg_8.size, snapimg_8_test.size)

    def test_image_crop(self):
        snapimg_1 = SnapImage(image=self.img_1)
        snapimg_3 = SnapImage(image=self.img_3)
        snapimg_6 = SnapImage(image=self.img_6)
        snapimg_8 = SnapImage(image=self.img_8)

        #The crop rectangle, as a (left, upper, right, lower)-tuple.
        snapimg_1.crop_square()
        snapimg_3.crop_square()
        snapimg_6.crop_square()
        snapimg_8.crop_square()

        filepath_1 = os.path.join(settings.PROJECT_PATH, 'api', 'assets', '%s_test_crop.jpg' % self.file_basename_1)
        filepath_3 = os.path.join(settings.PROJECT_PATH, 'api', 'assets', '%s_test_crop.jpg' % self.file_basename_3)
        filepath_6 = os.path.join(settings.PROJECT_PATH, 'api', 'assets', '%s_test_crop.jpg' % self.file_basename_6)
        filepath_8 = os.path.join(settings.PROJECT_PATH, 'api', 'assets', '%s_test_crop.jpg' % self.file_basename_8)
        snapimg_1.img.save(filepath_1, 'JPEG')
        snapimg_3.img.save(filepath_3, 'JPEG')
        snapimg_6.img.save(filepath_6, 'JPEG')
        snapimg_8.img.save(filepath_8, 'JPEG')

    def test_image_watermark(self):
        snapimg_lenna = SnapImage(image=self.img_lenna)

        # add watermark
        snapimg_lenna.watermark(self.img_logo, 0.9)

        # save image
        filepath_lenna = os.path.join(settings.PROJECT_PATH, 'api', 'assets', '%s_test_watermark.jpg' % self.file_basename_lenna)
        snapimg_lenna.img.save(filepath_lenna, 'JPEG')
