from napalm_ros import ros
import napalm


class RouterApiHelper:
    def __init__(self, ip, port, user, password):
        self.Router_ip = ip
        self.Port = port
        self.UserName = user
        self.Password = password
        self.device = ''

    def Connect(self):
        driver = napalm.get_network_driver('ros')
        self.device = driver(hostname=self.Router_ip, username=self.UserName,
                             password=self.Password, optional_args={'port': self.Port})
        self.device.open()
        return self.device
