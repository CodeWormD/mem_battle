from rest_framework import serializers

from apps.users.models import Profile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    subs = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ('owner', 'subs')


    def get_subs(self, obj):
        return obj.subs

