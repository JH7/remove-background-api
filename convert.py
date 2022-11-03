import numpy as np
import subprocess
import os

"""
Magick args taken from https://stackoverflow.com/a/57893768/1502477
"""
def remove_background_from_image_magick(image_content):
  CMD = os.environ.get('MAGICK_BIN')
  ARGS = ['-', '-background', 'white', '-gravity', 'center', '-extent', '702x702', '-fuzz', '2%', '-fill', 'none', '-draw', 'alpha 0,0 floodfill', '-channel', 'alpha', '-blur', '0x2', '-level', '50x100%', '+channel', '-shave', '1x1', 'png:-']
  
  proc = subprocess.Popen([CMD, *ARGS], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout, stderr = proc.communicate(input=image_content)

  stderr_string = stderr.decode('utf8').strip()
  if len(stderr_string) > 0:
    raise Exception(stderr_string)

  return stdout

"""
Taken from https://stackoverflow.com/a/63003020/1502477
"""
def remove_background_from_image(image_content):
  import cv2

  # load image
  img_arr = np.asarray(bytearray(image_content))
  img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

  # convert to graky
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  # threshold input image as mask
  mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)[1]

  # negate mask
  mask = 255 - mask

  # apply morphology to remove isolated extraneous noise
  # use borderconstant of black since foreground touches the edges
  kernel = np.ones((3,3), np.uint8)
  mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
  mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

  # anti-alias the mask -- blur then stretch
  # blur alpha channel
  mask = cv2.GaussianBlur(mask, (0,0), sigmaX=2, sigmaY=2, borderType = cv2.BORDER_DEFAULT)

  # linear stretch so that 127.5 goes to 0, but 255 stays 255
  mask = (2*(mask.astype(np.float32))-255.0).clip(0,255).astype(np.uint8)

  # put mask into alpha channel
  result = img.copy()
  result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
  result[:, :, 3] = mask

  # save resulting masked image
  return np.array(cv2.imencode('.png', result)[1]).tobytes()