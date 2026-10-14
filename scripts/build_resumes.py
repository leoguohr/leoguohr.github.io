"""Build the public CVs; no phone number, class rank, or private repository URL."""
from pathlib import Path
import shutil
import subprocess
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, HRFlowable, Table, TableStyle, KeepTogether, Spacer

ROOT = Path(__file__).resolve().parents[1]
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
BLUE = colors.HexColor('#1F4E79')
GRAY = colors.HexColor('#41464b')

DATA = {
 'en': {
  'name':'HAORAN GUO','file':'Haoran_Guo_CV.pdf',
  'education':'EDUCATION','school':'University of Science and Technology of China (USTC)',
  'degree':'School of Information Science and Technology | Undergraduate | Sep 2024 - Expected Jun 2028',
  'courses':'Selected coursework: Mathematical Analysis, Linear Algebra, Modern Control Theory.',
  'section':'RESEARCH &amp; ENGINEERING PROJECTS',
  'projects':[
   ('NEXUS: 3D Shape Generation and Reconstruction','Jul 15 - Aug 15, 2026',[
    'A 3D mesh represents an object’s surface with connected triangles. Implemented models based on NEXUS that learn vertex positions and their connections for 3D shape generation and reconstruction.',
    'Built PyTorch workflows for data processing, training, evaluation, and visualization; used controlled experiments to improve architecture and training choices.',
    'Achieved <b>99.63% surface reconstruction F1 on 100 fixed training shapes</b>, measuring the balance of recovered and extra faces. Evaluations under different posterior-noise conditions gave similar scores.']),
   ('Persona-to-Scene: Multi-Agent Scene Generation and Editing','Jul 15 - Aug 15, 2026',[
    'Built collaborating AI agents that turn a person’s interests and daily habits into a room layout and personalized interior images.',
    'Supported scene editing as activity needs change; used information tracking, instruction validation, and before/after image comparisons in end-to-end case studies.']),
   ('SceneFun3D Track 1: Interactive 3D Scene Understanding','',[
    'Placed sixth as an independent entrant, identifying interactive parts of indoor 3D scenes, such as handles and buttons.',
    'Completed environment and data preparation, baseline reproduction, training, and evaluation. Test-set results are listed on the official SceneFun3D benchmark.']),
   ('RoboGame: RGB-D Perception and Robotic Grasping','Jun - Oct 2026',[
    'Built a vision-guided grasping system: a RealSense D435i depth camera locates colored blocks, and a robotic arm uses a suction cup to pick them up. Completed perception, arm control, and hardware integration testing.']),
   ('Facial Expression Recognition','',[
    'Trained a lightweight MobileNetV2 classifier on FER2013 to recognize expressions such as happiness and surprise; compared several models on accuracy and computational cost.'])],
  'skills':'TECHNICAL SKILLS','skill_lines':[
   '<b>Programming:</b> Python, C/C++, Linux/Ubuntu, Git.',
   '<b>Machine learning:</b> PyTorch, training and debugging, evaluation, 3D mesh processing.',
   '<b>Robotics and tools:</b> MuJoCo, STM32, MATLAB.'],
  'honors':'HONORS &amp; ACTIVITIES','honor_text':'USTC Outstanding Student Scholarship; member of the USTC boxing team.'
 }
}

def build(lang):
 if lang == "zh":
  tectonic = shutil.which("tectonic") or str(ROOT.parent / "tools/bin/tectonic")
  subprocess.run([tectonic, "--outdir", str(ROOT / "assets"), str(ROOT / "scripts/郭浩然简历.tex")], check=True)
  return
 d=DATA[lang];cn=lang=='zh';font='STSong-Light' if cn else 'Helvetica';bold=font if cn else 'Helvetica-Bold'
 body=ParagraphStyle('body',fontName=font,fontSize=10.2 if cn else 9.6,leading=14.6 if cn else 12.7,textColor=GRAY,wordWrap='CJK' if cn else None,spaceAfter=3)
 name=ParagraphStyle('name',parent=body,fontName=bold,fontSize=25,leading=29,alignment=TA_CENTER,spaceAfter=6)
 contact=ParagraphStyle('contact',parent=body,fontSize=9.2,leading=12.5,alignment=TA_CENTER,spaceAfter=3)
 section=ParagraphStyle('section',parent=body,fontName=bold,fontSize=12.1,leading=16,textColor=BLUE,spaceBefore=10,spaceAfter=3)
 project=ParagraphStyle('project',parent=body,fontName=bold,fontSize=10.5 if cn else 10.1,leading=13.5,spaceBefore=0,spaceAfter=0)
 date=ParagraphStyle('date',parent=body,fontSize=8.8,alignment=2,spaceAfter=0)
 bullet=ParagraphStyle('bullet',parent=body,leftIndent=10,firstLineIndent=0,bulletIndent=0,spaceAfter=3)
 story=[Paragraph(d['name'],name),Paragraph('<link href="mailto:ghr@mail.ustc.edu.cn">ghr@mail.ustc.edu.cn</link> &nbsp; | &nbsp; <link href="https://leoguohr.github.io">leoguohr.github.io</link>',contact)]
 def heading(s):story.extend([Paragraph(s,section),HRFlowable(width='100%',thickness=.6,color=BLUE,spaceAfter=5)])
 heading(d['education']);story.extend([Paragraph(d['school'],project),Spacer(1,3),Paragraph(d['degree'],body),Paragraph('GPA: 3.52/4.3',body),Paragraph(d['courses'],body)])
 heading(d['section'])
 for title,period,bullets in d['projects']:
  cells=[[Paragraph(title,project),Paragraph(period,date)]]
  table=Table(cells,colWidths=[A4[0]-80-118,118]);table.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),4),('VALIGN',(0,0),(-1,-1),'TOP')]))
  story.append(KeepTogether([table]+[Paragraph(t,bullet,bulletText='•') for t in bullets]))
 heading(d['skills']);story.extend(Paragraph(t,body) for t in d['skill_lines'])
 heading(d['honors']);story.append(Paragraph(d['honor_text'],body))
 path=ROOT/'assets'/d['file'];SimpleDocTemplate(str(path),pagesize=A4,leftMargin=40,rightMargin=40,topMargin=29,bottomMargin=28,title='郭浩然简历' if cn else 'Haoran Guo - Curriculum Vitae',author='Haoran Guo').build(story)
 print(path)
if __name__ == '__main__':
 for lang in ['zh','en']:build(lang)
