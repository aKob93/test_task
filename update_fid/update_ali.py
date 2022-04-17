# -*- coding: utf-8 -*-
from lxml import etree
import requests

FILE_VENDOR = 'http://stripmag.ru/datafeed/p5s_full_stock.xml'
FILE_PROCESSING = 'http://alitair.1gb.ru/Intim_Ali_allfids_2.xml'


# создание xml для обработки
tree_file = etree.parse(FILE_PROCESSING)
tree_file.write('ali.xml')


def processing_data_from_vendor(file_vendor):
    get_xml = requests.get(file_vendor)  # xml поставщика
    xml_vendor = get_xml.content
    parser = etree.XMLParser()
    root_vendor = etree.fromstring(xml_vendor, parser)

    prod_ids = []
    prices = []
    quantities = []

    for elem in root_vendor.iter('product'):
        prod_id = elem.attrib  # айди продукта
        id = prod_id['prodID']
        prod_ids.append(id)

    for elem in root_vendor.iter('price'):
        price = elem.attrib  # цены
        prices.append(price)

    for elem in root_vendor.iter('assortiment'):
        for sklad_attr in elem:
            sklad = sklad_attr.attrib['sklad']  # остатки
            quantities.append({'quantity': sklad})

    data_xml = zip(prod_ids, prices, quantities)
    data_xml = tuple(data_xml)
    return data_xml


def updating_data(file_update):
    tree = etree.parse(file_update)
    root = tree.getroot()
    data_xml = processing_data_from_vendor(FILE_VENDOR)

    for data in data_xml:
        for offer_attr in root.iter('offer'):
            if offer_attr.attrib['id'] == data[0]:
                for child in offer_attr:
                    if child.tag == 'price':
                        child.attrib['BaseRetailPrice'] = data[1]['RetailPrice']
                        child.attrib['BaseWholePrice'] = data[1]['BaseRetailPrice']
                        child.attrib['RetailPrice'] = data[1]['RetailPrice']
                        child.attrib['WholePrice'] = data[1]['WholePrice']
                    if child.tag == 'quantity':
                        child.text = data[2]['quantity']
    tree.write('updated_ali.xml')


def main():
    updating_data('ali.xml')


if __name__ == '__main__':
    main()
