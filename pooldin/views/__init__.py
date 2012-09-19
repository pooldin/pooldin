from .home import ViewHomeIndex
from .campaign import ViewCampaignCreate, ViewCampaignDetails
from .user import ViewUserLogin, ViewUserLogout, ViewUserProfile

all = [
    ViewHomeIndex,
    ViewUserLogin,
    ViewUserLogout,
    ViewCampaignCreate,
    ViewCampaignDetails,
    ViewUserProfile,
]
