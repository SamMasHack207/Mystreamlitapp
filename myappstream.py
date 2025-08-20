import streamlit as st 
import requests as r
import json
from datetime import datetime

# Configuration
base_url = "https://betting-bot-ja4l.onrender.com"

# Configuration de la page
st.set_page_config(
    page_title="Betting AI Agent", 
    page_icon="⚽",
    layout="wide"
)

st.title("🤖⚽ My Betting AI Agent")

# Sidebar pour la configuration globale
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Vérifier l'état de l'API
    try:
        health_response = r.get(f"{base_url}/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            st.success("✅ API connectée")
            
            # Afficher la config actuelle
            config = health_data.get("config", {})
            st.info(f"""
            **Configuration actuelle:**
            - Sport: {config.get('sport', 'N/A')}
            - Région: {config.get('region', 'N/A')}
            - Ligue: {config.get('league', 'N/A')}
            - Market: {config.get('market', 'N/A')}
            """)
        else:
            st.error("❌ API non accessible")
    except Exception as e:
        st.error(f"❌ Erreur de connexion: {str(e)}")

# Section Configuration
st.header("⚙️ Configuration")

col_a, col_b = st.columns(2)

with col_a:
    market = st.text_input("Market", value="h2h", placeholder="h2h, spreads, totals...")
    market_but = st.button("🔄 Changer Market", key="market_btn")
    if market_but and market:
        try:
            data = {"market": market}
            url = f"{base_url}/config/market"
            res = r.post(url, json=data, timeout=10)  # Utiliser json= au lieu de data=
            
            if res.status_code == 200:
                response_data = res.json()
                st.success(f"✅ {response_data.get('message', 'Market changé avec succès')}")
            else:
                st.error(f"❌ Erreur {res.status_code}: {res.text}")
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")
    
with col_b:        
    sport = st.text_input("Sport", value="soccer_epl", placeholder="soccer_epl, basketball_nba...")
    sport_but = st.button("🔄 Changer Sport", key="sport_btn")
    if sport_but and sport:
        try:
            data = {"sport": sport}
            url = f"{base_url}/config/sport"
            res = r.post(url, json=data, timeout=10)
            
            if res.status_code == 200:
                response_data = res.json()
                st.success(f"✅ {response_data.get('message', 'Sport changé avec succès')}")
            else:
                st.error(f"❌ Erreur {res.status_code}: {res.text}")
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")

col1, col2 = st.columns(2)

with col1:       
    region = st.text_input("Région", value="eu", placeholder="eu, us, uk, au...")
    reg_but = st.button("🔄 Changer Région", key="region_btn")
    if reg_but and region:
        try:
            data = {"region": region}
            url = f"{base_url}/config/region"
            res = r.post(url, json=data, timeout=10)
            
            if res.status_code == 200:
                response_data = res.json()
                st.success(f"✅ {response_data.get('message', 'Région changée avec succès')}")
            else:
                st.error(f"❌ Erreur {res.status_code}: {res.text}")
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")
     
with col2:
    league = st.number_input("Ligue", value=61, min_value=1)
    leag_but = st.button("🔄 Changer Ligue", key="league_btn")
    if leag_but:
        try:
            leag = int(league)
            data = {"league": leag}
            url = f"{base_url}/config/league"
            res = r.post(url, json=data, timeout=10)
            
            if res.status_code == 200:
                response_data = res.json()
                st.success(f"✅ {response_data.get('message', 'Ligue changée avec succès')}")
            else:
                st.error(f"❌ Erreur {res.status_code}: {res.text}")
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")

st.divider()

# Section Informations
st.header("📊 Informations")

col_info1, col_info2 = st.columns(2)

with col_info1:
    if st.button("📋 Voir tous les sports", key="sports_btn"):
        try:
            url = f"{base_url}/sports"
            res = r.get(url, timeout=10)
            
            if res.status_code == 200:
                sports_data = res.json()
                sports_list = sports_data.get("sports", "")
                
                with st.expander("🏆 Sports disponibles", expanded=True):
                    # Formatter la liste des sports
                    if sports_list:
                        lines = sports_list.split('\n')
                        for line in lines:
                            if line.strip() and '//' in line:
                                parts = line.split('//')
                                if len(parts) >= 2:
                                    code = parts[0].strip()
                                    title = parts[1].replace('titre:', '').strip()
                                    st.code(f"{code} → {title}")
                    else:
                        st.warning("Aucun sport trouvé")
            else:
                st.error(f"❌ Erreur {res.status_code}: {res.text}")
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")

with col_info2:
    if st.button("⚽ Voir les matches disponibles", key="matches_btn"):
        try:
            url = f"{base_url}/matches"
            res = r.get(url, timeout=15)  # Plus de temps pour cette requête
            
            if res.status_code == 200:
                matches_data = res.json()
                sport = matches_data.get("sport", "Unknown")
                matches = matches_data.get("matches", [])
                count = matches_data.get("count", 0)
                
                with st.expander(f"⚽ Matches disponibles ({sport}) - Total: {count}", expanded=True):
                    if matches:
                        for i, match in enumerate(matches):
                            with st.container():
                                col_home, col_vs, col_away = st.columns([3, 1, 3])
                                
                                with col_home:
                                    st.markdown(f"**🏠 {match.get('home_team', 'N/A')}**")
                                with col_vs:
                                    st.markdown("**VS**")
                                with col_away:
                                    st.markdown(f"**✈️ {match.get('away_team', 'N/A')}**")
                                
                                # Formater la date
                                commence_time = match.get('commence_time')
                                if commence_time:
                                    try:
                                        dt = datetime.fromisoformat(commence_time.replace('Z', '+00:00'))
                                        formatted_time = dt.strftime("%d/%m/%Y à %H:%M")
                                        st.caption(f"🕒 {formatted_time}")
                                    except:
                                        st.caption(f"🕒 {commence_time}")
                                
                                if i < len(matches) - 1:  # Pas de divider après le dernier
                                    st.divider()
                    else:
                        st.warning("Aucun match trouvé pour ce sport/région")
            else:
                st.error(f"❌ Erreur {res.status_code}: {res.text}")
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")

st.divider()

# Section Analyse
st.header("🎯 Analyse de Match")

analyse_match = st.text_input(
    "Entrer le match à analyser", 
    placeholder="Manchester City vs Liverpool",
    help="Format: équipe1 vs équipe2"
)

if st.button("🚀 Analyser le match", key="analyze_btn", type="primary"):
    if not analyse_match or " vs " not in analyse_match:
        st.error("❌ Format invalide. Utilisez: 'équipe1 vs équipe2'")
    else:
        try:
            # Validation du format
            teams = analyse_match.split(" vs ")
            if len(teams) != 2:
                st.error("❌ Format invalide. Utilisez exactement: 'équipe1 vs équipe2'")
            else:
                team1, team2 = [team.strip() for team in teams]
                
                if not team1 or not team2:
                    st.error("❌ Les noms d'équipes ne peuvent pas être vides")
                else:
                    # Afficher un spinner pendant l'analyse
                    with st.spinner(f"🔍 Analyse en cours pour {team1} vs {team2}..."):
                        url = f"{base_url}/analyze"
                        data = {"team1": team1, "team2": team2}
                        
                        # Augmenter le timeout pour l'analyse
                        res = r.post(url, json=data, timeout=60)
                        
                        if res.status_code == 200:
                            analysis_data = res.json()
                            
                            # Afficher les résultats
                            st.success("✅ Analyse terminée avec succès!")
                            
                            with st.container():
                                st.subheader(f"📊 Analyse: {analysis_data.get('match', 'N/A')}")
                                
                                # Afficher l'analyse dans un bloc formaté
                                analysis_text = analysis_data.get('analysis', 'Aucune analyse disponible')
                                st.markdown("### 🎯 Résultats de l'analyse:")
                                st.text_area("", analysis_text, height=400, disabled=True)
                                
                                # Informations supplémentaires
                                with st.expander("ℹ️ Détails de l'analyse"):
                                    config_used = analysis_data.get('config', {})
                                    st.json({
                                        "Sport": config_used.get('sport'),
                                        "Région": config_used.get('region'),
                                        "Market": config_used.get('market'),
                                        "Ligue": config_used.get('league')
                                    })
                                    
                                    missing_apis = analysis_data.get('missing_apis')
                                    if missing_apis:
                                        st.warning(f"⚠️ APIs manquantes: {', '.join(missing_apis)}")
                        else:
                            error_msg = "Erreur inconnue"
                            try:
                                error_data = res.json()
                                error_msg = error_data.get('error', res.text)
                            except:
                                error_msg = res.text
                            
                            st.error(f"❌ Erreur {res.status_code}: {error_msg}")
                            
        except Exception as e:
            st.error(f"❌ Erreur lors de l'analyse: {str(e)}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🤖 Betting AI Agent - Analyse sportive powered by IA</p>
    <p>⚡ API: betting-bot-ja4l.onrender.com</p>
</div>
""", unsafe_allow_html=True)
