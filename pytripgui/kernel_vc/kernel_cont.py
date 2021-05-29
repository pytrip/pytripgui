from pytrip.tripexecuter import KernelModel
from pytrip.tripexecuter import Projectile

import logging

logger = logging.getLogger(__name__)


class KernelController:
    def __init__(self, model, view):
        self.kernels = model
        self.last_kernel_index = None
        self.view = view
        self.user_clicked_save = False
        self._setup_ok_and_cancel_buttons_callbacks()
        self.view.set_selected_beam_kernel_callback(self._current_kernel_index_has_changed)
        self.view.new_beam_kernel_callback(self._new_beam_kernel)
        self.view.remove_beam_kernel_callback(self._remove_current_beam_kernel)

    def _setup_ok_and_cancel_buttons_callbacks(self):
        self.view.set_ok_callback(self._save_and_exit)
        self.view.set_cancel_callback(self._exit)

    def _save_and_exit(self):
        self.set_model_from_view()
        self.user_clicked_save = True
        self.view.exit()

    def _exit(self):
        self.view.exit()

    def _current_kernel_index_has_changed(self, index):
        # this mean there is no data on kernel list
        if index == -1:
            self._new_beam_kernel()

        # if item was deleted, then this statement is false
        if index != self.last_kernel_index:
            # save previous kernel config to VIEW memory
            if self.last_kernel_index is not None:
                current_kernel_config = self._visible_kernel_config
                self.view.replace_kernel_by_index(current_kernel_config, self.last_kernel_index)

        # load new kernel config
        self.last_kernel_index = index
        new_kernel_config = self.view.get_selected_kernel()
        self._visible_kernel_config = new_kernel_config

    def _new_beam_kernel(self):
        kernel = KernelModel("Kernel")
        kernel.projectile = Projectile("H")
        self.view.add_kernel_with_name(kernel, kernel.name)
        self.view.select_recently_added_kernel()

    def _remove_current_beam_kernel(self):
        self.view.remove_current_kernel()

    def set_view_from_model(self):
        # projectile symbols should be setup before setup any kernel
        sorted_projectile = [y[0] for y in sorted(Projectile.projectile_defaults.items(), key=lambda x: x[1][0])]
        self.view.setup_all_available_projectile_symbols(sorted_projectile)
        if not self.kernels:
            self._new_beam_kernel()
            return

        self._setup_kernels()

    def _setup_kernels(self):
        for kernel in self.kernels:
            self.view.add_kernel_with_name(kernel, kernel.name)

    def set_model_from_view(self):
        # saves current kernel config to GUI memory
        self.view.replace_kernel_by_index(self._visible_kernel_config, self.last_kernel_index)

        # read all data from GUI memory
        kernels = self.view.get_all_kernels()
        self.kernels.clear()
        for kernel in kernels:
            self.kernels.append(kernel)

    @property
    def _visible_kernel_config(self):
        kernel = KernelModel()
        kernel.comment = self.view.comment
        kernel.projectile = Projectile("H")
        kernel.projectile.name = self.view.projectile_name
        kernel.projectile.iupac = self.view.projectile_symbol
        kernel.projectile.z = self.view.z
        kernel.projectile.a = self.view.a
        kernel.ddd_path = self.view.ddd_dir_path
        kernel.spc_path = self.view.spc_dir_path
        kernel.sis_path = self.view.sis_path
        kernel.name = self.view.kernel_name
        return kernel

    @_visible_kernel_config.getter
    def _visible_kernel_config(self):
        kernel = KernelModel()
        kernel.comment = self.view.comment
        kernel.projectile = Projectile("H")
        kernel.projectile.name = self.view.projectile_name
        kernel.projectile.iupac = self.view.projectile_symbol
        kernel.projectile.z = self.view.z
        kernel.projectile.a = self.view.a
        kernel.ddd_path = self.view.ddd_dir_path
        kernel.spc_path = self.view.spc_dir_path
        kernel.sis_path = self.view.sis_path
        kernel.name = self.view.kernel_name
        return kernel

    @_visible_kernel_config.setter
    def _visible_kernel_config(self, kernel):
        self.view.comment = kernel.comment
        if kernel.projectile is None:
            kernel.projectile = Projectile("H")
        self.view.projectile_name = kernel.projectile.name
        self.view.projectile_symbol = kernel.projectile.iupac
        self.view.z = kernel.projectile.z
        self.view.a = kernel.projectile.a
        self.view.ddd_dir_path = kernel.ddd_path
        self.view.spc_dir_path = kernel.spc_path
        self.view.sis_path = kernel.sis_path
        self.view.kernel_name = kernel.name
