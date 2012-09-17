from .home import ViewHomeIndex
from .campaign import ViewCampaignCreate, ViewCampaignDetails
from .user import ViewUserLogin, ViewUserLogout

all = [
    ViewHomeIndex,
    ViewUserLogin,
    ViewUserLogout,
    ViewCampaignCreate,
    ViewCampaignDetails,
]
