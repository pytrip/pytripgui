class Trip98ConfigModel:
    def __init__(self):
        self.remote_execution = False
        self.hlut_path = ""
        self.dedx_path = ""

        # Local execution
        self.wdir_path = ""
        self.trip_path = ""

        # remote execution
        self.host_name = ""
        self.username = ""
        self.password = ""
