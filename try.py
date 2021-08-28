from accounts.models import District,Province,Sector
import requests

url = "https://rwanda.p.rapidapi.com/sectors"
header={
    'x-rapidapi-key': "622de9c311msh423bbedf645954dp180485jsn7293b6a3194d",
    'x-rapidapi-host': "rwanda.p.rapidapi.com"
}
query={
    "p":"east",
    "d":"nyagatare"
}
r=requests.get(url,headers=header,params=query)
sectors=r.json()
print(sectors)

for sector in sectors['data']:
    Sector.objects.create(name=sector,district_id=4)




