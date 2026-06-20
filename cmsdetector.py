#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import re
from urllib.parse import urlparse
import sys
from colorama import init, Fore, Style

init(autoreset=True)

#############################################################################################
### CMS Detector
#############################################################################################
# ==================== CMS SIGNATURES ====================
CMS_SIGNATURES = {
    "WordPress": [
        r'/wp-content/', r'/wp-includes/', r'wp-.*\.php',
        r'meta name="generator" content="WordPress',
        r'content="WordPress'
    ],
    "Joomla": [
        r'/administrator/', r'/components/com_',
        r'meta name="generator" content="Joomla!',
        r'Joomla!'
    ],
    "Drupal": [
        r'/sites/default/files/', r'Drupal.settings',
        r'meta name="Generator" content="Drupal',
        r'Drupal'
    ],
    "Shopify": [
        r'cdn.shopify.com', r'Shopify.theme',
        r'checkout.shopify.com'
    ],
    "Magento": [
        r'/skin/frontend/', r'/js/mage/',
        r'meta name="generator" content="Magento'
    ],
    "PrestaShop": [
        r'/img/.*prestashop', r'PrestaShop',
        r'meta name="generator" content="PrestaShop'
    ],
    "Wix": [
        r'wix.com', r'Wix.com'
    ],
    "Squarespace": [
        r'squarespace.com', r'Squarespace'
    ],
    "Ghost": [
        r'ghost-platform', r'Ghost'
    ],
    "Blogger": [
        r'blogspot.com', r'blogger'
    ],
    "Webflow": [
        r'webflow.com', r'data-wf-', r'cdn.prod.website-files.com',
        r'meta content="Webflow" name="generator',
        r'<!-- This site was created in Webflow'
    ],
    "Weebly": [
        r'weebly.com', r'weebly-site.com',
        r'meta name="generator" content="Weebly'
    ],
    "TYPO3": [
        r'typo3', r'/typo3temp/', r'/typo3conf/',
        r'TYPO3', r'meta name="generator" content="TYPO3'
    ],
    "Bitrix": [
        r'bitrix', r'/bitrix/', r'BX_',
        r'Bitrix', r'meta name="generator" content="Bitrix'
    ],
    "OpenCart": [
        r'opencart', r'/catalog/view/theme/', r'OpenCart'
    ],
    "BigCommerce": [
        r'bigcommerce.com', r'static.bigcommerce.com',
        r'BigCommerce'
    ],
    "WooCommerce": [
        r'woocommerce', r'/wp-content/plugins/woocommerce/'
    ],
    "Craft_CMS": [
        r'craftcms', r'Craft CMS', r'data-craft'
    ],
    "Umbraco": [
        r'umbraco', r'/umbraco/', r'Umbraco'
    ],
    "Concrete_CMS": [
        r'concrete', r'concrete5', r'Concrete CMS'
    ],
    "HubSpot": [
        r'hubspot', r'hs-scripts.com', r'HubSpot'
    ],
    "GoDaddy": [
        r'godaddysites.com', r'GoDaddy'
    ],
    "Duda": [
        r'duda.co', r'Duda'
    ],
    "Tilda": [
        r'tilda.ws', r'Tilda'
    ],
    "Strapi": [
        r'strapi', r'Strapi'
    ],
    "Contentful": [
        r'contentful', r'Contentful'
    ],
    "Sanity": [
        r'sanity.io', r'Sanity'
    ],
    "Sitecore": [
        r'sitecore', r'Sitecore'
    ],
    "Kentico": [r'kentico', r'Kentico'],
    "Magnolia": [r'magnolia', r'Magnolia CMS'],
    "Liferay": [r'liferay', r'Liferay'],
    "Alfresco": [r'alfresco', r'Alfresco'],
    "Backbone": [r'backbone', r'Backbone.js'],
}

def get_domain(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

def detect_cms(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/128.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        content = response.text.lower()
        final_url = response.url

        print(Fore.CYAN + f"\n🔍 Analyzing: {final_url}")
        print(Fore.CYAN + f"Status Code: {response.status_code}\n")

        detected = []

        # Έλεγχος signatures
        for cms, signatures in CMS_SIGNATURES.items():
            for sig in signatures:
                if re.search(sig.lower(), content):
                    detected.append(cms)
                    break

        # Ειδικοί έλεγχοι
        if 'wordpress' in content or '/wp-' in content:
            detected.append("WordPress")
        if 'wp-content' in content:
            detected.append("WordPress")

        # Αφαίρεση διπλοτύπων
        detected = list(dict.fromkeys(detected))

        if detected:
            print(Fore.GREEN + f"✅ CMS Detected: {', '.join(detected)}")
            return detected[0]
        else:
            print(Fore.YELLOW + "⚠️  Could not detect CMS (Unknown or custom)")
            return "Unknown"

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"❌ Connection Error: {e}")
        return None
    except Exception as e:
        print(Fore.RED + f"❌ Error: {e}")
        return None


# ===================== MAIN =====================
if __name__ == "__main__":
    print(Fore.MAGENTA + Style.BRIGHT + """
    ╔══════════════════════════════════════════════╗
    ║           CMS Detector v1.0                  ║
    ║          Powered by SourceCode347            ║
    ╚══════════════════════════════════════════════╝
    """)

    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = input(Fore.WHITE + "🌐 Enter website URL: ").strip()

    detect_cms(get_domain(target))