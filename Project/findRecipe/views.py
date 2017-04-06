import os
import logging
import httplib2
import argparse
import base64
from PIL import Image
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.conf import settings as django_settings
from Project import settings
import markdown
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets




# Create your views here.



import argparse
import base64

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
# [END import_libraries]


@login_required
def _index(request,photo_file):
    """Run a label request on a single image"""

    # [START authenticate]
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)
    # [END authenticate]

    # [START construct_request]
    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 5
                }]
            }]
        })
        lab = []
        # [END construct_request]
        # [START parse_response]
        response = service_request.execute()
        label = response['responses'][0]['labelAnnotations']
        for l in range(len(label)):
          lab.append(response['responses'][0]['labelAnnotations'][l]['description'])
        return render(request,'findRecipe/found.html',{'label':lab})
        
# [END parse_response]

@login_required
def food_picture(request):
    uploaded_picture = False
    try:
        if request.GET.get('upload_food_picture') == 'uploaded':
            uploaded_picture = True

    except Exception, e:
        pass

    return render(request, 'findRecipe/find.html',{'uploaded_picture':uploaded_picture})

@login_required
def upload_food_picture(request):
    try:
        food_images = django_settings.MEDIA_ROOT + '/food_images/'
        if not os.path.exists(food_images):
            os.makedirs(food_images)
        f = request.FILES['picture']
        filename = food_images + request.user.username + '_tmp.jpg'
        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        im = Image.open(filename)
        width, height = im.size
        if width > 350:
            new_width = 350
            new_height = (height * 350) / width
            new_size = new_width, new_height
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(filename)

        return redirect('/findRecipe/food_picture/?upload_food_picture=uploaded')

    except Exception, e:
        print e
        return redirect('/findRecipe/food_picture/')


@login_required
def save_uploaded_food_picture(request):
    try:
        x = int(request.POST.get('x'))
        y = int(request.POST.get('y'))
        w = int(request.POST.get('w'))
        h = int(request.POST.get('h'))
        tmp_filename = django_settings.MEDIA_ROOT + '/food_images/' + request.user.username + '_tmp.jpg'
        filename = django_settings.MEDIA_ROOT + '/food_images/' + request.user.username + '.jpg'
        im = Image.open(tmp_filename)
        cropped_im = im.crop((x, y, w+x, h+y))
        cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
        cropped_im.save(filename)
    except Exception, e:
        pass
   
    return _index(request,filename)
