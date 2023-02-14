from django.shortcuts import render
import psycopg2
from psycopg2 import Error
from django.http import JsonResponse
import os
import json 
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from django.contrib.gis.geos import GEOSGeometry
from .models import Mydata
from django.contrib.gis.db import models
# Create your views here.
from django.db import connection
from django.conf import settings

def homee(request):
    global connection
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user="postgres",
                                      password="lakshay",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="lakshay")

    # Create a cursor to perform database operations
        cursor = connection.cursor()
    # Executing a SQL query
        cursor.execute("select  nward.*,n.geom from nward_waste_data as nward inner join  nwardsql as n on nward.geom_id=n.id")
        data = cursor.fetchall()
        # print(data)
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    # data = {'key': 'value'}
    # context=JsonResponse(data, safe=False)
    # js_data = simplejson.dumps(data)
   
    model_dict = model_to_dict(data)
    js_data=json.dumps(model_dict, cls=DjangoJSONEncoder)
    render_template_to_response("index.html", {"my_data": js_data})
    # return render(request, 'index.html',{'data': context})

def home(request):

    
    with connection.cursor() as cursor:
        cursor.execute("SELECT ST_AsGeoJSON(t.id,t.population,t.date,t.) FROM new_data AS t")
        data = cursor.fetchall()
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": json.loads(entry[0])
            }
            for entry in data
            ]
        }

    with open("myfile.js", "w") as f:
        f.write("export const mydata =")
        f.write(json.dumps(geojson, indent=4))
    return render(request,'index.html')


# Working Code For Generating geojson data from json (current on default view )
def data_view(request):

   with connection.cursor() as cursor:
    cursor.execute("SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' AS type, array_to_json(array_agg(f)) AS features FROM ( SELECT 'Feature' AS type, ST_AsGeoJSON(NULL)::json AS geometry, row_to_json((SELECT l FROM (SELECT ward_id, ward_date, total_waste, dry_waste, wet_waste, weight) AS l)) AS properties FROM public.ward_data ) AS f ) AS fc;")
    result = cursor.fetchone()[0]
    cursor.close()
    connection.close()
   
    with open('static/js/data/dynamic.js', 'w') as f:
     f.write('export const mydata = ')
     json.dump(result, f)
     f.write(';')
   return render(request,'index.html')


   
