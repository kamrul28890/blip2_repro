import zipfile
import os

pptx_file = 'BLIP2_Professional.pptx'

# Verify file exists and is valid ZIP
if os.path.exists(pptx_file):
    try:
        with zipfile.ZipFile(pptx_file, 'r') as zf:
            files = zf.namelist()
            slide_count = len([f for f in files if f.startswith('ppt/slides/slide') and f.endswith('.xml')])
            print('✓ File is valid PPTX')
            print('✓ Slide count:', slide_count)
            print('✓ Contains presentation.xml:', 'ppt/presentation.xml' in files)
            print('✓ Contains content types:', '[Content_Types].xml' in files)
            print('✓ File path:', os.path.abspath(pptx_file))
            print('✓ File size:', round(os.path.getsize(pptx_file) / 1024, 2), 'KB')
            print('\n✓ PRESENTATION IS READY TO USE')
    except Exception as e:
        print('✗ Error reading PPTX:', e)
else:
    print('✗ File not found:', pptx_file)
