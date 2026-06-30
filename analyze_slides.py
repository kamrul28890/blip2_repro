#!/usr/bin/env python3
"""Analyze reference presentations to understand their design"""

import zipfile
import os

def analyze_pptx(filename):
    """Extract and analyze structure of a PPTX file"""
    try:
        with zipfile.ZipFile(filename, 'r') as zf:
            slide_files = sorted([f for f in zf.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')])
            print(f"\n📊 {os.path.basename(filename)}")
            print(f"   Total slides: {len(slide_files)}")
            
            # Examine structure of a few slides
            for slide_idx, slide_file in enumerate(slide_files[:3]):
                with zf.open(slide_file) as f:
                    content = f.read().decode('utf-8', errors='ignore')
                    
                    # Count different elements
                    shapes = content.count('<p:sp>')
                    text_elements = content.count('<a:t>')
                    tables = content.count('<p:table>')
                    images = content.count('<p:pic>')
                    
                    print(f"   Slide {slide_idx+1}: {shapes} shapes, {text_elements} text, {tables} tables, {images} images")
                    
                    # Check for specific formatting
                    if 'srgbClr' in content:
                        # Extract some colors mentioned
                        import re
                        colors = re.findall(r'srgbClr val="([A-F0-9]{6})"', content)
                        if colors:
                            print(f"     Colors: {list(set(colors[:3]))}")
    except Exception as e:
        print(f"   Error: {e}")

# Analyze reference presentations
reference_files = [
    "Slides/BLIP-2_Multimodal_Bootstrapping.pptx",
    "Slides/VisionLLM_v2_Multimodal_Generalist.pptx",
    "Slides/Visual_Instruction_Tuning.pptx"
]

for ref_file in reference_files:
    if os.path.exists(ref_file):
        analyze_pptx(ref_file)
    else:
        print(f"✗ {ref_file} not found")

print("\n✓ Analysis complete")
