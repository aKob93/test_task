# -*- coding: utf-8 -*-
import top.api
import xml.etree.ElementTree as etree

APP_KEY = ''
APP_SECRET = ''
SESSION_KEY = ''
URL = ''
PORT = ''
FILE_HANDLER = 'updated_ali.xml'

tree = etree.parse(FILE_HANDLER)
root = tree.getroot()


def sender_request(quantities_sender, prices_sender):
    # обновление остатков
    req = top.api.AliexpressSolutionBatchProductInventoryUpdateRequest(URL, PORT)
    req.set_app_info(top.appinfo(APP_KEY, APP_SECRET))

    req.mutiple_product_update_list = quantities_sender
    try:
        resp = req.getResponse(SESSION_KEY)
        print(resp)
    except Exception, e:
        print(e)

    # обновление прайса
    req = top.api.AliexpressSolutionBatchProductPriceUpdateRequest(URL, PORT)
    req.set_app_info(top.appinfo(APP_KEY, APP_SECRET))

    req.mutiple_product_update_list = prices_sender
    try:
        resp = req.getResponse(SESSION_KEY)
        print(resp)
    except Exception, e:
        print(e)


def handler_price_and_quantity():
    quantities = []
    prices = []
    score = 0

    for offer_atr in root.iter('offer'):
        updating_quantity = {"product_id": '', "multiple_sku_update_list": [
            {"sku_code": '', "inventory": ''}]}
        update_price = {"product_id": '', "multiple_sku_update_list": [
            {"price": '', "sku_code": ''}]}

        if score == 20:  # В документации указано -
            # "В одном запросе можно обновить не более 20 товаров и не более 200 артикулов в каждом товаре."
            sender_request(quantities_sender=quantities, prices_sender=prices)
            quantities = []
            prices = []
            score = 0

        try:
            for tage in offer_atr:
                if tage.tag == 'price':
                    update_price["multiple_sku_update_list"][0]['price'] = tage.text
                    update_price['product_id'] = offer_atr.attrib['ae_intim4_id']
                    prices.append(update_price)

                if tage.tag == 'quantity':
                    updating_quantity["multiple_sku_update_list"][0]['inventory'] = tage.text
                    updating_quantity['product_id'] = offer_atr.attrib['ae_intim4_id']
                    quantities.append(updating_quantity)
            score += 1
        except Exception:
            continue


def main():
    handler_price_and_quantity()


if __name__ == '__main__':
    main()
