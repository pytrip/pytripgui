class Trip98ConfigModel:
    def __init__(self):
        self.name = ""
        self.remote_execution = False
        self.hlut_path = ""
        self.dedx_path = ""
        self.wdir_path = ""
        self.trip_path = ""

        # remote execution
        self.host_name = ""
        self.user_name = ""
        self.pkey_path = ""
        self.password = ""
        self.wdir_remote_path = ""
