import requests
import zipfile
import io
import xml.etree.ElementTree as ET
import logging

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.dateformat import format
from django.db import connection
from django.http import JsonResponse
from django.urls import reverse
from datetime import datetime
from .forms import AddVatPayerSettingsForm
from .models import Item, ItemTranslation, Vat_payer, Vat_payer_setting, Customer_VAT_check
from .utils import XMLDataProcessor, Translation


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def home(request):
    welcome_page = Translation.get_translation('welcome_page')
        
    return render(request, 'home.html', {'welcome_page': welcome_page})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # or redirect to another page
        else:
            # Handle invalid login
            return render(request, 'login.html', {'error': 'Invalid login'})
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')

def vat_payer(request):
    vat_payers = Vat_payer.objects.all()
    vat_payers_text = Translation.get_translation('vat_payers')
    download_and_populate = Translation.get_translation('download_and_populate')
    add_vat_payer_settings = Translation.get_translation('add_vat_payer_settings')
       
    return render(request, 'vat_payer.html', {
        'vat_payers': vat_payers, 
        'vat_payers_text': vat_payers_text, 
        'download_and_populate': download_and_populate,
        'add_vat_payer_settings': add_vat_payer_settings
        })

def vat_payer_settings_record(request, pk):
    vat_payer_settings_record = Vat_payer_setting.objects.get(id=pk)
    return render(request, 'vat_payer_settings_record.html', {'vat_payer_settings_record': vat_payer_settings_record})

def update_vat_payer(request):
    x = Vat_payer.objects.all()
    x.delete()

    try:
        # Step 1: Download the zip file and log progress
        url = "https://report.financnasprava.sk/ds_dphs.zip"
        logging.info("Downloading zip file from: %s", url)
        response = requests.get(url, timeout=60)
        logging.info("Download complete")

        # Step 2: Load the zip file from memory and log progress
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
        logging.info("Zip file loaded into memory")

        # Step 3: Find and read the XML file within the zip file
        xml_file_name = [file for file in zip_file.namelist() if file.endswith('.xml')]

        if not xml_file_name:
            logging.error("No XML file found in the zip archive")
            return redirect('vat_payer')  # Exit if no XML file found

        xml_file_name = xml_file_name[0]
        logging.info("XML file found: %s", xml_file_name)

        with zip_file.open(xml_file_name) as xml_file:
            # Step 4: Parse the XML and log progress
            tree = ET.parse(xml_file)
            root = tree.getroot()
            logging.info("XML file parsed")

            # Extract and format DatumAktualizacieZoznamu (convert from DDMMYYYY to YYYY-MM-DD)
            datum_aktualizacie = root.find('DatumAktualizacieZoznamu').text
            try:
                datum_aktualizacie = datetime.strptime(datum_aktualizacie, '%d%m%Y').strftime('%Y-%m-%d')
            except ValueError as e:
                logging.error(f"Invalid date format for DatumAktualizacieZoznamu: {e}")
                datum_aktualizacie = None  # Handle invalid date format

            # Step 5: Collect Vat_payer objects to be bulk inserted
            vat_payer_list = []
            for idx, item in enumerate(root.findall('.//DS_DPHS/ITEM')):
                try:
                    ic_dph = item.find('IC_DPH').text if item.find('IC_DPH') is not None else None
                    ico = item.find('ICO').text if item.find('ICO') is not None else None
                    nazov_ds = item.find('NAZOV_DS').text if item.find('NAZOV_DS') is not None else None
                    obec = item.find('OBEC').text if item.find('OBEC') is not None else None
                    psc = item.find('PSC').text if item.find('PSC') is not None else None
                    ulica_cislo = item.find('ULICA_CISLO').text if item.find('ULICA_CISLO') is not None else None
                    stat = item.find('STAT').text if item.find('STAT') is not None else None
                    druh_reg_dph = item.find('DRUH_REG_DPH').text if item.find('DRUH_REG_DPH') is not None else None
                    datum_reg = item.find('DATUM_REG').text if item.find('DATUM_REG') is not None else None
                    datum_zmeny_druhu_reg = item.find('DATUM_ZMENY_DRUHU_REG').text if item.find('DATUM_ZMENY_DRUHU_REG') is not None else None

                    try:
                        if datum_reg:
                            datum_reg = datetime.strptime(datum_reg, '%d.%m.%Y').strftime('%Y-%m-%d')
                        if datum_zmeny_druhu_reg:
                            datum_zmeny_druhu_reg = datetime.strptime(datum_zmeny_druhu_reg, '%d.%m.%Y').strftime('%Y-%m-%d')
                    except ValueError as e:
                        logging.error(f"Invalid date format in payer element: {e}")
                        continue

                    # Create Vat_payer instance and append it to the list
                    vat_payer_list.append(
                        Vat_payer(
                            DatumAktualizacieZoznamu=datum_aktualizacie,
                            IC_DPH=ic_dph,
                            ICO=ico,
                            NAZOV_DS=nazov_ds,
                            OBEC=obec,
                            PSC=psc,
                            ULICA_CISLO=ulica_cislo,
                            STAT=stat,
                            DRUH_REG_DPH=druh_reg_dph,
                            DATUM_REG=datum_reg,
                            DATUM_ZMENY_DRUHU_REG=datum_zmeny_druhu_reg
                        )
                    )

                                    
                except Exception as e:
                    logging.error("Error processing payer element: %s", str(e))

            # Step 6: Bulk insert all collected objects
            Vat_payer.objects.bulk_create(vat_payer_list)
            # Log the total number of processed rows
            total_rows_processed = len(vat_payer_list)
            logging.info(f"Processed {total_rows_processed} rows")
            logging.info("Bulk insert complete for all payers")

        messages.success(request, "údaje platcov DPH boli aktualizované")
        return redirect('vat_payer')

    except requests.exceptions.RequestException as e:
        logging.error("Failed to download or process the file: %s", str(e))
        return redirect('vat_payer')

def get_vat_payers(request):
    if request.method == 'GET':
        vat_payers = Vat_payer.objects.all().values(
            'id',  # Explicitly include 'id'
            'NAZOV_DS', 'ICO', 'IC_DPH', 'OBEC', 'PSC', 'ULICA_CISLO', 'STAT', 'DRUH_REG_DPH', 'DATUM_REG', 'DATUM_ZMENY_DRUHU_REG'
        )[:1000]  # Limit to 1000 records

        formatted_vat_payers = []
        for vat_payer in vat_payers:
            formatted_vat_payers.append({
                'Názov': vat_payer["NAZOV_DS"] or '',
                'IČO': vat_payer['ICO'] or '',
                'IČ DPH': vat_payer['IC_DPH'] or '',
                'Obec': vat_payer['OBEC'] or '',
                'PSČ': vat_payer['PSC'] or '',
                'Ulica, číslo': vat_payer['ULICA_CISLO'] or '',
                'Štát': vat_payer['STAT'] or '',
                'Druh reg. DPH': vat_payer['DRUH_REG_DPH'] or '',
                'Dátum reg.': format(vat_payer['DATUM_REG'], 'd.m.Y') if vat_payer['DATUM_REG'] else '',
                'Dátum zmeny druhu reg.': format(vat_payer['DATUM_ZMENY_DRUHU_REG'], 'd.m.Y') if vat_payer['DATUM_ZMENY_DRUHU_REG'] else ''
            })

        return JsonResponse({'rows': formatted_vat_payers})

def get_vat_payer_settings(request):
    if request.method == 'GET':
        vat_payer_settings = Vat_payer_setting.objects.all().values(
            'id',
            'DRUH_REG_DPH',
            'PLATNY_DRUH_REG'
        )

        formatted_vat_payer_settings = []
        for vat_payer_setting in vat_payer_settings:
            formatted_vat_payer_settings.append({
                'Druh reg. DPH': f'<a href="{reverse("vat_payer_settings_record", args=[vat_payer_setting["id"]])}">{vat_payer_setting["DRUH_REG_DPH"] or ""}</a>',
                'platný': vat_payer_setting['PLATNY_DRUH_REG']
            })

        return JsonResponse({'rows': formatted_vat_payer_settings})


def get_customer_vat_check(request):
    if request.method == 'GET':
        customer_vat_checks = Customer_VAT_check.objects.all().values(
            'ID',
            'NAZOV',
            'ICO',
            'IC_DPH_customer',
            'IC_DPH_fin',
            'DRUH_REG_DPH',
            'DESCRIPTION'
        )[:1000]  # Limit to 1000 records

        
        formatted_customer_vat_check = []
        for customer_vat_check in customer_vat_checks:
            formatted_customer_vat_check.append({
                'id': customer_vat_check["ID"],
                'Názov': customer_vat_check["NAZOV"],
                'IČO': customer_vat_check["ICO"],
                'IČ DPH zákazník': customer_vat_check["IC_DPH_customer"],
                'IČ DPH fin': customer_vat_check["IC_DPH_fin"],
                'druh reg. DPH': customer_vat_check['DRUH_REG_DPH'],
                'popis': customer_vat_check['DESCRIPTION']
            })

        return JsonResponse({'rows': formatted_customer_vat_check})


def test(request):
     return render(request, 'test.html', {})



def test_vat_payer(request):
    vat_payers = Vat_payer.objects.all()  # Fetch all VAT payers
       
    return render(request, 'test_vat_payer.html', {'vat_payers': vat_payers})

def delete_vat_payer_settings(request, pk):
    delete_it = Vat_payer_setting.objects.get(id=pk)
    delete_it.delete()
    
    messages.success(request, "Záznam bol úspešne odstránený")
    return redirect('vat_payer')


def add_vat_payer_settings(request):
    form = AddVatPayerSettingsForm(request.POST or None)
    if request.method=="POST":
        if form.is_valid():
            add_vat_payer_settings = form.save()
            messages.success(request, "Záznam bol pridaný")
            return redirect('vat_payer')
            
    return render(request, 'add_record.html', {'form': form,'form_action_url': reverse('add_vat_payer_settings')})


            




