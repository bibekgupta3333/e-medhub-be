import uuid
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from rest_framework import permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import CompanyProfileSerializer, UserProfileSerializer, MyUserSerializer
from .models import CompanyProfile, UserProfile, ResetToken
User = get_user_model()


class SignupView(APIView):
    """
    This method helps signup user by taking data from frontend.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = self.request.data
        username = data['username']
        email = data['email']
        password = data['password']
        password2 = data['password2']
        is_buyer = data['is_buyer']
        is_seller = data['is_seller']
        print(is_seller, is_buyer)
        if password == password2:
            print('hello')
            objectsa = User.objects.filter(email=email).exists()
            print(objectsa)
            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists'})
            else:
                if len(password) < 6:
                    return Response({'error': 'Password must be at least 6 Characters'})
                else:
                    user = User.objects.create_user(username=username,
                                                    email=email, password=password, is_buyer=is_buyer, is_seller=is_seller)
                    user.save()
                    # serializer = MyUserSerializer(data=data)
                    # if serializer.is_valid():
                    #     serializer.save()
                    return Response({'success': 'User created succesfully'})
        else:
            return Response({'error': 'Passwords do not match'})


class UserProfileView(APIView):
    """
    This method helps show userprofile accoding to user wise and also helps to update user profile.
    """

    permission_classes = (permissions.AllowAny,)

    def get_object(self):
        return UserProfile.objects.all()

    def get(self, request, pk, format=None):
        user_profile = self.get_object().get(pk=pk)
        print(user_profile)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user_profile = self.get_object().get(pk=pk)
        serializer = UserProfileSerializer(user_profile, request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)


class CompanyProfileView(APIView):
    """
    This method helps show companyprofile accoding to user wise and also helps to update company profile.
    """
    permission_classes = (permissions.AllowAny,)

    def get_object(self):
        return CompanyProfile.objects.all()

    def get(self, request, pk, format=None):
        company_profile = self.get_object().get(pk=pk)
        serializer = CompanyProfileSerializer(company_profile)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        company_profile = self.get_object().get(pk=pk)
        print(company_profile.user.id)

        # user = User.objects.all().get(pk=company_profile.get('user').get('id'))
        user = get_object_or_404(User, pk=company_profile.user.id)
        print(user)

        serializer = CompanyProfileSerializer(company_profile, request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)


class ResetPasswordView(APIView):
    """
    This method helps reset user password by taking users email by sending the email.
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request, uidb64):
        reset = ResetToken.objects.all().get(token=uidb64)
        return Response({'token': reset.token, 'email': reset.email})

    def post(self, request, format=None):
        data = self.request.data
        email = data['email']
        print("hello")
        if User.objects.filter(email=email).exists():
            user = User.objects.all().get(email=email)
            try:
                token = str(uuid.uuid4())
                current_site = get_current_site(self.request)
                print(current_site)
                SUBJECT = f"Reset Password {user.username}"
                MESSAGE = f"Hello {user.username} from EMEDHUB \n\t click this link to reset password http://{current_site}/api/accounts/activate/{token}/"
                send_mail(
                    SUBJECT,
                    'Name: '
                    + user.username
                    + '\nEmail: '
                    + user.email
                    + '\n\nMessage:\n'
                    + MESSAGE,
                    'didwhatlab@gmail.com',
                    [user.email, ],
                    fail_silently=False
                )
                reset = ResetToken(token=token, email=user.email)
                reset.save()
                return Response({'success': 'Password reset successfully. Please check your mail'})
            except:
                return Response({'errors': 'Error has occured during resetting password'})
        else:
            return Response({"errors": "This email does not exist"})

    def put(self, request, uidb64):
        if ResetToken.objects.all().get(token=uidb64):
            if ResetToken.objects.all().get(token=uidb64).used:
                return Response({'errors': 'Password has been already reset.And Link is used'})
            else:
                email = ResetToken.objects.all().get(token=uidb64).email
                user = User.objects.all().get(email=email)
                data = self.request.data
                password = data['password']
                password2 = data['password2']
                if password == password2:
                    user.set_password(password)
                    user.save()
                    token = ResetToken.objects.all().get(token=uidb64)
                    token.used = True
                    token.save()
                    return Response({'success': "Password changed successfully."})
                else:
                    return Response({'errors': "password does not changed successfully"})
