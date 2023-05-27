from .auth import AuthController
from .in_and_out import InAndOutController
from .region import RegionController
from .vehicle import VehicleController
from .entrance_auth import EntranceAuthController
from .ticket import TicketController


authCtrl = AuthController()
inAndOutCtrl = InAndOutController()
regionCtrl = RegionController()
vehicleCtrl = VehicleController()
entranceAuthCtrl = EntranceAuthController()
ticketCtrl = TicketController()