# Aviate Assignment

A RESTful API service using Django REST Framework as Backend with Postgres Database and Python=3.7.
This service has enpoints for :

* Creating a Profile
* Viewing a Profile
* Updating a Profile
* Soft Deleting a Profile
>
* Uploading Resume for a Profile
* Updating Resume for a Profile (on Updating, Old Resumes are also tracked)
* Viewing Current Resume
* Viewing Old Resume
>
* Super View of Complete Data
* Viewing Deleted Profiles
<hr/>

## Profile Model Fields Description
Each 'Profile' instance in the model has following fields :
<br/>
| Field | Description |
| :--: | :-----------: |
| id | Auto-Generated Field, acts as a *(primary key)*|
| name | Character Field |
| password | Character Field |
| age | Integer Field |
| contact | Integer Field |
| resume | FileField (stores CURRENT Resume's Path)|
| count | Auto-Generated Field (Tracks the count of Resume Uploaded) |
| prev_resume_list | JSON Field (stores ALL Old Resume's Path)|

<hr/>

## ENDPOINTS Description
<br/>

> Assumption : Development Server launched at URL = http://localhost:8000/

### 1. Creating a Profile
```
REQUEST : POST
URL = http://localhost:8000/create/
```
<br/>

| Request Fields | Type |
| :--: | :-----------: |
| name | Required |
| password | Required |
| age | Required |
| contact | Required |

> Comments
* This Endpoint allows only above Profile Details to be passed and does not allow 'id' & 'resume' fields. Separate Endpoint for Resume Upload to a Profile.
<hr/>

### 2. Viewing a Profile
```
REQUEST : GET
URL = http://localhost:8000/view_profile/<Profile_ID>/
```
<br/>

> Comments
* Performs a Profile Exists Validation Check
<hr/>


### 3. Updating a Profile's Details
```
REQUEST : PUT, PATCH
URL = http://localhost:8000/profile_ops/
```
<br/>

| Request Fields | Type |
| :--: | :-----------: |
| id | Required |
| password | Required |
| name | Editable |
| age | Editable |
| contact | Editable |


> Comments

* UPDATE operations for a Profile
* Profiles accessed using primary key = id (passed as a request field)
* Only the primary Profile Details(except RESUME) can be UPDATED via this endpoint
* Validation Check to avoid Update on RESUME field
* Separate Endpoint for RESUME Operations
* Validation Check for Profile Exists, ID, Password performed
<hr/>

### 4. Deleting a Profile
```
REQUEST : DELETE
URL = http://localhost:8000/profile_ops/
```
<br/>

| Request Fields | Type |
| :--: | :-----------: |
| id | Required |
| password | Required |

> Comments

* DELETE operation for a Profile
* Profiles accessed using primary key = id (passed as a request field)
* Validation Check for Profile Exists, ID, Password performed
* SOFT_DELETE operation implemented
* Soft Delete is that it's not permanently deleted it is only marked deleted so it is not shown to any user including admin.
<hr/>

### 5. UPLOAD / UPDATE a Profile's RESUME
```
REQUEST : PUT, PATCH
URL = http://localhost:8000/upload_resume/

Uploaded Resumes Storage Directory : "/media/"
FileName format : <Profile_Name>_<Resume_Number>
```
<br/>

| Request Fields | Type |
| :--: | :-----------: |
| id | Required |
| password | Required |
| resume | Required |


> Comments

* Only the RESUME field of a Profile can be UPDATED via this endpoint
* Separate Endpoint to UPDATE Profile Details
* Validation Check for Profile Exists, ID, Password performed
* Validation Check whether RESUME is passed in REQUEST for UPLOAD
* *__If a RESUME already exists for a Profile, then it is pushed into OLD RESUMEs,
Uploaded RESUME marked as CURRENT Resume__*
<hr/>

### 6. Viewing a Profile's CURRENT Resume
```
REQUEST : GET
URL = http://localhost:8000/view_current_resume/<Profile_ID>/
```
<br/>

> Comments
* Performs a Profile Exists Validation Check
* Performs a Resume Exists Validation Check
<hr/>

### 7. Viewing a Profile's OLD Resume
```
REQUEST : GET
URL = http://localhost:8000/view_old_resume/<Profile_ID>/
```
<br/>

> Comments
* Performs a Profile Exists Validation Check
* Performs an Old Resume's Exists Validation Check
<hr/>

### 8. SUPER View of the Database
```
REQUEST : GET
URL = http://localhost:8000/super_view/
```
<br/>

> Comments
* A Super VIEW operation for a complete DATABASE Overview
* Displays ALL the Profiles with ALL of their primary & hidden fields
<hr/>

### 9. Viewing Deleted Profiles (not visible to ADMIN also)
```
REQUEST : GET
URL = http://localhost:8000/view_deleted/
```
<br/>

> Comments
* VIEW operation for viewing DELETED Profiles
* *__Profiles are not HARD_DELETED, just MARKED Deleted__*
* Displays ALL the Deleted Profiles with ALL of their fields
<hr/>
