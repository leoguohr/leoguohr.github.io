"""Build the public CVs; no phone number, class rank, or private repository URL."""
from pathlib import Path
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
 'zh': {
  'name':'郭浩然','file':'郭浩然简历.pdf',
  'education':'教育背景','school':'中国科学技术大学（USTC）',
  'degree':'信息科学技术学院 · 本科在读 | 2024.09 - 至今 | 预计2028年6月毕业',
  'courses':'核心课程：数学分析、线性代数、模拟电子技术、数字电子技术、现代控制理论。',
  'section':'科研与项目经历',
  'projects':[
   ('NEXUS：三维形状生成与重建','2026.07.15 - 08.15',[
    '三维物体表面可用相互连接的小三角形表示，称为网格（mesh）。围绕NEXUS实现三维点生成与拓扑重建模型，学习点的位置及连接关系。',
    '使用PyTorch搭建数据处理、模型训练、结果评价和可视化流程，并通过对照实验改进模型结构与训练方式。',
    '在固定100个训练样本上，表面重建F1评分达到99.63%，综合衡量生成表面的完整性与准确性；不同随机采样条件下保持相近表现。']),
   ('Persona-to-Scene：多智能体场景生成与编辑','2026.07.15 - 08.15',[
    '开发多个AI协作的场景生成系统，根据人物的兴趣与生活习惯，规划房间布局并生成个性化室内图像。',
    '支持活动需求变化后的场景编辑；通过信息追踪、指令校验及生成前后图像对比，验证从人物描述到场景修改的完整流程。']),
   ('SceneFun3D Track 1：三维场景交互区域识别','',[
    '独立参赛并获得第六名。任务是从三维室内场景中识别把手、按钮等可交互部位，帮助计算机理解物体的使用方式。',
    '独立完成环境与数据准备、基线模型复现、训练和评价；测试集提交已收录于SceneFun3D官方公开榜单。']),
   ('RoboGame：视觉识别与机械臂抓取','2026.06 - 10',[
    '使用RealSense D435i深度相机识别彩色方块并估计三维位置，再控制机械臂用吸盘完成抓取、抬升和返回；完成视觉定位、机械臂控制及实机联调。']),
   ('基于深度学习的人脸表情识别','',[
    '基于MobileNetV2训练图像分类模型，识别高兴、惊讶等人脸表情；在FER2013数据集上比较多种模型的准确率与计算开销。'])],
  'skills':'技术能力','skill_lines':[
   '编程与开发：Python、C/C++、Linux/Ubuntu、Git。',
   '深度学习：PyTorch模型实现、训练调试、推理评价、三维网格处理与对照实验。',
   '机器人与工具：MuJoCo、STM32、MATLAB。'],
  'honors':'荣誉与活动','honor_text':'中国科学技术大学优秀学生奖学金；中国科学技术大学拳击队成员。'
 },
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
for lang in ['zh','en']:build(lang)
