from deta import Deta

deta = Deta()

# Our user database
auth_db = deta.Base("auth")

# Our url database
url_db = deta.Base("urls")

# Our snapshots database
snapshots_db = deta.Base("snapshots")

# Our settings database
settings_db = deta.Base("settings")

# Our QR Code storage drive
qr_drive = deta.Drive("codes")