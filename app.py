import json
import joblib
import pandas as pd
import os

# Modeli konteyner içinden (aynı dizinden) direkt yüklüyoruz
MODEL_PATH = os.path.join(os.path.dirname(__file__), "real_estate_model.joblib")
MODEL_CACHE = joblib.load(MODEL_PATH)

def handler(event, context):
    try:
        # API Gateway'den gelebilecek tüm farklı veri yapılarını (string, dict vb.) garantiye alıyoruz
        body = None
        
        if isinstance(event, dict) and "body" in event and isinstance(event["body"], str):
            try:
                body = json.loads(event["body"])
            except:
                pass
                
        if body is None and isinstance(event, dict) and "body" in event and isinstance(event["body"], dict):
            body = event["body"]
            
        if body is None and isinstance(event, dict):
            body = event
            
        if body is None and isinstance(event, str):
            try:
                body = json.loads(event)
            except:
                pass

        if body is None:
            raise Exception(f"Gelen veri yapısı çözülemedi! Veri tipi: {str(type(event))}")

        # Parametrelerin varlığını esnek bir şekilde kontrol ediyoruz
        t_date = body.get("transaction_date") or body.get("X1 transaction date")
        h_age = body.get("house_age") or body.get("X2 house age")
        d_mrt = body.get("distance_to_mrt") or body.get("X3 distance to the nearest MRT station")
        c_stores = body.get("convenience_stores") or body.get("X4 number of convenience stores")
        lat = body.get("latitude") or body.get("X5 latitude")
        lng = body.get("longitude") or body.get("X6 longitude")

        if None in [t_date, h_age, d_mrt, c_stores, lat, lng]:
            raise Exception(f"Eksik parametre tespit edildi! Gönderilen veri: {str(body)}")

        # Modelin eğiltildiği orijinal Pandas DataFrame yapısını oluşturuyoruz
        feature_vector = {
            "X1 transaction date": [float(t_date)],
            "X2 house age": [float(h_age)],
            "X3 distance to the nearest MRT station": [float(d_mrt)],
            "X4 number of convenience stores": [int(c_stores)],
            "X5 latitude": [float(lat)],
            "X6 longitude": [float(lng)]
        }
        
        input_df = pd.DataFrame(feature_vector)
        predicted_price = MODEL_CACHE.predict(input_df)[0]
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "status": "success",
                "predicted_unit_price": round(float(predicted_price), 4),
                "engine": "AWS Lambda Autonomous Docker Container"
            })
        }
    except Exception as e:
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "status": "kod_hatasi",
                "detay": str(e),
                "gelen_veri_ozeti": str(event)[:300]
            })
        }