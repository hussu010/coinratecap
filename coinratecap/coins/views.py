from django.shortcuts import render
from django.http import HttpResponse
import requests
from datetime import datetime
# Create your views here.

def home(request):

    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=true&price_change_percentage=1h%2C24h%2C7d"

    r = requests.get(url).json()

    final_list = []

    for x in range(100): 
        last_updated = r[x]['last_updated']
        readable_date = datetime.fromisoformat(last_updated[:-1])
        data = {
            'id' : r[x]['id'],
            'symbol': r[x]['symbol'],
            'name': r[x]['name'],
            'image' : r[x]['image'],
            'current_price' : r[x]['current_price'],
            'market_cap_rank' : r[x]['market_cap_rank'],
            'price_change_percentage_1h_in_currency' : r[x]['price_change_percentage_1h_in_currency'],
            'price_change_percentage_24h_in_currency' : r[x]['price_change_percentage_24h_in_currency'],
            'price_change_percentage_7d_in_currency' : r[x]['price_change_percentage_7d_in_currency'],
            'market_cap' : r[x]['market_cap'],
            'total_volume' : r[x]['total_volume'],
            'sparkline_in_7d' : r[x]['sparkline_in_7d']['price'],
            'last_updated' : readable_date
        }
        final_list.append(data)
    
    context = {
        'final_list' : final_list
    }

    return render(request, 'home.html', context)