from .models import Profile
from .serializers import ProfileSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ProfileCreate(APIView) :
    """
    Create a Profile with Required Entries of Name, Age & Contact
    """
    def post(self, request, format=None):

        if(request.data.get("resume")) :
            return Response({"Error" : "Upload Resume at a later stage!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message" : "Success! Profile Created"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileList(APIView):
    """
    List all Profiles registered in the database
    """
    def get(self, request, format=None):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)


class ProfileDetails(APIView):
    """
    RUD operations for singular profile in the database
    """
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():

            profile.resume_list['old_resume_'+str(profile.count)] = str(profile.resume)
            profile.count = profile.count + 1

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeletedProfiles(APIView) :

    def get(self, request, format=None):
        profiles = Profile.original_objects.all().filter(deleted_on__isnull=False)
        print(profiles)
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)
