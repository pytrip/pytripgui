import logging

import pytrip as pt

logger = logging.getLogger(__name__)


class PatientModel:
    def __init__(self):
        self.name = "Patient"
        self.ctx = None
        self.vdx = None
        self.dcm = None

        self.plans = []

    def open_ctx(self, path):
        ctx = pt.CtxCube()
        ctx.read(path)
        self.ctx = ctx
        self.name = ctx.basename

    def open_vdx(self, path):
        vdx = pt.VdxCube(self.ctx)
        vdx.read(path)
        self.vdx = vdx
        if self.name != vdx.basename:
            logger.error("CTX | VDX patient name not match")

    def open_dicom(self, path):
        self.dcm = pt.dicomhelper.read_dicom_dir(path)

        if 'images' in self.dcm:
            self.ctx = pt.CtxCube()
            self.ctx.read_dicom(self.dcm)

        if 'rtss' in self.dcm:
            self.vdx = pt.VdxCube(self.ctx)
            self.vdx.read_dicom(self.dcm)

    def init_with_empty_cube(self, cube_params=None):
        if cube_params is None:
            cube_params = [255, 100, 100, 100, 1, 5]
        value, dimx, dimy, dimz, pixel_size, slice_distance = cube_params
        cube = pt.Cube()
        cube.create_empty_cube(value, dimx, dimy, dimz, pixel_size, slice_distance)
        self.ctx = pt.CtxCube(cube)
        self.ctx.basename = "arek"
        sphere_params = ["asia", [50, 50, 50], 5]

        self.vdx = pt.VdxCube(self.ctx)
        sphere = pt.vdx.create_sphere(self.ctx, *sphere_params)
        # sphere.color = [255, 0, 0]
        # print(sphere)
        # print('#{:02x}{:02x}{:02x}'.format(sphere.color[0], sphere.color[1], sphere.color[2]))
        self.vdx.add_voi(sphere)
        self.vdx.basename = "arek"
        # print(self.vdx.vois)
        self.name = "arek"

    def insert_empty_sphere(self, sphere_params):
        pass

