import os
import qrcode

from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse

from core import settings
from core.connections import qr_drive


def create_qr_code(short_code: str, *, qr_type: str = 'png'):
    try:
        qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5)
        
        qr.add_data(f"{settings.APP_URL}/{short_code}")
        
        qr.make(fit=True)
        
        img = qr.make_image(fill='black', back_color='white')
        
        img.save(os.path.join('/tmp', f'{short_code}.{qr_type}'))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error creating new QR Code.")
    
def upload_qr_code(short_code: str):
    try:
        
        with open(os.path.join('/tmp', f'{short_code}.png'), 'rb') as f:
            qr_drive.put(f'{short_code}.png', f)
        
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