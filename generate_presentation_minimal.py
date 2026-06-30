#!/usr/bin/env python3
"""Generate BLIP-2 Reproduction Analysis presentation as PPTX"""

import zipfile
import os
import xml.etree.ElementTree as ET
from datetime import datetime

class SimplePPTXGenerator:
    """Minimal PPTX generator without external dependencies"""
    
    def __init__(self, filename="presentation.pptx"):
        self.filename = filename
        self.slides = []
        self.slide_layouts = {}
        self.relationships = {}
        self.zip = None
    
    def add_title_slide(self, title, subtitle=''):
        """Add a title slide"""
        slide_data = {
            'type': 'title',
            'title': title, 
            'subtitle': subtitle
        }
        self.slides.append(slide_data)
    
    def add_content_slide(self, title, bullets):
        """Add a content slide with bullet points"""
        slide_data = {
            'type': 'content',
            'title': title,
            'bullets': bullets
        }
        self.slides.append(slide_data)
    
    def save(self):
        """Save as PPTX file"""
        with zipfile.ZipFile(self.filename, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add required package files
            zf.writestr('[Content_Types].xml', self._get_content_types())
            zf.writestr('_rels/.rels', self._get_rels())
            zf.writestr('ppt/_rels/presentation.xml.rels', self._get_pres_rels())
            zf.writestr('ppt/presentation.xml', self._get_presentation())
            
            # Add slides
            for i, slide in enumerate(self.slides, 1):
                zf.writestr(f'ppt/slides/slide{i}.xml', self._generate_slide(i, slide))
            
            # Add slide layout
            zf.writestr('ppt/slideLayouts/slideLayout1.xml', self._get_slide_layout())
            zf.writestr('ppt/slideLayouts/_rels/slideLayout1.xml.rels', self._get_slide_layout_rels())
            
            # Add slide master
            zf.writestr('ppt/slideMasters/slideMaster1.xml', self._get_slide_master())
            zf.writestr('ppt/slideMasters/_rels/slideMaster1.xml.rels', self._get_slide_master_rels())
            
            # Add theme
            zf.writestr('ppt/theme/theme1.xml', self._get_theme())
            
            # Add docProps
            zf.writestr('docProps/core.xml', self._get_core_props())
            zf.writestr('docProps/app.xml', self._get_app_props())
        
        print(f"✓ Presentation saved: {self.filename}")
    
    def _get_content_types(self):
        return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
  <Override PartName="/ppt/slides/slide2.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
  <Override PartName="/ppt/slides/slide3.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
  <Override PartName="/ppt/slides/slide4.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
  <Override PartName="/ppt/slides/slide5.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
  <Override PartName="/ppt/slides/slide6.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
  <Override PartName="/ppt/slides/slide7.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
  <Override PartName="/ppt/slides/slide8.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
  <Override PartName="/ppt/slides/slide9.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
  <Override PartName="/ppt/slides/slide10.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
  <Override PartName="/ppt/slides/slide11.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
  <Override PartName="/ppt/slides/slide12.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
  <Override PartName="/ppt/slides/slide13.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
  <Override PartName="/ppt/slides/slide14.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
  <Override PartName="/ppt/slides/slide15.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.custom-properties+xml"/>
</Types>'''
    
    def _get_rels(self):
        return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''
    
    def _get_pres_rels(self):
        rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        rels += '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
        for i in range(1, len(self.slides) + 1):
            rels += f'  <Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>\n'
        rels += f'  <Relationship Id="rId{len(self.slides)+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="slideLayouts/slideLayout1.xml"/>\n'
        rels += f'  <Relationship Id="rId{len(self.slides)+2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>\n'
        rels += '</Relationships>'
        return rels
    
    def _get_presentation(self):
        slide_ids = '\n'.join(f'    <p:sldId id="{256+i}" r:id="rId{i}"/>' for i in range(1, len(self.slides)+1))
        return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <p:sldSz cx="9144000" cy="6858000"/>
  <p:sldIdLst>
{slide_ids}
  </p:sldIdLst>
</p:presentation>'''
    
    def _generate_slide(self, num, slide_data):
        """Generate slide XML"""
        if slide_data['type'] == 'title':
            return self._generate_title_slide_xml(slide_data)
        else:
            return self._generate_content_slide_xml(slide_data)
    
    def _generate_title_slide_xml(self, data):
        return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <p:cSld>
    <p:bg><p:bgPr><a:solidFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:srgbClr val="192D50"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name="Title 1"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:off x="0" y="0"/><a:ext cx="9144000" cy="6858000"/><a:chOff x="0" y="0"/><a:chExt cx="9144000" cy="6858000"/></a:xfrm></p:grpSpPr>
      <p:sp><p:nvSpPr><p:cNvPr id="2" name="Title"/><p:cNvSpPr txBody="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:off x="457200" y="1828800"/><a:ext cx="8229600" cy="1371600"/></a:xfrm></p:spPr><p:txBody><a:bodyPr xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" rtlCol="0"/><a:lstStyle/><a:p><a:r><a:rPr lang="en-US" sz="5400" b="1"><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></a:rPr><a:t>{data['title']}</a:t></a:r></a:p></p:txBody></p:sp>
      <p:sp><p:nvSpPr><p:cNvPr id="3" name="Subtitle"/><p:cNvSpPr txBody="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:off x="457200" y="3600000"/><a:ext cx="8229600" cy="1800000"/></a:xfrm></p:spPr><p:txBody><a:bodyPr xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" rtlCol="0"/><a:lstStyle/><a:p><a:r><a:rPr lang="en-US" sz="2800"><a:solidFill><a:srgbClr val="C8DCFF"/></a:solidFill></a:rPr><a:t>{data.get('subtitle', '')}</a:t></a:r></a:p></p:txBody></p:sp>
    </p:spTree>
  </p:cSld>
</p:sld>'''
    
    def _generate_content_slide_xml(self, data):
        """Generate content slide with bullet points"""
        bullets_xml = ''
        for i, bullet in enumerate(data['bullets']):
            level = 0 if not bullet.startswith('  ') else 1
            text = bullet.strip()
            indent = 342900 * (level + 1)
            bullets_xml += f'<a:p><a:pPr lvl="{level}" marL="{indent}"><a:buFont typeface="Calibri"/><a:buChar char="•"/></a:pPr><a:r><a:rPr lang="en-US" sz="1400"><a:solidFill><a:srgbClr val="000000"/></a:solidFill></a:rPr><a:t>{text}</a:t></a:r></a:p>'
        
        return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name="Slide 1"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:off x="0" y="0"/><a:ext cx="9144000" cy="6858000"/><a:chOff x="0" y="0"/><a:chExt cx="9144000" cy="6858000"/></a:xfrm></p:grpSpPr>
      <p:sp><p:nvSpPr><p:cNvPr id="2" name="Title"/><p:cNvSpPr txBody="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:off x="0" y="0"/><a:ext cx="9144000" cy="686400"/></a:xfrm><a:prstGeom xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" prst="rect"><a:avLst/></a:prstGeom><a:solidFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:srgbClr val="192D50"/></a:solidFill></p:spPr><p:txBody><a:bodyPr xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" rtlCol="0"/><a:lstStyle/><a:p><a:r><a:rPr lang="en-US" sz="2800" b="1"><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></a:rPr><a:t>{data['title']}</a:t></a:r></a:p></p:txBody></p:sp>
      <p:sp><p:nvSpPr><p:cNvPr id="3" name="Body"/><p:cNvSpPr txBody="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:off x="365760" y="914400"/><a:ext cx="8412480" cy="5486400"/></a:xfrm></p:spPr><p:txBody xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:bodyPr rtlCol="0"/><a:lstStyle/>{bullets_xml}</p:txBody></p:sp>
    </p:spTree>
  </p:cSld>
</p:sld>'''
    
    def _get_slide_layout(self):
        return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <p:cSld/>
</p:sldLayout>'''
    
    def _get_slide_layout_rels(self):
        return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>'''
    
    def _get_slide_master(self):
        return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <p:cSld/>
</p:sldMaster>'''
    
    def _get_slide_master_rels(self):
        return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>'''
    
    def _get_theme(self):
        return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Office">
  <a:themeElements/>
</a:theme>'''
    
    def _get_core_props(self):
        return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/">
  <dc:title>BLIP-2 Reproduction Analysis</dc:title>
  <dc:creator>User</dc:creator>
  <dcterms:created xsi:type="dcterms:W3CDTF" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">{datetime.now().isoformat()}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">{datetime.now().isoformat()}</dcterms:modified>
</cp:coreProperties>'''
    
    def _get_app_props(self):
        return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <TotalTime>0</TotalTime>
  <Slides>{len(self.slides)}</Slides>
  <Application>python</Application>
</Properties>'''

# Create presentation
prs = SimplePPTXGenerator("BLIP2_Reproduction_Analysis.pptx")

# Add all 15 slides
prs.add_title_slide(
    'Multimodal LLMs: From Theory to Practice',
    'Comparative Critique + BLIP-2 Reproduction Study'
)

prs.add_content_slide('Three Papers: Why & What', [
    '• BLIP-2 (Li et al., 2023): Q-Former bridge → frozen backbones → efficient alignment',
    '• LLaVA (Liu et al., 2023): Instruction tuning → multimodal assistants → data-centric',
    '• VisionLLM v2 (Wu et al., 2024): Multi-decoder routing → end-to-end generalist',
    '',
    'Common domain: Vision-language alignment & cross-modal understanding',
    'Key difference: Architecture complexity & supervision strategy scale',
    'Selection: BLIP-2 most suitable for local reproduction (modular, open, downscalable)'
])

prs.add_content_slide('Problem Statements', [
    'BLIP-2: Can lightweight bridge efficiently connect frozen vision & language?',
    '→ Compute-efficient multimodal learning without full retraining',
    '',
    'LLaVA: How to build practical multimodal assistants vs. captioning?',
    '→ Supervision format impact on assistant behavior',
    '',
    'VisionLLM v2: Can one system unify many vision & vision-language tasks?',
    '→ Generalist perception via shared router + task decoders',
    '',
    'Shared thread: Reuse frozen backbones, reduce training complexity'
])

prs.add_content_slide('Methodology Comparison', [
    'BLIP-2: Two-stage Q-Former (Stage1: ITC+ITM+LM; Stage2: aligned generation)',
    '  Data: 129M pairs | Compute: 16×A100 40GB, multi-day',
    '',
    'LLaVA: Lightweight projection + instruction tuning (GPT-4 generated)',
    '  Data: 158K pairs (ViT-L CLIP + Vicuna-7B) | Compute: 8×A100, ~10h',
    '',
    'VisionLLM v2: Central MLLM + super-link routing to decoders',
    '  Data: 64 datasets, ~100 tasks | Compute: 64→128 A100 GPUs, 18 days'
])

prs.add_content_slide('Results & Reproducibility', [
    'BLIP-2 | BLEU-4: 43.7, CIDEr: 145.8 | ✓ BEST LOCAL TARGET',
    '  • Frozen arch preserves coherent downscaling',
    '  • Official code available (LAVIS), no synthetic data dependency',
    '',
    'LLaVA | ScienceQA: 92.53% | ⚠ VIABLE WITH CONSTRAINTS',
    '  • Depends on GPT-4 instruction pipeline',
    '',
    'VisionLLM v2 | Broad tasks | ✗ NOT LOCAL FEASIBLE',
    '  • 64-128 A100 required, too high complexity'
])

prs.add_content_slide('Limitations Across Papers', [
    'BLIP-2: Performance tightly coupled to large backbones (ViT-g, OPT-2.7B)',
    '  → Scaling to commodity hardware unexplored',
    '',
    'LLaVA: GPT-4 instruction-data reliance introduces synthetic bias',
    '  → Reproducibility depends on pipeline quality',
    '',
    'VisionLLM v2: Multi-decoder complexity makes ablation difficult',
    '  → Gains unclear (routing? decoders? data? scale?)',
    '',
    'General: All show scale→performance coupling'
])

prs.add_content_slide('Local BLIP-2 Setup: Bridging Scale Gap', [
    'Hardware: RTX 3070 8GB (vs. 16 A100 40GB)',
    'Vision: CLIP ViT-L (vs. ViT-g); LLM: OPT-350M (vs. OPT-2.7B); Res: 224 (vs. 364)',
    '',
    'Data: COCO Karpathy subsets (10k, 50k, 100k) vs. 129M pretraining pairs',
    '  • Fixed val/test: 1k each for fidelity',
    '',
    'Pipeline stages (frozen backbone design preserved):',
    '  • Stage 1: Q-Former + frozen ViT-L via ITC+ITM+LM',
    '  • Stage 2: Generative alignment (Q→LLM)',
    '  • Stage 3: Caption finetuning',
    '',
    'Schedules: 50k (3/3/5), 100k (10/10/15) epochs'
])

prs.add_content_slide('Local Results & Scaling Analysis', [
    'Paper BLIP-2 (ViT-g, OPT-2.7B, 129M): BLEU-4=43.7, CIDEr=145.8',
    '',
    'Local 10k:    BLEU-4=1.45,   CIDEr=3.03    (baseline)',
    'Local 50k:    BLEU-4=11.13,  CIDEr=37.57   (epoch 3) ✓ PEAK',
    'Local 100k:   BLEU-4=8.57,   CIDEr=25.34   (epoch 2) ⚠ PEAKS EARLY',
    'Local 100k:   BLEU-4=6.61,   CIDEr=18.36   (epoch 14 final) → degradation',
    '',
    'Key finding: 10k→50k shows >7× gain (learning). 50k→100k peaks early.'
])

prs.add_content_slide('Why The Gap? Systematic Breakdown', [
    'Paper: ViT-g (7×), OPT-2.7B (8×), 129M pairs (1290×), 364px',
    'Local: ViT-L, OPT-350M, 50k pairs, 224px',
    '',
    'Gap sources:',
    '• Backbone scale (ViT-g→ViT-L): ~3-4× capacity loss',
    '• LLM scale (OPT-2.7B→OPT-350M): ~8× reduction',
    '• Pre-training data: 129M→0 external (COCO-only) = major impact',
    '• Fine-tune data: 50k vs. massive corpus',
    '• Resolution & budget: 224→364, schedules',
    '',
    'Verdict: ~25-30× gap = multiplicative, NOT pipeline failure'
])

prs.add_content_slide('100k Run: Peak-Early Phenomenon', [
    'Training losses decreased smoothly (Stage 1: 0.33, Stage 2: 0.36)',
    '→ Bridge training stable, no divergence',
    '',
    'Caption metrics showed early peaking:',
    '  • Best: Epoch 2 (BLEU-4=8.57, CIDEr=25.34)',
    '  • Final: Epoch 14 (BLEU-4=6.61, CIDEr=18.36) – 23% decline',
    '',
    'Root cause: Without tuned regularization, longer training',
    'without validation-driven early stopping = overfitting',
    '',
    'Diversity increased (677→734 captions) but semantic quality degraded'
])

prs.add_content_slide('Study Limitations', [
    '1. Local eval: 1k val/test (paper: full Karpathy)',
    '   → Internally comparable but not leaderboard-equivalent',
    '',
    '2. Downscaling: CLIP ViT-L + OPT-350M vs. ViT-g + OPT-2.7B',
    '   → Studied downscaling path, not exact reproduction',
    '',
    '3. Single-seed runs (no variance)',
    '',
    '4. Windows portability: Code fixes for non-distributed mode',
    '',
    '5. No synthetic data (unlike LLaVA)'
])

prs.add_content_slide('Future Work & Unexplored Directions', [
    '1. Backbone scaling: ViT-B, ViT-L, ViT-H systematically',
    '',
    '2. Data augmentation: Synthetic descriptions from larger models',
    '',
    '3. Regularization tuning: Early stopping, dropout, LR schedules',
    '   for student models',
    '',
    '4. Multi-resolution training (224→448) with batch accumulation',
    '',
    '5. Ensemble decoded captions from multiple checkpoints',
    '',
    '6. Compare ViT-L CLIP embeddings on external benchmarks'
])

prs.add_content_slide('Main Conclusions', [
    '✓ BLIP-2 pipeline IS reproducible on consumer GPU',
    '  (all 3 stages ran end-to-end)',
    '',
    '✗ BLIP-2 performance NOT directly reproducible at local scale',
    '',
    '⟹ Gap is systematic (backbones, data, compute), NOT pathological',
    '',
    'Why BLIP-2 was best choice:',
    '  • Modular Q-Former provides downscaling path',
    '  • Frozen backbones allow principled reduction',
    '  • Well-maintained LAVIS code',
    '  • No synthetic data dependency'
])

prs.add_content_slide('Reproducibility Artifacts', [
    'Checkpoint registry: metrics/blip2/checkpoint_registry.jsonl',
    '  → All runs, epochs, losses',
    '',
    'Per-epoch evals: metrics/blip2/caption_eval_summary_*.json',
    '  → Full trajectories, best-epoch validated',
    '',
    'Configs: configs/stage{1,2}_*.yaml & caption_*.yaml',
    '  → Exact hyperparams for 10k/50k/100k',
    '',
    'Loss logs: metrics/blip2/progress_registry.jsonl',
    '',
    'Code: Official LAVIS pipeline + documented modifications'
])

prs.add_content_slide('Research Implications', [
    'Multimodal literature conflates architecture + scale',
    'This study: BLIP-2 architecture sound; gap is scale-driven',
    '',
    'For practitioners:',
    '  • Backbone selection = biggest lever',
    '  • Checkpoint selection > longer training (100k proves)',
    '  • Frozen-bridge genuinely modular & downscalable',
    '',
    'For reproducibility:',
    '  • Pipeline reproducibility ≠ performance (important distinction)',
    '  • Metric-driven selection needed for student-scale',
    '  • Artifact trail matters: losses + metrics + configs',
    '',
    'Future: Efficient backbones (MobileViT, DeiT) + full pipeline'
])

# Save presentation
prs.save()

full_path = os.path.abspath(prs.filename)
file_size = os.path.getsize(prs.filename) / 1024  # KB
print(f"✓ File: {prs.filename}")
print(f"✓ Full path: {full_path}")
print(f"✓ Size: {file_size:.1f} KB")
print(f"✓ Slides: 15")
