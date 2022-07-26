from django.shortcuts import render
from image_store.form import ImageForm
from django.http import HttpResponse
import urllib.request
import os
from PIL import Image
import glob


def get_images(request):
    """
    # get images from unsplash.com and save images to local path:'image_store/static/photos/'
    # return required data and image paths to home.html
    """
    try:
        resolution, amount = "1080x1920", 15
        if request.method == 'POST':
            form = ImageForm(request.POST)
            if form.is_valid():
                [os.remove(item) for item in glob.glob('image_store/static/photos/*.png', recursive=True)]
                search_data = request.POST.get('image_name')
                images_list = []
                name_list=[]
                for x in range(int(amount)):
                    image_path = f"https://source.unsplash.com/random/{resolution}/?" + str(
                        "+".join([x for x in search_data.split()]))
                    image = urllib.request.urlretrieve(image_path, "image_store/static/photos/{}.png".format(
                        search_data + '_' + str(x)))
                    images_list.append(image[0])
                    name_list.append(image[0].split('/')[-1])
                return render(request, 'home.html',
                              {'images': ['/static/' + '/'.join(x.split('/')[2:]) for x in images_list], 'form': form,'data':name_list,'name':name_list[0].split('_')[0].title()})
            else:
                form = ImageForm(request.POST)
                return render(request, 'home.html', {'form': form})
        else:
            form = ImageForm(request.POST)
            return render(request, 'home.html', {'form': form})
    except:
        return HttpResponse('Please connect with Internet and try again')


def images_to_pdf(request):
    """"
    Convert and downloaded the all search images into PDF
    """
    image_files = [image for image in glob.glob('image_store/static/photos/*.png', recursive=True)]
    images = [Image.open(image) for image in image_files]
    try:
        pdf_download_to = os.path.expanduser("~") + "/Downloads/{}_images.pdf".format(str(image_files[0].split('\\')[-1]).split("_")[0])
        images[0].save(
            pdf_download_to, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
        )
        response = 'PDF downloaded on your local path : {}'.format(pdf_download_to)
        return render(request, 'home.html', {'response': response})
    except:
        pdf_download_to = "C:/{}_images.pdf".format(str(image_files[0].split('\\')[-1]).split("_")[0])
        images[0].save(
            pdf_download_to, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
        )
        response = 'PDF downloaded on your local path : {}'.format(pdf_download_to)
        return render(request, 'home.html', {'response': response})
