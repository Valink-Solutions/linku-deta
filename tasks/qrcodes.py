import os
import shutil
import qrcode

from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse

from core import settings
from core.connections import qr_drive, settings_db


def create_qr_code(short_code: str, *, qr_type: str = 'png'):
    try:
        qr = qrcode.QRCode(
                version=2,
                box_size=10,
                border=5)
        
        APP_URL = settings_db.get('APP_URL')
        
        if APP_URL.get('APP_URL'):
            
            qr.add_data(f"{APP_URL.get('APP_URL')}/{short_code}")
            
            qr.make(fit=True)
            
            img = qr.make_image(fill='black', back_color='white')
            
            img.save(os.path.join('/tmp', f'{short_code}.{qr_type}'))
            
        else:
            raise HTTPException(status_code=500, detail="APP_URL not set (POST /settings.)")
            
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error creating new QR Code.")
    
def upload_qr_code(short_code: str):
    try:
        
        with open(os.path.join('/tmp', f'{short_code}.png'), 'rb') as f:
            qr_drive.put(f'{short_code}.png', f)
            
        os.remove(os.path.join('/tmp', f'{short_code}.png'))
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error uploading new QR Code.")
    
def delete_qr_code(short_code: str):
    try:
        
        qr_drive.delete(f'{short_code}.png')
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Could not find and delete QR Code.")
    

def get_qr_code(short_code: str):
    try:
        res = qr_drive.get(f'{short_code}.png')
        return StreamingResponse(res.iter_chunks(1024), media_type="image/png")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Could not find and get QR Code.")