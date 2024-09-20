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
from django.db import connection
from django.http import JsonResponse
from datetime import datetime
from .models import Vat_payer
from .utils import XMLDataProcessor

# Set up logging
logging.basicConfig(level=logging.INFO)

def home(request):
     return render(request, 'home.html', {})


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
    messages.success(request, "Boli ste odhlásení")
    return redirect('login')

def vat_payer(request):
    vat_payers = Vat_payer.objects.all()  # Fetch all VAT payers

    # Set up pagination with 100 records per page
    '''paginator = Paginator(vat_payers, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'vat_payer.html', context)'''
    return render(request, 'vat_payer.html', {'vat_payers': vat_payers})

def vat_payer_record(request, pk):
    vat_payer_record = Vat_payer.objects.get(id=pk)
    return render(request, 'vat_payer_record.html', {'vat_payer_record': vat_payer_record})

def update_vat_payer_old(request):
    # Clear existing data
    Vat_payer.objects.all().delete()

    with connection.cursor() as cursor:
        cursor.execute("ALTER TABLE website_vat_payer AUTO_INCREMENT = 1;")

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
            return redirect('home')  # Exit if no XML file found

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

            logging.info(f"DatumAktualizacieZoznamu: {datum_aktualizacie}")

            # Step 5: Iterate over <ITEM> elements (each payer)
            for item in root.findall('.//DS_DPHS/ITEM'):
                try:
                    # Extract fields from XML with safety checks
                    ic_dph = item.find('IC_DPH').text if item.find('IC_DPH') is not None else None
                    ico = item.find('ICO').text if item.find('ICO') is not None else None
                    nazov_ds = item.find('NAZOV_DS').text if item.find('NAZOV_DS') is not None else None
                    obec = item.find('OBEC').text if item.find('OBEC') is not None else None
                    psc = item.find('PSC').text if item.find('PSC') is not None else None
                    ulica_cislo = item.find('ULICA_CISLO').text if item.find('ULICA_CISLO') is not None else None
                    stat = item.find('STAT').text if item.find('STAT') is not None else None
                    druh_reg_dph = item.find('DRUH_REG_DPH').text if item.find('DRUH_REG_DPH') is not None else None
                    
                    # Parse and convert date fields
                    datum_reg = item.find('DATUM_REG').text if item.find('DATUM_REG') is not None else None
                    datum_zmeny_druhu_reg = item.find('DATUM_ZMENY_DRUHU_REG').text if item.find('DATUM_ZMENY_DRUHU_REG') is not None else None

                    # Convert date formats
                    try:
                        if datum_reg:
                            datum_reg = datetime.strptime(datum_reg, '%d.%m.%Y').strftime('%Y-%m-%d')
                        if datum_zmeny_druhu_reg:
                            datum_zmeny_druhu_reg = datetime.strptime(datum_zmeny_druhu_reg, '%d.%m.%Y').strftime('%Y-%m-%d')
                    except ValueError as e:
                        logging.error(f"Invalid date format in payer element: {e}")
                        continue

                    # Log the extracted values for debugging
                    logging.info(f'Extracted: {ic_dph}, {ico}, {nazov_ds}, {obec}, {psc}, {ulica_cislo}, {stat}, {druh_reg_dph}, {datum_reg}, {datum_zmeny_druhu_reg}')

                    # Save to the database even if some fields are missing, as long as DatumAktualizacieZoznamu is present
                    Vat_payer.objects.create(
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

                except Exception as e:
                    logging.error("Error processing payer element: %s", str(e))

        logging.info("All payers processed")
        return redirect('vat_payer')

    except requests.exceptions.RequestException as e:
        logging.error("Failed to download or process the file: %s", str(e))
        return redirect('vat_payer')

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

        return redirect('vat_payer')

    except requests.exceptions.RequestException as e:
        logging.error("Failed to download or process the file: %s", str(e))
        return redirect('vat_payer')

def get_vat_payers(request):
    if request.method == 'GET':
        vat_payers = Vat_payer.objects.all().values(
            'NAZOV_DS', 'ICO', 'IC_DPH', 'OBEC', 'PSC', 'ULICA_CISLO', 'STAT', 'DRUH_REG_DPH', 'DATUM_REG', 'DATUM_ZMENY_DRUHU_REG'
        )
        return JsonResponse({'rows': list(vat_payers)})







    

            




