# -*- coding: utf-8 -*-
import envitro

##### RACKSPACE #####
CLOUDFILES_IMAGES_PREFIX = envitro.str('CLOUDFILES_IMAGES_PREFIX', 'dev_images_')
CLOUDFILES_DOWNLOAD_PREFIX = envitro.str('CLOUDFILES_DOWNLOAD_PREFIX', 'dev_downloads_')
CLOUDFILES_WATERMARK_PREFIX = envitro.str('CLOUDFILES_WATERMARK_PREFIX', 'dev_watermark')
CLOUDFILES_EVENTS_PER_CONTAINER = 10000
CLOUDFILES_PUBLIC_NETWORK = envitro.bool('CLOUDFILES_PUBLIC_NETWORK', True)