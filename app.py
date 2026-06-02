import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import io
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="MedData Analyzer", page_icon="🧬", layout="wide", initial_sidebar_state="expanded")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
:root {
    --bg:     #050c18;
    --card:   rgba(10,22,40,0.85);
    --border: rgba(0,212,200,0.15);
    --glow:   rgba(0,212,200,0.4);
    --cyan:   #00d4c8;
    --teal:   #0891b2;
    --gold:   #f59e0b;
    --text:   #e8f4f8;
    --muted:  #7a9bb5;
    --red:    #ef4444;
    --green:  #10b981;
}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;color:var(--text);}
.stApp{
    background:var(--bg);
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%,rgba(0,212,200,0.06) 0%,transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%,rgba(8,145,178,0.06) 0%,transparent 60%);
}
.stApp::before{content:'';position:fixed;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,var(--teal),var(--cyan),var(--teal),transparent);z-index:9999;}
.main .block-container{padding:2rem 2.5rem;max-width:1400px;}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#040b16 0%,#071220 60%,#050f1c 100%);border-right:1px solid var(--border);}
section[data-testid="stSidebar"] *{color:var(--text) !important;}
section[data-testid="stSidebar"] .stRadio label{border-radius:10px;padding:10px 16px;font-size:0.88rem;transition:all 0.25s;border:1px solid transparent;cursor:pointer;display:block;}
section[data-testid="stSidebar"] .stRadio label:hover{background:rgba(0,212,200,0.06);border-color:var(--border);color:var(--cyan) !important;}
h1,h2,h3,h4{font-family:'Syne',sans-serif !important;color:var(--text) !important;letter-spacing:-0.02em;}
.page-header{padding:2rem 0 1.5rem;border-bottom:1px solid var(--border);margin-bottom:2rem;}
.page-header .eyebrow{font-size:0.7rem;font-weight:500;letter-spacing:0.2em;text-transform:uppercase;color:var(--cyan);margin-bottom:8px;}
.page-header h1{font-size:2.2rem;font-weight:800;margin:0;background:linear-gradient(135deg,#e8f4f8 0%,var(--cyan) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.page-header .subtitle{color:var(--muted);font-size:0.9rem;margin-top:8px;}
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:2rem;}
.kpi-card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:20px 22px;position:relative;overflow:hidden;backdrop-filter:blur(12px);transition:border-color 0.3s,transform 0.3s;}
.kpi-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--cyan),transparent);opacity:0.6;}
.kpi-card:hover{border-color:var(--glow);transform:translateY(-2px);}
.kpi-card .kpi-label{font-size:0.68rem;font-weight:500;letter-spacing:0.15em;text-transform:uppercase;color:var(--muted);margin-bottom:10px;}
.kpi-card .kpi-value{font-family:'Syne',sans-serif;font-size:2rem;font-weight:700;color:var(--text);}
.kpi-card .kpi-icon{position:absolute;right:18px;top:18px;font-size:1.4rem;opacity:0.25;}
.kpi-card.c-cyan .kpi-value{color:var(--cyan);}
.kpi-card.c-gold .kpi-value{color:var(--gold);}
.kpi-card.c-red  .kpi-value{color:var(--red);}
.kpi-card.c-green .kpi-value{color:var(--green);}
.glass{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:24px;backdrop-filter:blur(16px);margin-bottom:20px;}
.tag{display:inline-flex;align-items:center;gap:8px;background:rgba(0,212,200,0.1);border:1px solid var(--glow);border-radius:100px;padding:5px 14px;font-size:0.72rem;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:var(--cyan);margin-bottom:16px;}
.ai{background:rgba(0,212,200,0.07);border:1px solid rgba(0,212,200,0.2);border-radius:10px;padding:14px 18px;color:var(--text);margin:8px 0;}
.as{background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.25);border-radius:10px;padding:14px 18px;color:#6ee7b7;margin:8px 0;}
.aw{background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.25);border-radius:10px;padding:14px 18px;color:#fcd34d;margin:8px 0;}
.ae{background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.25);border-radius:10px;padding:14px 18px;color:#fca5a5;margin:8px 0;}
.pill{display:inline-block;padding:3px 12px;border-radius:100px;font-size:0.72rem;font-weight:600;}
.p-ok{background:rgba(16,185,129,0.15);color:#34d399;border:1px solid rgba(16,185,129,0.3);}
.p-w{background:rgba(245,158,11,0.15);color:#fbbf24;border:1px solid rgba(245,158,11,0.3);}
.p-b{background:rgba(239,68,68,0.15);color:#f87171;border:1px solid rgba(239,68,68,0.3);}
.feat{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:24px;transition:all 0.3s;}
.feat:hover{border-color:var(--glow);transform:translateY(-3px);box-shadow:0 12px 32px rgba(0,212,200,0.08);}
.feat .fi{font-size:1.8rem;margin-bottom:12px;}
.feat .ft{font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:var(--text);margin-bottom:8px;}
.feat .fd{font-size:0.83rem;color:var(--muted);line-height:1.6;}
.step{display:flex;gap:16px;align-items:flex-start;padding:18px;background:var(--card);border:1px solid var(--border);border-radius:12px;margin-bottom:10px;}
.sn{width:32px;height:32px;background:rgba(0,212,200,0.1);border:1px solid var(--glow);border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'Syne',sans-serif;font-weight:700;color:var(--cyan);font-size:0.85rem;flex-shrink:0;}
.sc .st{font-weight:600;color:var(--text);font-size:0.9rem;margin-bottom:3px;}
.sc .sd{font-size:0.8rem;color:var(--muted);}
.sbar-logo{padding:28px 20px 20px;border-bottom:1px solid var(--border);margin-bottom:16px;}
.sbar-logo .lm{font-size:1.6rem;margin-bottom:6px;}
.sbar-logo .ln{font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:var(--text);}
.sbar-logo .ls{font-size:0.7rem;color:var(--cyan);letter-spacing:0.12em;text-transform:uppercase;font-weight:500;}
.ds-badge{background:rgba(0,212,200,0.07);border:1px solid var(--border);border-radius:12px;padding:14px 16px;margin:0 8px;font-size:0.82rem;}
.ds-badge .dn{color:var(--cyan);font-weight:600;font-size:0.85rem;margin-bottom:8px;}
.ds-badge .dr{display:flex;justify-content:space-between;color:var(--muted);margin-bottom:4px;}
.ds-badge .dr span{color:var(--text);font-weight:500;}
.hitem{font-size:0.8rem;color:var(--muted);padding:6px 12px;border-left:2px solid var(--border);margin-bottom:4px;}
.hitem .ht{color:var(--cyan);margin-right:8px;}
.stButton>button{background:linear-gradient(135deg,rgba(0,212,200,0.15),rgba(8,145,178,0.15));color:var(--cyan) !important;border:1px solid var(--glow) !important;border-radius:10px;font-weight:500;padding:10px 22px;transition:all 0.25s;}
.stButton>button:hover{background:linear-gradient(135deg,rgba(0,212,200,0.25),rgba(8,145,178,0.25));border-color:var(--cyan) !important;transform:translateY(-1px);box-shadow:0 8px 24px rgba(0,212,200,0.18);}
[data-testid="stDownloadButton"]>button{background:linear-gradient(135deg,rgba(16,185,129,0.15),rgba(5,150,105,0.15)) !important;color:#34d399 !important;border:1px solid rgba(16,185,129,0.3) !important;}
.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:rgba(5,15,30,0.8) !important;border:1px solid var(--border) !important;border-radius:10px !important;color:var(--text) !important;}
.stSelectbox>div>div{background:rgba(5,15,30,0.8) !important;border:1px solid var(--border) !important;border-radius:10px !important;}
.stSlider>div>div>div>div{background:var(--cyan) !important;}
.stTabs [data-baseweb="tab-list"]{background:rgba(5,15,30,0.6) !important;border-radius:12px;padding:4px;border:1px solid var(--border);}
.stTabs [data-baseweb="tab"]{background:transparent !important;border-radius:9px;color:var(--muted) !important;font-size:0.85rem;}
.stTabs [aria-selected="true"]{background:rgba(0,212,200,0.12) !important;color:var(--cyan) !important;border:1px solid var(--glow) !important;}
[data-testid="stMetricValue"]{font-family:'Syne',sans-serif !important;color:var(--cyan) !important;font-size:2rem !important;}
[data-testid="stMetricLabel"]{color:var(--muted) !important;font-size:0.78rem !important;text-transform:uppercase;letter-spacing:0.1em;}
[data-testid="stFileUploadDropzone"]{background:rgba(0,212,200,0.03) !important;border:2px dashed var(--glow) !important;border-radius:16px !important;}
[data-baseweb="tag"]{background:rgba(0,212,200,0.15) !important;border:1px solid var(--glow) !important;border-radius:6px !important;}
[data-baseweb="tag"] span{color:var(--cyan) !important;}
hr{border:none;border-top:1px solid var(--border);margin:2rem 0;}
#MainMenu,footer,header{visibility:hidden;}
::-webkit-scrollbar{width:6px;height:6px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--glow);border-radius:3px;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ── FIX : template Plotly sans go.Layout ─────────────────────
DARK_LAYOUT = dict(
    paper_bgcolor='rgba(5,12,24,0)',
    plot_bgcolor='rgba(5,12,24,0)',
    font=dict(family='DM Sans,Arial', color='#7a9bb5', size=12),
    title_font=dict(family='Syne,Arial', color='#e8f4f8', size=16),
    xaxis=dict(gridcolor='rgba(0,212,200,0.07)', linecolor='rgba(0,212,200,0.15)'),
    yaxis=dict(gridcolor='rgba(0,212,200,0.07)', linecolor='rgba(0,212,200,0.15)'),
    colorway=['#00d4c8','#0891b2','#f59e0b','#10b981','#8b5cf6','#ef4444'],
    margin=dict(l=20,r=20,t=50,b=20),
    hoverlabel=dict(bgcolor='#0a1628',bordercolor='rgba(0,212,200,0.3)',font=dict(color='#e8f4f8')),
    legend=dict(bgcolor='rgba(5,12,24,0.5)',bordercolor='rgba(0,212,200,0.15)'),
)

def T(fig):
    fig.update_layout(**DARK_LAYOUT)
    return fig

for k,v in [("df",None),("df0",None),("hist",[]),("fname","")]:
    if k not in st.session_state: st.session_state[k]=v

def H(a):
    ts=datetime.now().strftime("%H:%M:%S")
    st.session_state.hist.append({"t":ts,"a":a})

def kpi(label,val,icon,acc=""):
    return f'<div class="kpi-card {acc}"><div class="kpi-icon">{icon}</div><div class="kpi-label">{label}</div><div class="kpi-value">{val}</div></div>'

def ph(eye,title,sub):
    st.markdown(f'<div class="page-header"><div class="eyebrow">{eye}</div><h1>{title}</h1><p class="subtitle">{sub}</p></div>',unsafe_allow_html=True)

def alert(msg,t="i"):
    cls={"i":"ai","s":"as","w":"aw","e":"ae"}[t]
    st.markdown(f'<div class="{cls}">{msg}</div>',unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="sbar-logo"><div class="lm">🧬</div><div class="ln">MedData Analyzer</div><div class="ls">Sciences de Données Médicales</div></div>',unsafe_allow_html=True)
    page = st.radio("Nav",[
        "🏠  Accueil",
        "📂  Importation",
        "🔍  Analyse exploratoire",
        "⚙️  Preprocessing",
        "📊  Visualisations",
        "💾  Exportation",
        "ℹ️  A propos"
    ],label_visibility="collapsed")
    if st.session_state.df is not None:
        df=st.session_state.df
        mv=round(df.isnull().sum().sum()/max(df.shape[0]*df.shape[1],1)*100,1)
        pc="p-ok" if mv==0 else ("p-w" if mv<10 else "p-b")
        fn=st.session_state.fname; short=fn[:22]+"…" if len(fn)>24 else fn
        st.markdown(f'<div class="ds-badge"><div class="dn">📄 {short}</div><div class="dr">Lignes<span>{df.shape[0]:,}</span></div><div class="dr">Colonnes<span>{df.shape[1]}</span></div><div class="dr">Manquants<span class="pill {pc}">{mv}%</span></div><div class="dr">Doublons<span>{df.duplicated().sum()}</span></div></div>',unsafe_allow_html=True)
    st.markdown('<br><div style="text-align:center;font-size:0.65rem;color:#3d5a72;padding-bottom:12px;">UM6SS · LICENCE IDSD · 2024-2025</div>',unsafe_allow_html=True)

if page == "🏠  Accueil":
    ph("Plateforme d'analyse","Sciences de Données Médicales","Analysez, nettoyez et visualisez vos données biomédicales.")
    c1,c2,c3,c4=st.columns(4)
    for col,icon,title,desc in [
        (c1,"📂","Importation","Chargez vos fichiers CSV avec détection automatique des types."),
        (c2,"🔬","Analyse EDA","Statistiques, corrélations, distributions et valeurs manquantes."),
        (c3,"⚙️","Preprocessing","Nettoyage, normalisation, encodage et filtrage avancés."),
        (c4,"📊","Visualisation","Graphiques interactifs Plotly avec export PNG."),
    ]:
        with col:
            st.markdown(f'<div class="feat"><div class="fi">{icon}</div><div class="ft">{title}</div><div class="fd">{desc}</div></div>',unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    if st.session_state.df is not None:
        df=st.session_state.df
        st.markdown('<div class="tag">Dataset en mémoire</div>',unsafe_allow_html=True)
        g="".join([kpi("Lignes",f"{df.shape[0]:,}","📋","c-cyan"),kpi("Colonnes",f"{df.shape[1]}","🗂️"),
                   kpi("Manquantes",f"{df.isnull().sum().sum():,}","❓","c-gold" if df.isnull().sum().sum()>0 else "c-green"),
                   kpi("Doublons",f"{df.duplicated().sum()}","🔁","c-red" if df.duplicated().sum()>0 else "c-green")])
        st.markdown(f'<div class="kpi-grid">{g}</div>',unsafe_allow_html=True)
    else:
        st.markdown('<div class="tag">Guide de démarrage</div>',unsafe_allow_html=True)
        for n,t,d in [("1","Importer un fichier CSV","Cliquez sur Importation et déposez votre fichier CSV."),
                      ("2","Explorer les données","Statistiques et distributions dans l'onglet Analyse."),
                      ("3","Nettoyer et Préparer","Traitez les valeurs manquantes, outliers et transformations."),
                      ("4","Visualiser et Exporter","Générez des graphiques et exportez le dataset nettoyé.")]:
            st.markdown(f'<div class="step"><div class="sn">{n}</div><div class="sc"><div class="st">{t}</div><div class="sd">{d}</div></div></div>',unsafe_allow_html=True)
    if st.session_state.hist:
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown('<div class="tag">Historique</div>',unsafe_allow_html=True)
        ht="".join([f'<div class="hitem"><span class="ht">{h["t"]}</span>{h["a"]}</div>' for h in reversed(st.session_state.hist[-8:])])
        st.markdown(f'<div class="glass" style="padding:16px">{ht}</div>',unsafe_allow_html=True)

elif page == "📂  Importation":
    ph("Etape 1","Importation des Données","Chargez votre fichier CSV pour commencer l'analyse.")
    cu,co=st.columns([2,1])
    with cu: fichier=st.file_uploader("",type=["csv"],label_visibility="collapsed")
    with co: sep=st.selectbox("Séparateur",[",",";","\t","|"],format_func=lambda x:{",":" Virgule",";":" Point-virgule","\t":" Tabulation","|":" Pipe"}[x])
    if fichier is not None:
        with st.spinner("Chargement..."):
            try:
                df=pd.read_csv(fichier,sep=sep)
                st.session_state.df0=df.copy(); st.session_state.df=df.copy(); st.session_state.fname=fichier.name
                H(f"Fichier chargé : {fichier.name} ({df.shape[0]} x {df.shape[1]})")
                alert(f"✅ Fichier chargé : {fichier.name} — {df.shape[0]:,} lignes, {df.shape[1]} colonnes","s")
            except Exception as e: alert(f"❌ Erreur : {e}","e")
    if st.session_state.df is not None:
        df=st.session_state.df
        cn=df.select_dtypes(include=np.number).columns.tolist()
        cc=df.select_dtypes(exclude=np.number).columns.tolist()
        mv=df.isnull().sum().sum(); dup=df.duplicated().sum(); mem=round(df.memory_usage(deep=True).sum()/1024,2)
        g="".join([kpi("Lignes",f"{df.shape[0]:,}","📋","c-cyan"),kpi("Colonnes",f"{df.shape[1]}","🗂️"),
                   kpi("Manquantes",f"{mv:,}","❓","c-gold" if mv>0 else "c-green"),kpi("Mémoire",f"{mem} KB","💾")])
        st.markdown(f'<div class="kpi-grid">{g}</div>',unsafe_allow_html=True)
        t1,t2,t3,t4=st.tabs(["👀 Aperçu","🗂️ Types","📈 Statistiques","ℹ️ Infos"])
        with t1:
            n=st.slider("Lignes à afficher",5,min(100,len(df)),10)
            st.dataframe(df.head(n),use_container_width=True,height=360)
        with t2:
            c1,c2=st.columns(2)
            with c1:
                st.markdown('<div class="tag">Colonnes numériques</div>',unsafe_allow_html=True)
                for c in cn: st.markdown(f"<span class='pill p-ok'>{c}</span> &nbsp;",unsafe_allow_html=True)
            with c2:
                st.markdown('<div class="tag">Colonnes catégorielles</div>',unsafe_allow_html=True)
                for c in cc: st.markdown(f"<span class='pill p-w'>{c}</span> &nbsp;",unsafe_allow_html=True)
            st.markdown("<br>",unsafe_allow_html=True)
            info=pd.DataFrame({"Colonne":df.columns,"Type":[str(t) for t in df.dtypes],"Non-nulles":df.count().values,
                                "Manquantes":df.isnull().sum().values,"% Manquant":(df.isnull().mean()*100).round(2).values,
                                "Valeurs uniques":[df[c].nunique() for c in df.columns]})
            st.dataframe(info,use_container_width=True,hide_index=True)
        with t3: st.dataframe(df.describe().T.round(3),use_container_width=True)
        with t4:
            c1,c2,c3=st.columns(3)
            c1.metric("Col. numériques",len(cn)); c2.metric("Col. catégorielles",len(cc)); c3.metric("Doublons",dup)
            alert(f"⚠️ {dup} doublon(s) détecté(s).","w") if dup>0 else alert("✅ Aucun doublon détecté.","s")

elif page == "🔍  Analyse exploratoire":
    if st.session_state.df is None: alert("⚠️ Importez d'abord un fichier CSV.","w"); st.stop()
    ph("Etape 2","Analyse Exploratoire","Explorez la structure statistique de vos données.")
    df=st.session_state.df
    cn=df.select_dtypes(include=np.number).columns.tolist()
    cc=df.select_dtypes(exclude=np.number).columns.tolist()
    t1,t2,t3,t4,t5=st.tabs(["📊 Statistiques","🔗 Corrélations","📈 Distributions","❓ Manquantes","🔁 Doublons"])
    with t1:
        if not cn: alert("Aucune colonne numérique.","i")
        else:
            col=st.selectbox("Colonne",cn)
            d=df[col].dropna()
            c1,c2,c3,c4=st.columns(4)
            c1.metric("Moyenne",f"{d.mean():.4f}"); c2.metric("Médiane",f"{d.median():.4f}")
            c3.metric("Écart-type",f"{d.std():.4f}"); c4.metric("Mode",f"{d.mode()[0]:.4f}" if len(d.mode()) else "N/A")
            c1,c2,c3,c4=st.columns(4)
            c1.metric("Minimum",f"{d.min():.4f}"); c2.metric("Maximum",f"{d.max():.4f}")
            c3.metric("Q1 (25%)",f"{d.quantile(0.25):.4f}"); c4.metric("Q3 (75%)",f"{d.quantile(0.75):.4f}")
            c1,c2,c3,c4=st.columns(4)
            c1.metric("Variance",f"{d.var():.4f}"); c2.metric("IQR",f"{d.quantile(0.75)-d.quantile(0.25):.4f}")
            c3.metric("Asymétrie",f"{d.skew():.4f}"); c4.metric("Kurtosis",f"{d.kurtosis():.4f}")
            fig=px.histogram(df,x=col,nbins=35,title=f"Distribution — {col}",color_discrete_sequence=["#00d4c8"])
            fig.update_traces(marker_line_width=0,opacity=0.85); st.plotly_chart(T(fig),use_container_width=True)
    with t2:
        if len(cn)<2: alert("Il faut au moins 2 colonnes numériques.","i")
        else:
            corr=df[cn].corr()
            fig=px.imshow(corr,text_auto=".2f",aspect="auto",title="Matrice de Corrélation",
                          color_continuous_scale=["#050c18","#0891b2","#00d4c8","#e8f4f8"])
            fig.update_layout(height=500); st.plotly_chart(T(fig),use_container_width=True)
            pairs=corr.abs().unstack().sort_values(ascending=False)
            pairs=pairs[pairs<1.0].drop_duplicates().head(8).reset_index()
            pairs.columns=["Variable A","Variable B","Corrélation (|r|)"]
            st.markdown('<div class="tag">Top corrélations</div>',unsafe_allow_html=True)
            st.dataframe(pairs,use_container_width=True,hide_index=True)
    with t3:
        c1,c2=st.columns(2)
        with c1:
            if cn:
                col=st.selectbox("Colonne numérique",cn,key="d1")
                tp=st.selectbox("Type",["Histogramme","Boxplot","Courbe de densité"])
                if tp=="Histogramme":
                    fig=px.histogram(df,x=col,nbins=35,color_discrete_sequence=["#00d4c8"],title=f"Histogramme — {col}")
                    fig.update_traces(marker_line_width=0,opacity=0.85)
                elif tp=="Boxplot":
                    fig=px.box(df,y=col,color_discrete_sequence=["#0891b2"],title=f"Boxplot — {col}")
                else:
                    try: fig=ff.create_distplot([df[col].dropna().tolist()],[col],colors=["#00d4c8"],show_rug=False); fig.update_layout(title=f"Densité — {col}")
                    except: fig=px.histogram(df,x=col,nbins=35,color_discrete_sequence=["#00d4c8"],title=f"Distribution — {col}")
                st.plotly_chart(T(fig),use_container_width=True)
        with c2:
            if cc:
                col=st.selectbox("Colonne catégorielle",cc,key="d2")
                tp=st.selectbox("Type",["Bar chart","Pie chart"])
                vc=df[col].value_counts().reset_index(); vc.columns=["Valeur","Effectif"]
                if tp=="Bar chart":
                    fig=px.bar(vc,x="Valeur",y="Effectif",color="Effectif",color_continuous_scale=["#0a1628","#00d4c8"],title=f"Distribution — {col}")
                else:
                    fig=px.pie(vc,names="Valeur",values="Effectif",title=f"Répartition — {col}",hole=0.35,
                               color_discrete_sequence=["#00d4c8","#0891b2","#f59e0b","#10b981","#8b5cf6","#ef4444"])
                st.plotly_chart(T(fig),use_container_width=True)
        if len(cn)>=2:
            st.markdown('<div class="tag">Scatter Plot</div>',unsafe_allow_html=True)
            cx,cy=st.columns(2)
            xc=cx.selectbox("Axe X",cn,key="sx"); yc=cy.selectbox("Axe Y",cn,key="sy",index=min(1,len(cn)-1))
            hue=st.selectbox("Couleur par",["Aucun"]+cc) if cc else "Aucun"
            fig=px.scatter(df,x=xc,y=yc,color=(hue if hue!="Aucun" else None),opacity=0.75,title=f"{xc} vs {yc}",
                           color_discrete_sequence=["#00d4c8"])
            st.plotly_chart(T(fig),use_container_width=True)
    with t4:
        mv=df.isnull().sum().reset_index(); mv.columns=["Colonne","Manquantes"]
        mv["% Manquant"]=(mv["Manquantes"]/len(df)*100).round(2)
        mv=mv[mv["Manquantes"]>0].sort_values("Manquantes",ascending=False)
        if mv.empty: alert("✅ Aucune valeur manquante — dataset complet.","s")
        else:
            tot=mv["Manquantes"].sum()
            c1,c2,c3=st.columns(3)
            c1.metric("Cellules manquantes",f"{tot:,}"); c2.metric("Colonnes affectées",len(mv)); c3.metric("% global",f"{round(tot/(df.shape[0]*df.shape[1])*100,2)}%")
            st.dataframe(mv,use_container_width=True,hide_index=True)
            fig=px.bar(mv,x="Colonne",y="% Manquant",color="% Manquant",color_continuous_scale=["#0891b2","#f59e0b","#ef4444"],title="% valeurs manquantes")
            st.plotly_chart(T(fig),use_container_width=True)
    with t5:
        nb=df.duplicated().sum()
        if nb==0: alert("✅ Aucun doublon détecté.","s")
        else:
            alert(f"⚠️ {nb} ligne(s) dupliquée(s).","w")
            st.dataframe(df[df.duplicated()],use_container_width=True)

elif page == "⚙️  Preprocessing":
    if st.session_state.df is None: alert("⚠️ Importez d'abord un fichier CSV.","w"); st.stop()
    ph("Etape 3","Preprocessing des Données","Nettoyez, transformez et préparez vos données.")
    df=st.session_state.df
    cn=df.select_dtypes(include=np.number).columns.tolist()
    cc=df.select_dtypes(exclude=np.number).columns.tolist()
    t1,t2,t3,t4,t5,t6=st.tabs(["❓ Val. manquantes","🔁 Doublons","📉 Outliers","🔄 Transformations","🗑️ Colonnes","🔍 Filtrage"])
    with t1:
        mvc=[c for c in df.columns if df[c].isnull().any()]
        if not mvc: alert("✅ Aucune valeur manquante.","s")
        else:
            c1,c2=st.columns(2)
            with c1:
                col=st.selectbox("Colonne",mvc); nb=df[col].isnull().sum()
                alert(f"❓ {nb} valeur(s) manquante(s) dans <b>{col}</b>","w")
            with c2:
                meth=st.selectbox("Méthode",["Supprimer les lignes","Supprimer la colonne","Remplacer par la moyenne","Remplacer par la médiane","Remplacer par le mode","Valeur personnalisée"])
                vp=st.text_input("Valeur") if meth=="Valeur personnalisée" else None
            if st.button("✅ Appliquer",key="bmv"):
                df2=df.copy()
                if meth=="Supprimer les lignes": df2=df2.dropna(subset=[col])
                elif meth=="Supprimer la colonne": df2=df2.drop(columns=[col])
                elif meth=="Remplacer par la moyenne": df2[col]=df2[col].fillna(df2[col].mean())
                elif meth=="Remplacer par la médiane": df2[col]=df2[col].fillna(df2[col].median())
                elif meth=="Remplacer par le mode": df2[col]=df2[col].fillna(df2[col].mode()[0])
                elif vp: df2[col]=df2[col].fillna(vp)
                st.session_state.df=df2; H(f"VM — {col} : {meth}"); alert("✅ Traitement appliqué !","s"); st.rerun()
    with t2:
        nb=df.duplicated().sum()
        c1,c2,c3=st.columns(3)
        c1.metric("Doublons",nb); c2.metric("Lignes totales",len(df)); c3.metric("Lignes uniques",len(df)-nb)
        if nb>0:
            if st.button("🗑️ Supprimer les doublons"):
                st.session_state.df=df.drop_duplicates().reset_index(drop=True); H(f"Doublons supprimés : {nb}"); alert("✅ Doublons supprimés !","s"); st.rerun()
        else: alert("✅ Aucun doublon.","s")
    with t3:
        if not cn: alert("Aucune colonne numérique.","i")
        else:
            col=st.selectbox("Colonne",cn,key="oc")
            d=df[col].dropna(); Q1,Q3=d.quantile(0.25),d.quantile(0.75); IQR=Q3-Q1; bl,bu=Q1-1.5*IQR,Q3+1.5*IQR
            nb=int(((d<bl)|(d>bu)).sum())
            c1,c2,c3,c4=st.columns(4)
            c1.metric("Borne basse",f"{bl:.2f}"); c2.metric("Borne haute",f"{bu:.2f}"); c3.metric("Outliers",nb); c4.metric("% total",f"{round(nb/max(len(df),1)*100,1)}%")
            fig=px.box(df,y=col,color_discrete_sequence=["#ef4444"],title=f"Boxplot — {col}")
            st.plotly_chart(T(fig),use_container_width=True)
            if nb>0 and st.button("🗑️ Supprimer les outliers (IQR)"):
                df2=df[(df[col].isna())|((df[col]>=bl)&(df[col]<=bu))].reset_index(drop=True)
                st.session_state.df=df2; H(f"Outliers supprimés — {col} : {nb}"); alert("✅ Outliers supprimés !","s"); st.rerun()
    with t4:
        sub=st.selectbox("Transformation",["Normalisation Min-Max","Standardisation Z-score","Encodage One-Hot","Renommer une colonne","Changer le type"])
        st.markdown("<br>",unsafe_allow_html=True)
        if sub=="Normalisation Min-Max":
            alert("ℹ️ Ramène les valeurs entre 0 et 1.","i"); cols=st.multiselect("Colonnes",cn)
            if st.button("Appliquer") and cols:
                df2=df.copy()
                for c in cols:
                    mn,mx=df2[c].min(),df2[c].max()
                    if mx!=mn: df2[c]=(df2[c]-mn)/(mx-mn)
                st.session_state.df=df2; H(f"Normalisation Min-Max : {cols}"); alert("✅ Normalisation appliquée !","s"); st.rerun()
        elif sub=="Standardisation Z-score":
            alert("ℹ️ Moyenne=0, écart-type=1.","i"); cols=st.multiselect("Colonnes",cn)
            if st.button("Appliquer") and cols:
                df2=df.copy()
                for c in cols:
                    if df2[c].std()!=0: df2[c]=(df2[c]-df2[c].mean())/df2[c].std()
                st.session_state.df=df2; H(f"Standardisation Z-score : {cols}"); alert("✅ Standardisation appliquée !","s"); st.rerun()
        elif sub=="Encodage One-Hot":
            alert("ℹ️ Crée une colonne binaire par modalité.","i"); cols=st.multiselect("Colonnes",cc)
            if st.button("Appliquer") and cols:
                st.session_state.df=pd.get_dummies(df,columns=cols,dtype=int); H(f"Encodage One-Hot : {cols}"); alert("✅ Encodage appliqué !","s"); st.rerun()
        elif sub=="Renommer une colonne":
            col=st.selectbox("Colonne",df.columns.tolist()); nouveau=st.text_input("Nouveau nom")
            if st.button("Renommer") and nouveau.strip():
                st.session_state.df=df.rename(columns={col:nouveau.strip()}); H(f"Renommage : {col} -> {nouveau.strip()}"); alert("✅ Renommée !","s"); st.rerun()
        else:
            col=st.selectbox("Colonne",df.columns.tolist()); nt=st.selectbox("Type",["int","float","str","bool"])
            if st.button("Changer"):
                try:
                    df2=df.copy(); df2[col]=df2[col].astype(nt); st.session_state.df=df2; H(f"Type {col} -> {nt}"); alert("✅ Type modifié !","s"); st.rerun()
                except Exception as e: alert(f"❌ Erreur : {e}","e")
    with t5:
        cols=st.multiselect("Colonnes à supprimer",df.columns.tolist())
        if st.button("Supprimer") and cols:
            st.session_state.df=df.drop(columns=cols); H(f"Colonnes supprimées : {cols}"); alert("✅ Supprimées !","s"); st.rerun()
    with t6:
        if cn:
            col=st.selectbox("Colonne",cn,key="ff"); mn,mx=float(df[col].min()),float(df[col].max())
            plage=st.slider("Plage",mn,mx,(mn,mx)); dff=df[(df[col]>=plage[0])&(df[col]<=plage[1])]
            alert(f"ℹ️ <b>{len(dff):,}</b> lignes sur {len(df):,} correspondent au filtre.","i")
            st.dataframe(dff.head(30),use_container_width=True)
        tc=st.selectbox("Trier par",df.columns.tolist()); asc=st.radio("Ordre",["Ascendant","Descendant"],horizontal=True)=="Ascendant"
        st.dataframe(df.sort_values(tc,ascending=asc).head(30),use_container_width=True)
    st.markdown("<hr>",unsafe_allow_html=True)
    st.markdown('<div class="tag">Aperçu Avant / Après</div>',unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1: st.markdown("**Dataset original**"); st.dataframe(st.session_state.df0.head(8),use_container_width=True) if st.session_state.df0 is not None else None
    with c2: st.markdown("**Dataset actuel**"); st.dataframe(st.session_state.df.head(8),use_container_width=True)
    if st.button("🔄 Réinitialiser"):
        st.session_state.df=st.session_state.df0.copy(); H("Dataset réinitialisé"); alert("✅ Réinitialisé !","s"); st.rerun()

elif page == "📊  Visualisations":
    if st.session_state.df is None: alert("⚠️ Importez d'abord un fichier CSV.","w"); st.stop()
    ph("Etape 4","Visualisations Interactives","Créez et personnalisez vos graphiques.")
    df=st.session_state.df
    cn=df.select_dtypes(include=np.number).columns.tolist()
    cc=df.select_dtypes(exclude=np.number).columns.tolist()
    cc1,cm=st.columns([1,3])
    with cc1:
        st.markdown('<div class="glass" style="padding:20px">',unsafe_allow_html=True)
        tg=st.selectbox("Type de graphique",["Histogramme","Boxplot","Heatmap Corrélation","Nuage de points","Barres catégorielles","Pie chart","Graphique de lignes","Violin plot"])
        couleur=st.color_picker("Couleur","#00d4c8")
        st.markdown('</div>',unsafe_allow_html=True)
    with cm:
        fig=None
        if tg=="Histogramme" and cn:
            col=st.selectbox("Colonne",cn); bins=st.slider("Bins",5,100,35)
            fig=px.histogram(df,x=col,nbins=bins,title=f"Histogramme — {col}",color_discrete_sequence=[couleur])
            fig.update_traces(marker_line_width=0,opacity=0.85)
        elif tg=="Boxplot" and cn:
            col=st.selectbox("Colonne Y",cn); grp=st.selectbox("Grouper par",["Aucun"]+cc) if cc else "Aucun"
            fig=px.box(df,x=(grp if grp!="Aucun" else None),y=col,color=(grp if grp!="Aucun" else None),
                       color_discrete_sequence=[couleur],title=f"Boxplot — {col}")
        elif tg=="Heatmap Corrélation" and len(cn)>=2:
            fig=px.imshow(df[cn].corr(),text_auto=".2f",aspect="auto",title="Heatmap de Corrélation",
                          color_continuous_scale=["#050c18","#0891b2",couleur,"#e8f4f8"]); fig.update_layout(height=520)
        elif tg=="Nuage de points" and len(cn)>=2:
            xc=st.selectbox("Axe X",cn,key="vx"); yc=st.selectbox("Axe Y",cn,key="vy",index=min(1,len(cn)-1))
            hue=st.selectbox("Couleur par",["Aucun"]+cc) if cc else "Aucun"
            fig=px.scatter(df,x=xc,y=yc,color=(hue if hue!="Aucun" else None),opacity=0.75,title=f"{xc} vs {yc}",color_discrete_sequence=[couleur])
        elif tg=="Barres catégorielles" and cc:
            col=st.selectbox("Colonne",cc); vc=df[col].value_counts().reset_index(); vc.columns=["Valeur","Effectif"]
            fig=px.bar(vc,x="Valeur",y="Effectif",color="Effectif",color_continuous_scale=["#0a1628",couleur],title=f"Distribution — {col}")
        elif tg=="Pie chart" and cc:
            col=st.selectbox("Colonne",cc); vc=df[col].value_counts().reset_index(); vc.columns=["Valeur","Effectif"]
            fig=px.pie(vc,names="Valeur",values="Effectif",title=f"Répartition — {col}",hole=0.35,
                       color_discrete_sequence=["#00d4c8","#0891b2","#f59e0b","#10b981","#8b5cf6","#ef4444"])
        elif tg=="Graphique de lignes" and cn:
            col=st.selectbox("Colonne Y",cn)
            fig=px.line(df.reset_index(),x="index",y=col,title=f"Évolution — {col}",color_discrete_sequence=[couleur])
            fig.update_traces(line_width=2)
        elif tg=="Violin plot" and cn:
            col=st.selectbox("Colonne",cn); grp=st.selectbox("Grouper par",["Aucun"]+cc) if cc else "Aucun"
            fig=px.violin(df,x=(grp if grp!="Aucun" else None),y=col,color=(grp if grp!="Aucun" else None),
                          box=True,color_discrete_sequence=[couleur],title=f"Violin — {col}")
        if fig is not None:
            st.plotly_chart(T(fig),use_container_width=True)
            try:
                img=fig.to_image(format="png",width=1400,height=750,scale=2)
                st.download_button("📥 Télécharger PNG",img,file_name="graphique.png",mime="image/png")
            except: alert("ℹ️ Pour exporter en PNG : <code>pip install kaleido</code>","i")
        else: alert("ℹ️ Sélectionnez un graphique compatible avec vos colonnes.","i")

elif page == "💾  Exportation":
    if st.session_state.df is None: alert("⚠️ Importez d'abord un fichier CSV.","w"); st.stop()
    ph("Etape 5","Exportation des Résultats","Téléchargez vos données nettoyées et votre rapport.")
    df=st.session_state.df
    g="".join([kpi("Lignes finales",f"{df.shape[0]:,}","📋","c-cyan"),kpi("Colonnes",f"{df.shape[1]}","🗂️"),
               kpi("Manquantes",f"{df.isnull().sum().sum()}","❓","c-green" if df.isnull().sum().sum()==0 else "c-gold"),
               kpi("Actions",f"{len(st.session_state.hist)}","⚙️")])
    st.markdown(f'<div class="kpi-grid">{g}</div>',unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        st.markdown('<div class="glass">',unsafe_allow_html=True)
        st.markdown('<div class="tag">Dataset nettoyé</div>',unsafe_allow_html=True)
        st.download_button("⬇️ Télécharger en CSV",df.to_csv(index=False).encode("utf-8"),
                           file_name="dataset_nettoye.csv",mime="text/csv",use_container_width=True)
        try:
            buf=io.BytesIO()
            with pd.ExcelWriter(buf,engine="openpyxl") as w:
                df.to_excel(w,index=False,sheet_name="Données"); df.describe().T.round(3).to_excel(w,sheet_name="Statistiques")
            buf.seek(0)
            st.download_button("⬇️ Télécharger en Excel",buf,file_name="dataset_nettoye.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",use_container_width=True)
        except Exception as e: alert(f"❌ Erreur Excel : {e}","e")
        st.markdown('</div>',unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="glass">',unsafe_allow_html=True)
        st.markdown('<div class="tag">Statistiques et Rapport</div>',unsafe_allow_html=True)
        st.download_button("⬇️ Statistiques (CSV)",df.describe().T.round(3).to_csv().encode("utf-8"),
                           file_name="statistiques.csv",mime="text/csv",use_container_width=True)
        ht="\n".join([f"  [{h['t']}] {h['a']}" for h in st.session_state.hist]) or "  Aucun traitement."
        rapport=f"""RAPPORT D ANALYSE — MEDDATA ANALYZER
Universite Mohammed VI des Sciences et de la Sante (UM6SS)
Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Fichier : {st.session_state.fname}

INFORMATIONS GENERALES
  Lignes             : {df.shape[0]:,}
  Colonnes           : {df.shape[1]}
  Valeurs manquantes : {df.isnull().sum().sum()}
  Doublons           : {df.duplicated().sum()}
  Memoire            : {df.memory_usage(deep=True).sum()/1024:.2f} KB

COLONNES
{chr(10).join([f'  - {c} [{df[c].dtype}]' for c in df.columns])}

STATISTIQUES DESCRIPTIVES
{df.describe().round(3).to_string()}

HISTORIQUE DES TRAITEMENTS
{ht}
"""
        st.download_button("⬇️ Rapport complet (.txt)",rapport.encode("utf-8"),
                           file_name="rapport_analyse.txt",mime="text/plain",use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown("<hr>",unsafe_allow_html=True)
    st.markdown('<div class="tag">Aperçu du rapport</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="glass"><pre style="font-size:0.75rem;color:#7a9bb5;white-space:pre-wrap">{rapport[:2000]}</pre></div>',unsafe_allow_html=True)

elif page == "ℹ️  A propos":
    ph("Documentation","A propos","Informations sur MedData Analyzer — UM6SS Rabat.")
    c1,c2=st.columns([2,1])
    with c1:
        st.markdown('<div class="glass"><div class="tag">Description</div><p style="color:#b0cad8;line-height:1.8;font-size:0.9rem"><strong style="color:#e8f4f8">MedData Analyzer</strong> est une application web interactive développée dans le cadre du cours Sciences de Données Médicales par Python — 2ème Année Licence IDSD, Université Mohammed VI des Sciences et de la Santé (UM6SS), Rabat.</p></div>',unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="glass" style="text-align:center"><div style="font-size:3rem;margin-bottom:12px">🧬</div><div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:#e8f4f8">MedData Analyzer</div><div style="font-size:0.75rem;color:#00d4c8;letter-spacing:0.1em;text-transform:uppercase;margin:6px 0">Version 1.0</div><div style="font-size:0.78rem;color:#7a9bb5;margin-top:8px">UM6SS · IDSD · 2024-2025</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="tag">Stack technique</div>',unsafe_allow_html=True)
    cols=st.columns(3)
    for i,(ic,nm,ds) in enumerate([("🌐","Streamlit","Interface web interactive"),("🐼","Pandas","Manipulation des données"),("🔢","NumPy","Calculs numériques"),("📊","Plotly","Visualisations interactives"),("🎨","Matplotlib","Graphiques statiques"),("📗","OpenPyXL","Export Excel")]):
        with cols[i%3]:
            st.markdown(f'<div class="feat" style="margin-bottom:12px"><div class="fi">{ic}</div><div class="ft">{nm}</div><div class="fd">{ds}</div></div>',unsafe_allow_html=True)