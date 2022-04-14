from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

class UserRegistrationSerializer(BaseUserRegistrationSerializer): #Override of the djoser's default registration
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('username','email','password') #fields required for the registration