from PIL import Image
from PIL.ExifTags import TAGS

class SnapImage(object):
    """
    A helper class that wraps the PIL Image class with useful Snapable
    functionality.
    """

    def __init__(self, image=None):
        # read the opject into the wrapper
        if image != None :
            self._img = image
        else:
            self._img = Image

        self._rotate_upright()

    def __getattr__(self, name):
        if name == 'img':
            return self._img
        elif name == 'exif':
            try:
                return dict(self._img._getexif().items())
            except:
                return {}
        else:
            return getattr(self._img, name)

    def resize(self, size):
        if self._rotate_upright():
            img = self._img.copy()
            try:
                # get the size param
                self._img = self._img.resize(size, Image.ANTIALIAS)
                return True
            except Exception as e:
                self._img = img
                return False

    def _rotate_upright(self):
        img = self._img.copy()
        try:
            exif = self.exif
            # rotate as required
            # 0x0112 = orientation
            if exif.has_key(0x0112) and exif[0x0112] == 3:
                self._img = self._img.rotate(180, expand=True)
            elif exif.has_key(0x0112) and exif[0x0112] == 6:
                self._img = self._img.rotate(270, expand=True)
            elif exif.has_key(0x0112) and exif[0x0112] == 8:
                self._img = self._img.rotate(90, expand=True)

            return True
        except Exception as e:
            self._img = img
            return False
