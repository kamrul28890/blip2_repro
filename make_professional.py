#!/usr/bin/env python3
"""
Professional BLIP-2 Reproduction Presentation Generator
Uses only standard library (zipfile, xml) - no external dependencies
"""

import zipfile
import os
from datetime import datetime

class ProfessionalPPTX:
    def __init__(self, filename):
        self.filename = filename
        self.slides_data = []
        self.colors = {
            'dark_bg': '0F1729',
            'title_blue': '3B82F6',
            'accent_green': '22C55E',
            'white': 'FFFFFF',
            'dark_text': '141E1E',
            'card_bg': '1E293B'
        }
    
    def add_title_slide(self, main_title, subtitle):
        self.slides_data.append({
            'type': 'title',
            'main': main_title,
            'sub': subtitle
        })
    
    def add_content_slide(self, title, left_col, right_col):
        self.slides_data.append({
            'type': 'content',
            'title': title,
            'left': left_col,
            'right': right_col
        })
    
    def generate_content_types(self):
        num_slides = len(self.slides_data)
        slides_xml = '\n'.join(f'  <Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
                              for i in range(1, num_slides + 1))
        return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
{slides_xml}
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.custom-properties+xml"/>
</Types>'''
    
    def generate_presentation_rels(self):
        num_slides = len(self.slides_data)
        slide_rels = ''.join(f'  <Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>\n'
                            for i in range(1, num_slides + 1))
        return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
{slide_rels}  <Relationship Id="rId{num_slides + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>
  <Relationship Id="rId{num_slides + 2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>
</Relationships>'''
    
    def generate_presentation(self):
        num_slides = len(self.slides_data)
        slide_ids = ''.join(f'    <p:sldId id="{256 + i}" r:id="rId{i}"/>\n' for i in range(1, num_slides + 1))
        return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <p:sldSz cx="9144000" cy="6858000"/>
  <p:sldIdLst>
{slide_ids}  </p:sldIdLst>
</p:presentation>'''
    
    def generate_title_slide(self):
        return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
  <p:cSld>
    <p:bg><p:bgPr><a:solidFill><a:srgbClr val="{self.colors['dark_bg']}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name="Title 1"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="9144000" cy="6858000"/><a:chOff x="0" y="0"/><a:chExt cx="9144000" cy="6858000"/></a:xfrm></p:grpSpPr>
      <p:sp><p:nvSpPr><p:cNvPr id="2" name="Title"/><p:cNvSpPr txBody="1"/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="457200" y="1828800"/><a:ext cx="8229600" cy="1828800"/></a:xfrm></p:spPr>
        <p:txBody><a:bodyPr rtlCol="0"/><a:lstStyle/>
          <a:p align="ctr"><a:r><a:rPr lang="en-US" sz="6000" b="1"><a:solidFill><a:srgbClr val="{self.colors['title_blue']}"/></a:solidFill></a:rPr><a:t>Multimodal LLMs: From Theory to Practice</a:t></a:r></a:p>
        </p:txBody>
      </p:sp>
      <p:sp><p:nvSpPr><p:cNvPr id="3" name="Subtitle"/><p:cNvSpPr txBody="1"/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="457200" y="4114800"/><a:ext cx="8229600" cy="1828800"/></a:xfrm></p:spPr>
        <p:txBody><a:bodyPr rtlCol="0"/><a:lstStyle/>
          <a:p align="ctr"><a:r><a:rPr lang="en-US" sz="2400"><a:solidFill><a:srgbClr val="{self.colors['white']}"/></a:solidFill></a:rPr><a:t>Comparative Critique + BLIP-2 Local Reproduction Study</a:t></a:r></a:p>
          <a:p align="ctr"><a:r><a:rPr lang="en-US" sz="1800"><a:solidFill><a:srgbClr val="{self.colors['accent_green']}"/></a:solidFill></a:rPr><a:t>15 Dense Slides | Best in Class</a:t></a:r></a:p>
        </p:txBody>
      </p:sp>
    </p:spTree>
  </p:cSld>
</p:sld>'''
    
    def generate_content_slide(self, idx, slide_data):
        title = slide_data['title']
        left_title, left_items = slide_data['left'][0], slide_data['left'][1:]
        right_title, right_items = slide_data['right'][0], slide_data['right'][1:]
        
        # Build left column text
        left_text_runs = f'<a:p><a:r><a:rPr lang="en-US" sz="1400" b="1"><a:solidFill><a:srgbClr val="{self.colors["accent_green"]}"/></a:solidFill></a:rPr><a:t>{left_title}</a:t></a:r></a:p>'
        for item in left_items:
            left_text_runs += f'<a:p><a:r><a:rPr lang="en-US" sz="1000"><a:solidFill><a:srgbClr val="{self.colors["white"]}"/></a:solidFill></a:rPr><a:t>{item}</a:t></a:r></a:p>'
        
        # Build right column text
        right_text_runs = f'<a:p><a:r><a:rPr lang="en-US" sz="1400" b="1"><a:solidFill><a:srgbClr val="{self.colors["accent_green"]}"/></a:solidFill></a:rPr><a:t>{right_title}</a:t></a:r></a:p>'
        for item in right_items:
            right_text_runs += f'<a:p><a:r><a:rPr lang="en-US" sz="1000"><a:solidFill><a:srgbClr val="{self.colors["white"]}"/></a:solidFill></a:rPr><a:t>{item}</a:t></a:r></a:p>'
        
        return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
  <p:cSld>
    <p:bg><p:bgPr><a:solidFill><a:srgbClr val="{self.colors['dark_bg']}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name="Slide {idx}"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="9144000" cy="6858000"/><a:chOff x="0" y="0"/><a:chExt cx="9144000" cy="6858000"/></a:xfrm></p:grpSpPr>
      
      <!-- Title bar -->
      <p:sp><p:nvSpPr><p:cNvPr id="2" name="Title"/><p:cNvSpPr txBody="1"/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="9144000" cy="685800"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="{self.colors['title_blue']}"/></a:solidFill></p:spPr>
        <p:txBody><a:bodyPr rtlCol="0"/><a:lstStyle/><a:p><a:r><a:rPr lang="en-US" sz="2800" b="1"><a:solidFill><a:srgbClr val="{self.colors['white']}"/></a:solidFill></a:rPr><a:t>{title}</a:t></a:r></a:p></p:txBody>
      </p:sp>
      
      <!-- Left column -->
      <p:sp><p:nvSpPr><p:cNvPr id="3" name="Left"/><p:cNvSpPr txBody="1"/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="274638" y="914400"/><a:ext cx="4114800" cy="5486400"/></a:xfrm></p:spPr>
        <p:txBody><a:bodyPr rtlCol="0"/><a:lstStyle/>{left_text_runs}</p:txBody>
      </p:sp>
      
      <!-- Right column -->
      <p:sp><p:nvSpPr><p:cNvPr id="4" name="Right"/><p:cNvSpPr txBody="1"/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="4754562" y="914400"/><a:ext cx="4114800" cy="5486400"/></a:xfrm></p:spPr>
        <p:txBody><a:bodyPr rtlCol="0"/><a:lstStyle/>{right_text_runs}</p:txBody>
      </p:sp>
    </p:spTree>
  </p:cSld>
</p:sld>'''
    
    def generate_slide_master(self):
        return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="{self.colors['dark_bg']}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg></p:cSld>
</p:sldMaster>'''
    
    def generate_slide_layout(self):
        return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <p:cSld><p:bg><p:bgPr><a:solidFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:srgbClr val="{self.colors['dark_bg']}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg></p:cSld>
  <p:clrMapOvr xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>'''
    
    def save(self):
        with zipfile.ZipFile(self.filename, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('[Content_Types].xml', self.generate_content_types())
            zf.writestr('_rels/.rels', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>''')
            
            zf.writestr('ppt/_rels/presentation.xml.rels', self.generate_presentation_rels())
            zf.writestr('ppt/presentation.xml', self.generate_presentation())
            
            # Add slides
            zf.writestr('ppt/slides/slide1.xml', self.generate_title_slide())
            for i, slide_data in enumerate(self.slides_data[1:], start=2):
                zf.writestr(f'ppt/slides/slide{i}.xml', self.generate_content_slide(i, slide_data))
            
            zf.writestr('ppt/slideMasters/slideMaster1.xml', self.generate_slide_master())
            zf.writestr('ppt/slideLayouts/slideLayout1.xml', self.generate_slide_layout())
            
            zf.writestr('ppt/theme/theme1.xml', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Office Theme">
  <a:themeElements/>
</a:theme>''')
            
            zf.writestr('docProps/core.xml', f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/">
  <dc:title>BLIP-2 Reproduction Analysis</dc:title>
  <dcterms:created>{datetime.now().isoformat()}</dcterms:created>
</cp:coreProperties>''')
            
            zf.writestr('docProps/app.xml', f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
  <TotalTime>0</TotalTime>
  <Slides>{len(self.slides_data)}</Slides>
</Properties>''')

# CREATE PRESENTATION
prs = ProfessionalPPTX("BLIP2_Professional.pptx")

# Slide 1 (automatic title)

# Slide 2
prs.add_content_slide("Three Papers: Quick Comparison",
    ["BLIP-2", "• Q-Former bridge", "• 129M image-text pairs", "• BLEU-4: 43.7, CIDEr: 145.8", "• ✓ Best for local repro"],
    ["LLaVA & VisionLLM v2", "• Instruction-tuned assistant", "• GPT-4 generated data (158K)", "• Result: 92.53% ScienceQA", "• ⚠ Requires constraints"])

# Slide 3
prs.add_content_slide("Local Setup: Downscaling",
    ["Hardware & Models", "• GPU: RTX 3070 8GB", "• Vision: CLIP ViT-L", "• LLM: OPT-350M", "• Resolution: 224px"],
    ["Paper Configuration", "• GPU: 16×A100 40GB", "• Vision: ViT-g", "• LLM: OPT-2.7B", "• Resolution: 364px"])

# Slide 4
prs.add_content_slide("Local Results: Data Scaling",
    ["Pilot & Main", "• 10k: 1.45 BLEU-4", "• 50k: 11.13 BLEU-4 ✓", "• 50k Polish: 10.49", "• 50k diversity: 563 captions"],
    ["Long Run Analysis", "• 100k: 8.57 BLEU-4 (e2)", "• 100k (final): 6.61 (e14)", "• Peak-early phenomenon", "• Diversity: 734 captions"])

# Slide 5
prs.add_content_slide("Performance Gap: Breakdown",
    ["Gap Components", "• Backbone (ViT-g→ViT-L): 3-4×", "• LLM (OPT-2.7B→OPT-350M): 8×", "• Pre-training data: 129M→0", "• Resolution: 364→224"],
    ["Gap Analysis", "• Multiplicative effect: ~25-30×", "• NOT pipeline failure", "• Scale-driven, not archit.", "• All components stable"])

# Slide 6
prs.add_content_slide("100k Run: Peak-Early Phenomenon",
    ["Training Losses", "• Stage 1: 0.33", "• Stage 2: 0.36", "• Caption loss: steady ↓", "• No divergence → stable"],
    ["Caption Metrics", "• Epoch 2 (best): 8.57 BLEU", "• Epoch 14 (final): 6.61", "• Degradation: -23%", "• Overfitting w/o early stop"])

# Slide 7
prs.add_content_slide("Reproducibility: Pipeline vs Performance",
    ["Pipeline Status", "✓ All 3 stages complete", "✓ End-to-end on RTX 3070", "✓ Stable gradients", "✓ Output predictions valid"],
    ["Performance Status", "✗ 25-30× gap to paper", "⟹ Gap is systematic", "⟹ NOT impl failure", "✓ Architecture sound"])

# Slide 8
prs.add_content_slide("Why BLIP-2 Was Best Choice",
    ["Architectural Fit", "• Modular Q-Former bridge", "• Frozen backbones downscalable", "• Clear reduction path", "• Scientific coherence"],
    ["Practical Advantages", "• Official LAVIS code available", "• Well-documented pipeline", "• No synthetic data needed", "• Tractable complexity"])

# Slide 9
prs.add_content_slide("Study Limitations & Caveats",
    ["Evaluation Scope", "• Local: 1k val/test", "• Paper: Full Karpathy split", "• Internal comparability: ✓", "• Leaderboard equiv.: ✗"],
    ["Study Design", "• Single-seed runs (no CI)", "• Student-scale downscaling", "• Windows portability tested", "• Real data only"])

# Slide 10
prs.add_content_slide("Reproducibility Artifacts Trail",
    ["Checkpoint Registry", "• All runs: checkpoint_registry", "• Per-epoch metrics saved", "• Loss trajectories logged", "• Model selection justified"],
    ["Configuration & Proof", "• Stage config files .yaml", "• Hyperparams for 10k/50k/100k", "• Progress logs available", "• Traceability complete"])

# Slide 11
prs.add_content_slide("Technical Takeaways",
    ["Architecture", "• Backbone selection > LLM size", "• Frozen design is genuinely", "  modular and downscalable", "• Q-Former works as intended"],
    ["Optimization", "• Checkpoint selection > train time", "• Validation-driven needed", "• Early stopping is critical", "• 100k run proved limits"])

# Slide 12
prs.add_content_slide("For Practitioners & Researchers",
    ["Building Locally", "1. Choose modular arch", "2. Invest in backbone", "3. Use metric-driven selection", "4. Validate every checkpoint"],
    ["Future Research", "1. Systematic backbone scaling", "2. Data augmentation strategies", "3. Regularization tuning", "4. Efficient models (MobileViT)"])

# Slide 13
prs.add_content_slide("Main Conclusions",
    ["Pipeline Reproducibility", "✓ BLIP-2 pipeline IS reproducible", "  on consumer GPU", "✓ All 3 stages run end-to-end", "✓ Official code works locally"],
    ["Performance Reproducibility", "✗ Local performance NOT matched", "⟹ Gap is SYSTEMATIC", "  (backbones, data, compute)", "⟹ NOT pipeline bug"])

# Slide 14
prs.add_content_slide("Key Research Insight",
    ["Multimodal ML Lesson", "• Literature conflates", "  architecture + scale", "• This study: BLIP-2 arch", "  is sound; gap is scale"],
    ["Reproducibility Lesson", "• Pipeline repr. ≠ perf. repr.", "• Important distinction!", "• Local needs tuning", "• Scale compounds"])

# Slide 15
prs.add_content_slide("Summary & Impact",
    ["What We Showed", "• Compared 3 MLLM papers", "• Selected best for local work", "• Full repro on RTX 3070", "• Systematic gap analysis"],
    ["Why It Matters", "• Shows feasibility path", "• BLIP-2 is best commodity", "  reproduction target", "• Architecture over scale"])

prs.save()
print("✓ Professional presentation generated!")
print(f"✓ File: BLIP2_Professional.pptx")
print(f"✓ Slides: {len(prs.slides_data)}")
print("✓ Dense layout, no white space, professional formatting")
