from .models import Profile
from .serializers import ProfileSerializer, ResumeSerializer, SuperSerializer
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

"""
Create a Profile with Required Entries of Name, Password, Age & Contact
Request is NOT allowed to ADD resume as there's a separate endpoint

ACCESS_URL : "/create/" , Request Type : GET
"""
class ProfileCreate(APIView) :

    def post(self, request, format=None):

        if(request.data.get("resume")) :
            return Response({"Error" : "Upload Resume after creating Profile!"}, status=status.HTTP_400_BAD_REQUEST)

        if(request.data.get("id")) :
            return Response({"Error" : "ID will be automatically generated!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"Message" : "Success! Profile Created" , "ID" : serializer.data["id"]} , status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



"""
Validity Check function used for UPDATE (PUT,PATCH) requests
Validates whether ID and Password fields are passed in the REQUEST
Performs Profile Exist Check,
If Exists, performs Correct Password Check
"""
def validity_check(request):

    if(not request.data.get("id")) :
        return Response({"Error" : "Enter Profile ID to make changes"}, status=status.HTTP_400_BAD_REQUEST)
    if(not request.data.get("password")) :
        return Response({"Error" : "Enter Password to make changes"}, status=status.HTTP_400_BAD_REQUEST)

    id = request.data.get("id")
    try:
        profile = Profile.objects.get(pk=id)
    except Profile.DoesNotExist:
        raise Http404

    if(request.data.get("password") != profile.password) :
        return Response({"Error" : "Incorrect Password"}, status=status.HTTP_400_BAD_REQUEST)


"""
UPDATE & DELETE operations for a Profile
Profiles accessed using primary key = id (passed as a request field)

Only the primary Profile Details(except RESUME) can be UPDATED via this endpoint
Validation Check to avoid Update/Delete on RESUME field
Separate Endpoint for RESUME Operations

Reuired Fields : id , password
Validation Check for Profile Exists, ID, Password performed

SOFT_DELETE operation implemented
Soft Delete is that it's not permanently deleted it is only marked deleted
so it is not shown to any user including admin.

ACCESS_URLs :
Update a Profile : "/profile_ops/" , Request Type : PUT, PATCH
Delete a Profile : "/profile_ops/" , Request Type : DELETE
"""
class ProfileOperations(APIView):
    def put(self, request,format=None):

        if(request.data.get("resume")) :
            return Response({"Error" : "Use /resume_ops/ to update resume"}, status=status.HTTP_400_BAD_REQUEST)

        invalid_response = validity_check(request)
        if(invalid_response) :
            return invalid_response

        profile = Profile.objects.get(pk = request.data.get("id"))
        serializer = ProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request,format=None):

        invalid_response = validity_check(request)
        if(invalid_response) :
            return invalid_response

        profile = Profile.objects.get(pk = request.data.get("id"))
        profile.delete()

        return Response({"Message" : "Profile Successfully Deleted!"} , status=status.HTTP_204_NO_CONTENT)



"""
VIEW operation for a Profile's Details
Profile Exists Validation

ACCESS_URLs : "/view_profile/<profile_id>/" , Request Type : GET
"""
@api_view(["GET"])
def ViewProfile(request, pk) :

    if(request.method == "GET") :
        try:
            profile = Profile.objects.get(pk=pk)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)

        except Profile.DoesNotExist:
            raise Http404


"""
UPLOAD & UPDATE operations for a Profile's Resume

Only the RESUME field of a Profile can be UPDATED via this endpoint
Separate Endpoint to UPDATE Profile Details

Reuired Fields : id , password
Validation Check for Profile Exists, ID, Password
Validation Check whether RESUME is passed in REQUEST for UPLOAD

If a RESUME already exists for a Profile, then it is pushed into OLD RESUMEs,
Uploaded RESUME marked as CURRENT Resume

Uploaded Resumes Storage Directory : "/media/"

ACCESS_URLs : "/upload_resume/" , Request Type : PUT, PATCH
"""
@api_view(["PUT", "PATCH"])
def UploadResume(request) :

    if(request.method == "PUT" or request.method == "PATCH") :

        if(not request.data.get("resume")) :
            return Response({"Error" : "Please select resume to upload"}, status=status.HTTP_204_NO_CONTENT)
        invalid_response = validity_check(request)

        if(invalid_response) :
            return invalid_response

        profile = Profile.objects.get(pk = request.data.get("id"))

        if(profile.resume) :
            profile.prev_resume_list['old_resume_'+str(profile.count)] = str(profile.resume)
            profile.count = profile.count + 1

        serializer = ResumeSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message" : "Success! Resume Uploaded"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
VIEW operation for a Profile's Current Resume

Validation CHECK whether a RESUME has been uploaded for the Profile or Not
Profile Exists Validation as well

ACCESS_URLs : "view_current_resume/<profile_id>/" , Request Type : GET
"""
@api_view(["GET"])
def ViewCurrentResume(request, pk) :

    if(request.method == "GET") :
        try:
            profile = Profile.objects.get(pk=pk)

            if(not profile.resume) :
                return Response({"Message" : "No Resume Uploaded Yet!"} , status=status.HTTP_204_NO_CONTENT)

            serializer = ProfileSerializer(profile)
            return Response({
                        "ID" : serializer.data['id'],
                        "Name" : serializer.data['name'],
                        "Current Resume" : serializer.data['resume'],
            })

        except Profile.DoesNotExist:
            raise Http404


"""
VIEW operation for a Profile's Old Resumes

Validation CHECK whether OLD RESUMEs exist!
Profile Exists Validation as well

ACCESS_URLs : "view_old_resume/<profile_id>/" , Request Type : GET
"""
@api_view(["GET"])
def ViewOldResume(request, pk) :

    if(request.method == "GET") :
        try:
            profile = Profile.objects.get(pk=pk)

            if(not profile.prev_resume_list) :
                return Response({"Message" : "No Previous Resumes Found!"} , status=status.HTTP_204_NO_CONTENT)

            serializer = ResumeSerializer(profile)
            print(serializer)
            return Response({
                        "ID" : serializer.data['id'],
                        "Name" : serializer.data['name'],
                        "Previous Resumes" : serializer.data['prev_resume_list'],
            })

        except Profile.DoesNotExist:
            raise Http404




"""
A Super VIEW operation for a complete DATABASE Overview
Displays ALL the Profiles with ALL of their fields

ACCESS_URLs : "/super_view/" , Request Type : GET
"""
@api_view(["GET"])
def SuperList(request) :

    if(request.method == "GET") :
        profiles = Profile.objects.all()
        serializer = SuperSerializer(profiles, many=True)
        return Response(serializer.data)


"""
A VIEW operation for viewing DELETED Profiles
Note : Profiles are not HARD_DELETED, just MARKED Deleted
Displays ALL the Deleted Profiles with ALL of their fields

ACCESS_URLs : "/view_deleted/" , Request Type : GET
"""
@api_view(["GET"])
def ViewDeletedProfiles(request) :

    if(request.method == "GET") :
        profiles = Profile.original_objects.all().filter(deleted_on__isnull=False)
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)
