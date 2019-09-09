# https://github.com/ChiChou/glskybox

import shutil
import time
import sys

from os import path, mkdir

from PIL import Image

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class Projector(object):
    DIRECTIONS = {
        'top': (180, 180, 0),
        'bottom': (0, 180, 0),
        'front': (90, 180, 0),
        'left': (90, 180, 90),
        'back': (90, 180, 180),
        'right': (90, 180, 270),
    }

    def __init__(self, size, dest, verbose=False, overwrite=False):
        super(Projector, self).__init__()

        self.dest = dest
        self.x, self.y, self.z = 0, 0, 0
        self.w = self.h = size
        self.texture = None
        self.verbose = True
        self.overwrite = overwrite

        self.init_gl()

    def log(self, msg):
        if self.verbose:
            sys.stderr.write(str(msg) + '\n')


    def load_texture(self, f):
        start = time.time()
        im = Image.open(f)
        # im = im.resize((4096, 2048), Image.ANTIALIAS)

        w, h = im.size
        exif = im._getexif()
        buf = im.convert("RGB").tobytes("raw", "RGB")

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGB, w, h, 0,
            GL_RGB, GL_UNSIGNED_BYTE, buf
        )

        elapsed = time.time() - start
        self.log('[+] took %fs to load texture' % elapsed)

        self.texture = texture


    def run(self, src):
        if path.isdir(src):
            self.log('[+] target is a directory: ')
            self.log(' %s' % src)
            filelist = [path.join(src, filename) for filename in os.listdir(src) 
                if not filename.startswith('.')]

            [self.run(filename) for filename in filelist]

        elif path.isfile(src):
            self.log('[+] processing image: %s' % src)
            self.render(src)
            self.log('[+] done.')

        else:
            self.log('[!] invalid file: %s' % src)


    def render(self, filename):
        prefix, ext = path.splitext(path.basename(filename))

        if not path.isdir(self.dest):
            mkdir(self.dest)

        subdir = path.join(self.dest, prefix)
        if path.isdir(subdir):
            if self.overwrite:
                self.log('[!] overwriting %s' % subdir)
                shutil.rmtree(subdir)
            else:
                self.log('[!] %s exists, skipping' % subdir)
                return

        mkdir(subdir)

        self.load_texture(filename)
        start = time.time()

        directions = Projector.DIRECTIONS
        for name, vec in directions.items():
            buf = self.rotate(*vec)
            image = Image.frombytes(mode="RGB", size=(self.w, self.h), data=buf)
            image_name = path.join(subdir, "%s.jpg" % name)
            image.save(image_name)

        elapsed = time.time() - start
        self.log('[+] took %fs to render 6 images' % elapsed)

    def init_gl(self):

        glutInit()
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
        glutInitWindowSize(self.w, self.h)
        glutCreateWindow("glskybox renderer")
        glutHideWindow()

        glClearColor(0., 0., 0., 0.)
        glClearDepth(1.)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90, 1., .1, 100.)
        glMatrixMode(GL_MODELVIEW)


    def rotate(self, *args):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        glPushMatrix()

        glTranslatef(0., 0., 0.)
        glScalef(-1, 1, 1)
        
        x, y, z = args
        glRotatef(x, 1., 0., 0.)
        glRotatef(y, 0., 1., 0.)
        glRotatef(z, 0., 0., 1.)

        glEnable(GL_TEXTURE_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        Q = gluNewQuadric()
        gluQuadricNormals(Q, GL_SMOOTH)
        gluQuadricTexture(Q, GL_TRUE)
        glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
        glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
        gluSphere(Q, 2.0, 100, 100)

        glDisable(GL_TEXTURE_2D)
        
        buf = glReadPixels(0, 0, self.w, self.h, GL_RGB, GL_UNSIGNED_BYTE)
        
        glPopMatrix()
        
        return buf
        
if __name__ == '__main__':
    t = time.time()
    projector = Projector(1024, 'cubemap.jpg', True, True)
    projector.run('images/COR R1 S00 0 16.JPG')
    print(time.time() - t)