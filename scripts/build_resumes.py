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
   ('NEXUS：三维拓扑VAE与点云条件顶点扩散','2026.07.15 - 08.15',[
    '基于PyTorch实现并迭代拓扑VAE与点云条件八叉树顶点扩散模块，搭建数据处理、训练恢复、实际拓扑重建评价与可视化流程。',
    '围绕Fourier坐标特征、Graph/LayerNorm顺序及Face负例采样开展对照实验，分析结构重建与优化行为。',
    '最终VAE在固定100条训练网格上的实际Face micro-F1达到99.63%，五组固定后验噪声评价获得相近分数；Face由预测Edge图枚举后分类。']),
   ('Persona-to-Scene：多智能体场景生成与编辑','2026.07.15 - 08.15',[
    '开发多智能体管线，将人物描述转化为场景内容、空间布局和结构化生成指令，支持室内图像生成及事件驱动编辑。',
    '结合证据追踪、结构校验和成对图像评价，完成端到端案例验证，并整理生成与编辑前后的效果对比。']),
   ('SceneFun3D Track 1：三维场景功能区域分割','',[
    '以Night’s Watch队参与功能区域分割任务，完成环境配置和数据集准备，复现基线三维感知模型并梳理训练、推理与评价流程。',
    '围绕真实室内场景的功能区域理解与可供性定位开展方案调研；测试集提交已收录于SceneFun3D官方公开榜单。']),
   ('RoboGame：视觉识别与机械臂抓取','2026.06 - 10',[
    '基于RealSense D435i实现方块顶面识别与三维定位，结合深度对齐、IMU倾角补偿和多帧平均；完成相机到机械臂坐标变换、五舵机逆运动学及吸盘抓取流程，完成实机联调。']),
   ('基于深度学习的人脸表情识别','',[
    '基于MobileNetV2实现FER2013表情分类，对比ResNet、EfficientNet与MAE-DFER的分类准确率和计算开销，组织训练与评价流程。'])],
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
   ('NEXUS: 3D Topology VAE and Vertex Diffusion','Jul 15 - Aug 15, 2026',[
    'Implemented topology VAE and point-cloud-conditioned octree vertex diffusion components in PyTorch; built data processing, training recovery, structural evaluation, and visualization workflows.',
    'Conducted controlled experiments on Fourier coordinate features, Graph/LayerNorm ordering, and face negative sampling to investigate reconstruction and optimization behavior.',
    'Achieved <b>99.63% actual Face micro-F1 on 100 fixed training meshes</b>, with faces classified from predicted edge graphs; five fixed posterior-noise evaluations produced similar scores.']),
   ('Persona-to-Scene: Multi-Agent Scene Generation and Editing','Jul 15 - Aug 15, 2026',[
    'Developed a multi-agent pipeline from persona descriptions to scene content, spatial layouts, and structured generation instructions for interior image generation and event-driven editing.',
    'Used evidence tracking, schema validation, and paired-image evaluation in end-to-end case studies.']),
   ('SceneFun3D Track 1: Functionality Segmentation','',[
    'Participated with team Night\'s Watch; prepared the environment and dataset, reproduced a 3D perception baseline, and organized training, inference, and evaluation workflows.',
    'Investigated functional-region understanding and affordance localization in indoor scenes. Test-set results are listed on the official SceneFun3D benchmark.']),
   ('RoboGame: RGB-D Perception and Robotic Grasping','Jun - Oct 2026',[
    'Built RealSense D435i block detection and 3D localization with depth alignment, IMU tilt compensation, and multi-frame averaging. Integrated camera-to-arm transforms, five-servo inverse kinematics, and suction-grasp control; completed hardware integration testing.']),
   ('Facial Expression Recognition','',[
    'Implemented MobileNetV2 classification on FER2013 and compared accuracy and computational cost with ResNet, EfficientNet, and MAE-DFER.'])],
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
