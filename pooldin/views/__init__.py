from .home import ViewHomeIndex
from .campaign import ViewCampaignCreate, ViewCampaignDetails
from .user import ViewUserLogin

all = [
    ViewHomeIndex,
    ViewUserLogin,
    ViewCampaignCreate,
    ViewCampaignDetails,
]
