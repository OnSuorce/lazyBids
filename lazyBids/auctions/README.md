
# Auction

This is the folder that django creates whenever an app is created with the manage.py script.
There isn't much to do other than defining the models and tests used by the app.
Views, Serializers, Permissions, Urls are defined in the sub folder [api](api/README.md)

# Auction model
Auction model is defined in [models.py](models.py)
|Field   | Type  | Default  | Editable|Description  |
|---|---|---|---|---|
|title|`TextField()`   |   |Yes   |title of the auction|
|uuid   |`UUIDField()` |   |No   |Automatically generated uuid, used to reference specific auction's instances|
|description|`TextField()`   |   |Yes   |Description of the item that is being auctioned|
|starting_bid   |`DecimalField()`   |   |   | Minimun amount to make the first offer
|user   |`ForeignKey()`   |   |?   |Registered user who has posted the auction|
|image_url   |`URLField()`   |  |Yes   |URL of the item's image
|publish_date   |`DateField()`   |   |No   |Date of when the auction is posted
|is_open   |`BooleanField()`   |True   |Yes   |Boolean which determine if an auction is accepting bids
|currency   |`CharField()`    |USD   |?   |Accepted currency
|last_updated   |`DateField()`   |   |Yes   | Automatically inserted date whenever the instance is persisted 
|pk|`BigAutoField()`|Auto Generated|No|Inherited from models.Model field that is used as primary key

The `__str__(self)` function can be overrided to customize the string output making it more readable whenever an Auction instance is printed or casted to string
