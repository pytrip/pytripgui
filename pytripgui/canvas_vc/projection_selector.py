import logging

logger = logging.getLogger(__name__)


class ProjectionSelector:
    def __init__(self):
        self._transversal_slice_no = 0
        self._sagittal_slice_no = 0
        self._coronal_slice_no = 0

        self._transversal_last_slice_no = 0
        self._sagittal_last_slice_no = 0
        self._coronal_last_slice_no = 0

        # "Transversal" (xy)
        # "Sagittal" (yz)
        # "Coronal"  (xz)
        self.plane = "Transversal"

    def next_slice(self):
        self.current_slice_no = (self.current_slice_no + 1) % self.last_slice_no

    def prev_slice(self):
        self.current_slice_no = (self.current_slice_no - 1) % self.last_slice_no

    def get_projection(self, data):
        if self.plane == "Transversal":
            return data.cube[self.current_slice_no, ::, ::]
        if self.plane == "Sagittal":
            return data.cube[::-1, ::-1, self.current_slice_no]
        if self.plane == "Coronal":
            return data.cube[::-1, self.current_slice_no, ::-1]

    def get_current_slices(self):
        return {
            'Transversal': self._transversal_slice_no,
            'Sagittal': self._sagittal_slice_no,
            'Coronal': self._coronal_slice_no
        }

    def get_last_slices(self):
        return {
            'Transversal': self._transversal_last_slice_no,
            'Sagittal': self._sagittal_last_slice_no,
            'Coronal': self._coronal_last_slice_no
        }

    def load_slices_count(self, data):
        self._transversal_last_slice_no = data.dimz
        self._sagittal_last_slice_no = data.dimy
        self._coronal_last_slice_no = data.dimx

        self._transversal_slice_no = self._transversal_last_slice_no // 2
        self._sagittal_slice_no = self._sagittal_last_slice_no // 2
        self._coronal_slice_no = self._coronal_last_slice_no // 2

    def is_loaded(self):
        """Check if all slice numbers are non-zero"""
        return self._transversal_last_slice_no * self._sagittal_last_slice_no * self._coronal_last_slice_no != 0

    @property
    def current_slice_no(self):
        if self.plane == "Transversal":
            return self._transversal_slice_no
        if self.plane == "Sagittal":
            return self._sagittal_slice_no
        if self.plane == "Coronal":
            return self._coronal_slice_no

    @current_slice_no.getter
    def current_slice_no(self):
        if self.plane == "Transversal":
            return self._transversal_slice_no
        if self.plane == "Sagittal":
            return self._sagittal_slice_no
        if self.plane == "Coronal":
            return self._coronal_slice_no

    @current_slice_no.setter
    def current_slice_no(self, position):
        if self.plane == "Transversal":
            self._transversal_slice_no = position
        if self.plane == "Sagittal":
            self._sagittal_slice_no = position
        if self.plane == "Coronal":
            self._coronal_slice_no = position

    @property
    def last_slice_no(self):
        if self.plane == "Transversal":
            return self._transversal_last_slice_no
        if self.plane == "Sagittal":
            return self._sagittal_last_slice_no
        if self.plane == "Coronal":
            return self._coronal_last_slice_no
