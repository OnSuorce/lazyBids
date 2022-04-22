# Auction API
These are the essential files for pretty much any api made with DRF
+ [views.py](views.py) defines the endpoint's logic
+ [serializers.py](serializers.py) defines how objects must be serialized
+ [urls.py](urls.py)  used to define the endpoint urls

These are the non-essential files
 
 + [permissions.py](permissions.py) handles the authorization 
 + [paginations.py](paginations.py) handles the pagination

# Views
This is how views looks like:
```python
class AuctionView(APIView):

    def get(self, request):
        return Response("Successful")
```
These view returns "Successful".


```python
class AuctionDetailView(generics.DestroyAPIView, generics.UpdateAPIView, generics.RetrieveAPIView):
        queryset = Auction.objects.all()
        serializer_class = AuctionDetailSerializer
        permission_classes = [IsAuthorizedOrReadOnly, IsAuthenticated]
        lookup_field = "uuid"
```
These view returns a specific auction's instance based on the UUID in the url (GET /api/v1/auctions/{uuid}/) or destroys it depending on the HTTP method

Most of the view i implemented used the [generics API View](https://www.django-rest-framework.org/api-guide/generic-views/#generic-views) which provides many useful functionalities (such as crud operations) to handle models but they are also completly customizable.
This is the view that returns a list containing all the created auctions:

```python
class AuctionListView(generics.ListAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = AuctionsPagination

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = AuctionDetailSerializer(self.paginate_queryset(queryset), many=True)
        
        return Response(self.get_paginated_response(serializer.data).data)
```

To implement a generic View it's sufficient to define a class which inherits a generic View and override 2 fields: 
+ **queryset**: The objects that are handled and returned from this view 
+ **serializer_class**: Which serializer to use to serialize/deserialize the objects
  
With only those overrides the view would return every single auction saved in the database to every client requesting it. In the example case there are a few more overrides:

+ **permissions_classes**: Array containing all the classes that defines the authorization/authentication. In this case its being used the default IsAuthenticated class from django which authenticate users based on how the authentication has been configured in the settings.py file
+ **pagination_class**: A class that defines the pagination
+ **list(self, request)**: this method has been overrided to make the view return a paginated list of auctions. The logic of the paginations it's the one in the pagination_class attribute
  

A more """"complex"""" view looks like this:
```python
  class AuctionWinnerView(generics.RetrieveUpdateAPIView):
        
        queryset = Auction.objects.filter(is_open=True)
        serializer_class = AuctionWinnerSerializer
        permission_classes = [IsAuthorizedOrReadOnly, IsAuthenticated]
        lookup_field = "uuid"

        def update(self, request, *args, **kwargs):

            try:
                bid = Bid.objects.get(uuid=request.data.get('bid_uuid'))
            except ObjectDoesNotExist:
                return Response({'bid_uuid': 'No matching bid has been found with this uuid'},
                            status=status.HTTP_404_NOT_FOUND)

            bid.has_won = True
            bid.save(update_fields=['has_won'])
            return super().update(request, *args, **kwargs)

        def perform_update(self, serializer):
            serializer.save(is_open=False)

        def retrieve(self, request, *args, **kwargs):
                auction = self.get_object()

                bid = Bid.objects.get(uuid=request.data.get('bid_uuid'))
                
                return Response({'auction_uuid': auction.uuid, 'winner_uuid':bid.uuid})
                
```
This is the view that is used by the auction's user to accept a bid.
The queryset doesn't take all auction instances but the ones with the field `is_open` set to `True` because you can't accept bids while the auction is closed :smiley:.
The `serializers_class` uses a specific serializer as the class name suggests.
There are 2 permissions classes: the django's class and `IsAuthorizedOrReadOnly` class which is the one i wrote to make sure only the owner of the auction can access unsafe http methods (POST, DELETE, PUT...).
 The `lookup_field` is assigned to 'uuid' which means that the auction instance should be retrieved using the uuid provided, by default django would use the primary key which in this case would be the 'pk' field.

Another note worthy detail is the fact that both `perform_update()` and `update()` have been overrided. These methods work together to make sure that the requested instance of an auction gets updated with the new values. A detailed explanation is available in the bid's api folder.

# Serializers

Serializers are classes that manage how models are serialized in Python datatypes or deserialized in JSON. They are very useful as, combined with generics views, they make serialization easy to implement and use.
This is the serializer class used by the create view:
```python
class AuctionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model= Auction
        exclude = ['id','publish_date', 'user', 'last_updated']
    
    def validate_starting_bid(self, value):
        if(value<1):
            raise serializers.ValidationError("starting bid not valid, must be 1.00 or greater")
        return value
```
Serializers are made with 2 classes: in the outer class you'd override some field serialization ore define validators, in the inner class you'd have to specify which model and fields to serialize. In this case the serializer would process an auction model with all the fields excluding the ones in the `exclude` array. There many other ways to handle this as documented [here](https://www.django-rest-framework.org/api-guide/serializers/#specifying-which-fields-to-include). The method defined is a field level validator which essentially validate the data for a single field. Their firm must be `validate_< name of the field >(self, value)`.

In the `AuctionDetailSerializer` there is an example of a custom field serialization:
```python
class AuctionUserSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = CustomUser
        read_only_fields = ["email", "username"]

class AuctionDetailSerializer(serializers.ModelSerializer):
    user = AuctionUserSerializer()

    class Meta:
        model = Auction
        exclude = ['id']
        read_only_fields = ['publish_date','last_updated']
```

To serialize the user field (which is a foreign key related to the user's model) it's being used another serializator. This allows to fully control how the serialization for a single field should work instead of using the default one.
This is what the json output would like of the default and the shown one:
```json
//Default
{
  "user": 1,
  "title": "Postcard",
  "uuid": "2ce0bd2f-d634-496a-846e-9577c72efff1",
  "description": "A cool postcard",
  "starting_bid": "1.99",
  ...
}
```

```json
//with AuctionUserSerializer
{
  "user": {
    "email": "sus@mail.com",
    "username": "PIPPO"
  },
  "title": "Postcard",
  "uuid": "2ce0bd2f-d634-496a-846e-9577c72efff1",
  "description": "A cool postcard",
  "starting_bid": "1.99",
  ...
}
```