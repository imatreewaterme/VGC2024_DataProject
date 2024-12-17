import requests

r = requests.get('https://www.nimbasacitypost.com/2024/08/world-championships-2024.html')
with open("vgcData.html", "w") as f:
    f.write(r.text)
