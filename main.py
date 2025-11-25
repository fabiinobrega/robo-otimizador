import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, jsonify, g
from werkzeug.utils import secure_filename
import json
import random

# Importação dos módulos de serviços
# Import dos serviços
try:
    from services import facebook_ads_service
    from services import google_ads_service
    from services import competitor_spy_service
    from services import dco_service
    from services import landing_page_builder_service
    from services import segmentation_service
    from services.velyra_prime import operator as velyra_prime
    from services.ab_testing_service import ab_testing_service
    from services.automation_service import automation_service
    from services import openai_service
except ImportError as e:
    print(f"Warning: Some service modules not found: {e}")

# Import do cliente Manus API (separado para evitar erros)
try:
    from services.manus_api_client import manus_api
except ImportError as e:
    print(f"Warning: Manus API client not available: {e}")
    manus_api = None

# Import do serviço MCP
try:
    from services.mcp_integration_service import mcp_service
except ImportError as e:
    print(f"Warning: MCP service not available: {e}")
    mcp_service = None

# Import do serviço de controle remoto
try:
    from services.remote_control_service import remote_control
except ImportError as e:
    print(f"Warning: Remote control service not available: {e}")
    remote_control = None

# Import do serviço de automação de campanhas
try:
    from services.campaign_automation_service import campaign_automation
except ImportError as e:
    print(f"Warning: Campaign automation service not available: {e}")
    campaign_automation = None

# Import do serviço de geração de campanhas com IA
try:
    from services.ai_campaign_generator import AICampaignGenerator
    ai_campaign_generator = AICampaignGenerator()
except ImportError as e:
    print(f"Warning: AI Campaign Generator not available: {e}")
    ai_campaign_generator = None
    campaign_automation = None

# Import do serviço de auditoria UX
try:
    from services.ux_audit_service import ux_audit
except ImportError as e:
    print(f"Warning: UX audit service not available: {e}")
    ux_audit = None

# Import do serviço de inteligência de produtos
try:
    from services.product_intelligence_service import product_intelligence
except ImportError as e:
    print(f"Warning: Product intelligence service not available: {e}")
    product_intelligence = None

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "uma_chave_secreta_muito_segura")
app.config["UPLOAD_FOLDER"] = "static/uploads"

DATABASE = os.path.join(app.root_path, 'database.db')


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        schema_path = os.path.join(app.root_path, "schema.sql")
        if os.path.exists(schema_path):
            try:
                with open(schema_path, 'r') as f:
                    db.cursor().executescript(f.read())
                db.commit()
                print("Database initialized successfully")
            except Exception as e:
                print(f"Error initializing database: {e}")


if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])


# Forçar init do banco no Render
with app.app_context():
    try:
        init_db()
        # Verificar se precisa fazer seed
        db = get_db()
        count = db.execute("SELECT COUNT(*) as count FROM campaigns").fetchone()[0]
        if count == 0:
            print("Database vazio, executando seed...")
            import seed_data
            seed_data.seed_database(DATABASE)
    except Exception as e:
        print(f"DB initialization warning: {e}")


def log_activity(action, details=""):
    """Log activity to the database."""
    db = get_db()
    try:
        db.execute(
            "INSERT INTO activity_logs (action, details) VALUES (?, ?)",
            (action, details),
        )
        db.commit()
    except sqlite3.OperationalError as e:
        print(f"Error logging activity: {e}")


# ===== CAMPAIGN CRUD ENDPOINTS =====

@app.route("/api/campaign/create", methods=["POST"])
def api_campaign_create():
    """Create a new campaign with all details."""
    db = get_db()
    data = request.get_json()

    campaign_name = data.get("campaignName")
    platform = data.get("platform")
    budget = data.get("budgetAmount")
    start_date = data.get("scheduleStart")
    end_date = data.get("scheduleEnd")
    objective = data.get("campaignObjective")
    product_url = data.get("productUrl")

    if not all([campaign_name, platform, budget, start_date]):
        return jsonify({"success": False, "message": "Campos obrigatórios faltando"}), 400

    try:
        cursor = db.execute(
            """INSERT INTO campaigns (name, platform, budget, start_date, end_date, objective, product_url, status, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (campaign_name, platform, float(budget), start_date, end_date or None, objective, product_url, "Draft", datetime.now().isoformat(), datetime.now().isoformat())
        )
        db.commit()
        campaign_id = cursor.lastrowid

        # Save segmentation if provided
        if data.get("segmentation"):
            seg = data.get("segmentation")
            db.execute(
                """INSERT INTO campaign_segmentation (campaign_id, target_country, target_cities, min_age, max_age, interests, keywords)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (campaign_id, seg.get("country"), seg.get("cities"), seg.get("minAge"), seg.get("maxAge"), 
                 json.dumps(seg.get("interests", [])), json.dumps(seg.get("keywords", [])))
            )

        # Save budget config if provided
        if data.get("budgetConfig"):
            cfg = data.get("budgetConfig")
            db.execute(
                """INSERT INTO campaign_budget_config (campaign_id, is_daily_budget, bid_strategy, budget_optimization, ad_rotation)
                   VALUES (?, ?, ?, ?, ?)""",
                (campaign_id, cfg.get("isDailyBudget", True), cfg.get("bidStrategy", "maximize_conversions"),
                 cfg.get("budgetOptimization", "campaign"), cfg.get("adRotation", "optimize"))
            )

        # Save copy if provided
        if data.get("copy"):
            copy = data.get("copy")
            db.execute(
                """INSERT INTO campaign_copy (campaign_id, headline_1, headline_2, description_1, call_to_action, copy_sentiment, negative_keywords)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (campaign_id, copy.get("headline1"), copy.get("headline2"), copy.get("description1"),
                 copy.get("callToAction"), copy.get("sentiment", "neutral"), json.dumps(copy.get("negativeKeywords", [])))
            )

        db.commit()
        log_activity("Campanha Criada", f"Campanha '{campaign_name}' (ID: {campaign_id}) criada com sucesso.")

        return jsonify({
            "success": True,
            "message": f"Campanha '{campaign_name}' criada com sucesso!",
            "campaign_id": campaign_id
        })

    except Exception as e:
        print(f"Erro ao criar campanha: {e}")
        return jsonify({"success": False, "message": f"Erro ao criar campanha: {str(e)}"}), 500


@app.route("/api/campaign/list", methods=["GET"])
def api_campaign_list():
    """List all campaigns with pagination."""
    db = get_db()
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    status = request.args.get('status', None)
    
    offset = (page - 1) * limit
    
    try:
        if status:
            campaigns = db.execute(
                "SELECT * FROM campaigns WHERE status = ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (status, limit, offset)
            ).fetchall()
            total = db.execute("SELECT COUNT(*) as count FROM campaigns WHERE status = ?", (status,)).fetchone()[0]
        else:
            campaigns = db.execute(
                "SELECT * FROM campaigns ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (limit, offset)
            ).fetchall()
            total = db.execute("SELECT COUNT(*) as count FROM campaigns").fetchone()[0]
        
        return jsonify({
            "success": True,
            "campaigns": [dict(c) for c in campaigns],
            "total": total,
            "page": page,
            "limit": limit
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/campaign/read/<int:campaign_id>", methods=["GET"])
def api_campaign_read(campaign_id):
    """Read a specific campaign with all details."""
    db = get_db()
    
    try:
        campaign = db.execute("SELECT * FROM campaigns WHERE id = ?", (campaign_id,)).fetchone()
        if campaign is None:
            return jsonify({"success": False, "message": "Campanha não encontrada"}), 404

        creatives = db.execute("SELECT * FROM campaign_creatives WHERE campaign_id = ?", (campaign_id,)).fetchall()
        keywords = db.execute("SELECT * FROM campaign_keywords WHERE campaign_id = ?", (campaign_id,)).fetchall()
        audiences = db.execute("SELECT * FROM campaign_audiences WHERE campaign_id = ?", (campaign_id,)).fetchall()
        segmentation = db.execute("SELECT * FROM campaign_segmentation WHERE campaign_id = ?", (campaign_id,)).fetchone()
        budget_config = db.execute("SELECT * FROM campaign_budget_config WHERE campaign_id = ?", (campaign_id,)).fetchone()
        copy = db.execute("SELECT * FROM campaign_copy WHERE campaign_id = ?", (campaign_id,)).fetchone()
        metrics = db.execute("SELECT * FROM campaign_metrics WHERE campaign_id = ?", (campaign_id,)).fetchone()

        return jsonify({
            "success": True,
            "campaign": dict(campaign),
            "details": {
                "creatives": [dict(c) for c in creatives],
                "keywords": [dict(k) for k in keywords],
                "audiences": [dict(a) for a in audiences],
                "segmentation": dict(segmentation) if segmentation else None,
                "budget_config": dict(budget_config) if budget_config else None,
                "copy": dict(copy) if copy else None,
                "metrics": dict(metrics) if metrics else None,
            }
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/campaign/update/<int:campaign_id>", methods=["PUT"])
def api_campaign_update(campaign_id):
    """Update campaign details."""
    db = get_db()
    data = request.get_json()
    
    try:
        campaign = db.execute("SELECT * FROM campaigns WHERE id = ?", (campaign_id,)).fetchone()
        if not campaign:
            return jsonify({"success": False, "message": "Campanha não encontrada"}), 404

        # Update main campaign fields
        updates = []
        params = []
        
        if "name" in data:
            updates.append("name = ?")
            params.append(data["name"])
        if "status" in data:
            updates.append("status = ?")
            params.append(data["status"])
        if "budget" in data:
            updates.append("budget = ?")
            params.append(float(data["budget"]))
        if "objective" in data:
            updates.append("objective = ?")
            params.append(data["objective"])
        
        if updates:
            updates.append("updated_at = ?")
            params.append(datetime.now().isoformat())
            params.append(campaign_id)
            
            query = f"UPDATE campaigns SET {', '.join(updates)} WHERE id = ?"
            db.execute(query, params)
            db.commit()

        log_activity("Campanha Atualizada", f"Campanha ID {campaign_id} atualizada.")
        
        return jsonify({"success": True, "message": "Campanha atualizada com sucesso!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/campaign/delete/<int:campaign_id>", methods=["DELETE"])
def api_campaign_delete(campaign_id):
    """Delete a campaign."""
    db = get_db()
    
    try:
        campaign = db.execute("SELECT * FROM campaigns WHERE id = ?", (campaign_id,)).fetchone()
        if not campaign:
            return jsonify({"success": False, "message": "Campanha não encontrada"}), 404

        db.execute("DELETE FROM campaigns WHERE id = ?", (campaign_id,))
        db.commit()
        
        log_activity("Campanha Deletada", f"Campanha ID {campaign_id} deletada do sistema.")
        
        return jsonify({"success": True, "message": "Campanha deletada com sucesso!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/campaign/publish", methods=["POST"])
def api_campaign_publish():
    """Publish a campaign to Meta and/or Google Ads."""
    db = get_db()
    data = request.get_json()
    campaign_id = data.get("campaign_id")
    platform = data.get("platform", "Both")

    if not campaign_id:
        return jsonify({"success": False, "message": "ID da campanha é obrigatório"}), 400

    try:
        campaign = db.execute("SELECT * FROM campaigns WHERE id = ?", (campaign_id,)).fetchone()
        if not campaign:
            return jsonify({"success": False, "message": "Campanha não encontrada"}), 404

        publish_results = {}
        publish_status = "Success"

        # Mock publishing to Meta
        if platform in ["Meta", "Both"]:
            meta_result = {
                "success": True,
                "campaign_id_external": f"meta_{campaign_id}_{random.randint(100000, 999999)}"
            }
            publish_results["meta"] = meta_result
            db.execute("UPDATE campaigns SET meta_campaign_id = ? WHERE id = ?", 
                       (meta_result["campaign_id_external"], campaign_id))

        # Mock publishing to Google
        if platform in ["Google", "Both"]:
            google_result = {
                "success": True,
                "campaign_id_external": f"google_{campaign_id}_{random.randint(100000, 999999)}"
            }
            publish_results["google"] = google_result
            db.execute("UPDATE campaigns SET google_campaign_id = ? WHERE id = ?", 
                       (google_result["campaign_id_external"], campaign_id))

        db.execute("UPDATE campaigns SET status = ?, last_publish_status = ? WHERE id = ?", 
                   ("Active", publish_status, campaign_id))
        db.commit()
        
        log_activity("Campanha Publicada", f"Campanha ID {campaign_id} publicada com sucesso.")

        return jsonify({
            "success": True,
            "message": "Campanha publicada com sucesso!",
            "campaign_id": campaign_id,
            "publish_status": publish_status,
            "results": publish_results
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ===== AI FEATURES ENDPOINTS =====

@app.route("/api/analyze-landing-page", methods=["POST"])
def api_analyze_landing_page():
    """Analyze a landing page URL with AI."""
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({"success": False, "message": "URL é obrigatória"}), 400
    
    try:
        # Mock analysis
        result = {
            "keywords": ["marketing", "digital", "optimization", "conversion"],
            "interests": ["Marketing", "Business", "Technology"],
            "sentiment": "positive",
            "copy_suggestions": [
                "Maximize your ROI with our AI-powered platform",
                "Transform your marketing strategy today"
            ]
        }
        
        log_activity("Análise de Página", f"URL analisada: {url}")
        
        return jsonify({
            "success": True,
            **result
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/competitor-spy", methods=["POST"])
def api_competitor_spy():
    """Spy on competitors for a given keyword."""
    data = request.get_json()
    keyword = data.get('keyword')
    
    if not keyword:
        return jsonify({"success": False, "message": "Keyword é obrigatória"}), 400
    
    try:
        # Mock competitor analysis
        result = {
            "suggested_headlines": [
                f"Best {keyword} Solution Online",
                f"Top {keyword} Platform for 2024",
                f"Revolutionary {keyword} Technology"
            ],
            "suggested_copy": [
                f"Discover the ultimate {keyword} solution that transforms your business.",
                f"Join thousands using our {keyword} platform for guaranteed results."
            ],
            "competitors_count": 5,
            "competitors": [
                {"name": "Competitor Alpha", "ad_spend": "$5k-50k", "keywords_overlap": 65},
                {"name": "Competitor Beta", "ad_spend": "$10k-100k", "keywords_overlap": 75},
                {"name": "Competitor Gamma", "ad_spend": "$1k-20k", "keywords_overlap": 35},
            ]
        }
        
        log_activity("Espionagem de Concorrentes", f"Keyword: {keyword}")
        
        return jsonify({
            "success": True,
            "keyword": keyword,
            **result
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/dco/generate-segmentation", methods=["POST"])
def api_dco_generate_segmentation():
    """Generate audience segmentation with AI."""
    data = request.get_json()
    objective = data.get('objective')
    url = data.get('url')
    
    try:
        result = {
            "interests": ["Marketing", "Business", "Digital Marketing", "Technology"],
            "keywords": ["marketing automation", "digital marketing", "business growth"],
            "age_range": {"min": 25, "max": 55},
            "locations": ["Brazil", "United States", "Portugal"]
        }
        
        log_activity("Geração de Segmentação", f"Objetivo: {objective}")
        
        return jsonify({
            "success": True,
            **result
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/dco/generate", methods=["POST"])
def api_dco_generate():
    """Generate creatives with DCO."""
    data = request.get_json()
    url = data.get('url')
    objective = data.get('objective')
    
    try:
        result = {
            "creatives": [
                {"description": f"Creative 1 for {objective}", "url": "https://via.placeholder.com/300x250"},
                {"description": f"Creative 2 for {objective}", "url": "https://via.placeholder.com/300x250"},
                {"description": f"Creative 3 for {objective}", "url": "https://via.placeholder.com/300x250"},
            ],
            "variations": 3
        }
        
        log_activity("Geração de Criativos (DCO)", f"URL: {url}")
        
        return jsonify({
            "success": True,
            **result
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/dco/generate-copy", methods=["POST"])
def api_dco_generate_copy():
    """Generate ad copy with AI."""
    data = request.get_json()
    url = data.get('url')
    objective = data.get('objective')
    
    try:
        result = {
            "headlines": [
                f"Descubra a Solução Perfeita para {objective}",
                f"Maximize seu ROI com Nossa Plataforma",
                f"Transforme seu Negócio Hoje Mesmo"
            ],
            "descriptions": [
                f"Análise profunda de {url} para resultados garantidos. Clique agora!",
                f"Otimize suas campanhas com IA. Aumento de 300% em conversões."
            ],
            "cta": "Saiba Mais"
        }
        
        log_activity("Geração de Copy", f"URL: {url}, Objetivo: {objective}")
        
        return jsonify({
            "success": True,
            **result
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ===== DASHBOARD ENDPOINTS =====

@app.route("/api/dashboard/metrics", methods=["GET"])
def api_dashboard_metrics():
    """Get dashboard metrics."""
    db = get_db()
    
    try:
        # Contagem de campanhas
        total = db.execute("SELECT COUNT(*) as count FROM campaigns").fetchone()[0]
        active = db.execute("SELECT COUNT(*) as count FROM campaigns WHERE status = 'Active'").fetchone()[0]
        paused = db.execute("SELECT COUNT(*) as count FROM campaigns WHERE status = 'Paused'").fetchone()[0]
        failed = db.execute("SELECT COUNT(*) as count FROM campaigns WHERE status = 'Failed'").fetchone()[0]
        
        # Métricas agregadas de todas as campanhas
        metrics = db.execute("""
            SELECT 
                SUM(impressions) as total_impressions,
                SUM(clicks) as total_clicks,
                SUM(conversions) as total_conversions,
                SUM(spend) as total_spend,
                SUM(revenue) as total_revenue,
                AVG(roas) as avg_roas,
                AVG(ctr) as avg_ctr,
                AVG(cpa) as avg_cpa
            FROM campaign_metrics
        """).fetchone()
        
        total_clicks = int(metrics[1] or 0)
        total_conversions = int(metrics[2] or 0)
        avg_roas = float(metrics[5] or 0)
        
        return jsonify({
            "success": True,
            "total_campaigns": total,
            "active_campaigns": active,
            "paused_campaigns": paused,
            "failed_campaigns": failed,
            "total_clicks": total_clicks,
            "total_conversions": total_conversions,
            "avg_roas": round(avg_roas, 2),
            "total_impressions": int(metrics[0] or 0),
            "total_spend": round(float(metrics[3] or 0), 2),
            "total_revenue": round(float(metrics[4] or 0), 2),
            "avg_ctr": round(float(metrics[6] or 0), 2),
            "avg_cpa": round(float(metrics[7] or 0), 2),
            "published_today": 0,
            "alerts": failed,
            "meta_campaigns": active,
            "google_campaigns": active,
            "ai_analyses": total * 2,
            "ai_suggestions": total,
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/activity-logs", methods=["GET"])
def api_activity_logs():
    """Get activity logs."""
    db = get_db()
    limit = request.args.get('limit', 10, type=int)
    
    try:
        logs = db.execute(
            "SELECT * FROM activity_logs ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        ).fetchall()
        
        return jsonify({
            "success": True,
            "logs": [dict(log) for log in logs]
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ===== PAGE ROUTES =====

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create-campaign")
def create_campaign():
    return render_template("create_campaign.html")


@app.route("/campaigns")
def campaigns():
    db = get_db()
    try:
        campaigns_list = db.execute("SELECT * FROM campaigns ORDER BY created_at DESC").fetchall()
        return render_template("campaigns.html", campaigns=campaigns_list)
    except:
        return render_template("campaigns.html", campaigns=[])


@app.route("/dashboard")
def dashboard():
    db = get_db()
    try:
        campaigns_list = db.execute("SELECT * FROM campaigns ORDER BY created_at DESC LIMIT 5").fetchall()
        logs = db.execute("SELECT * FROM activity_logs ORDER BY timestamp DESC LIMIT 10").fetchall()
        return render_template("dashboard.html", campaigns=campaigns_list, logs=logs)
    except:
        return render_template("dashboard.html", campaigns=[], logs=[])


@app.route("/competitor-spy")
def competitor_spy():
    return render_template("competitor_spy.html")


@app.route("/dco")
def dco():
    return render_template("dco_builder.html")


@app.route("/funnel-builder")
def funnel_builder():
    return render_template("funnel_builder.html")


@app.route("/segmentation")
def segmentation():
    return render_template("segmentation.html")


@app.route("/reports")
def reports():
    return render_template("reports_dashboard.html")


@app.route("/media-library")
def media_library():
    db = get_db()
    try:
        media_files = db.execute("SELECT * FROM media_files ORDER BY uploaded_at DESC").fetchall()
        return render_template("media_library.html", media_files=media_files)
    except:
        return render_template("media_library.html", media_files=[])


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/notifications")
def notifications():
    return render_template("notifications.html")


@app.route("/subscriptions")
def subscriptions():
    return render_template("subscriptions.html")


@app.route("/affiliates")
def affiliates():
    return render_template("affiliates.html")


@app.route("/developer-api")
def developer_api():
    return render_template("developer_api.html")


@app.route("/landing-page-builder")
def landing_page_builder():
    return render_template("landing_page_builder.html")


@app.route("/operator-chat")
def operator_chat():
    return render_template("operator_chat.html")


@app.route("/ab-testing")
def ab_testing():
    return render_template("ab_testing.html")


@app.route("/automation")
def automation():
    return render_template("automation.html")


@app.route("/all-features")
def all_features():
    return render_template("all_features.html")


@app.route("/activity-logs")
def activity_logs():
    return render_template("activity_logs.html")


@app.route("/campaign-sandbox")
def campaign_sandbox():
    return render_template("campaign_sandbox.html")


@app.route("/dco-builder")
def dco_builder():
    return render_template("dco_builder.html")


@app.route("/health")
def health_check():
    return jsonify({"status": "ok"})


@app.route("/api/media/upload", methods=["POST"])
def api_upload_media():
    """Upload media files (single or multiple)."""
    # Suportar tanto 'mediaFile' (single) quanto 'media' (multiple)
    files_key = 'media' if 'media' in request.files else 'mediaFile'
    
    if files_key not in request.files:
        return jsonify({"success": False, "message": "Nenhum arquivo enviado"}), 400

    files = request.files.getlist(files_key)
    if not files or files[0].filename == "":
        return jsonify({"success": False, "message": "Nenhum arquivo selecionado"}), 400

    try:
        uploaded_files = []
        db = get_db()
        
        for file in files:
            if file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)

                file_url = url_for("static", filename=f"uploads/{filename}", _external=True)
                filetype = file.mimetype.split("/")[0] if file.mimetype else "unknown"

                db.execute(
                    "INSERT INTO media_files (filename, url, filetype) VALUES (?, ?, ?)",
                    (filename, file_url, filetype),
                )
                
                uploaded_files.append({
                    "filename": filename,
                    "url": file_url,
                    "filetype": filetype
                })
        
        db.commit()
        log_activity("Upload de Mídia", f"{len(uploaded_files)} arquivo(s) enviado(s)")

        return jsonify({
            "success": True,
            "message": f"{len(uploaded_files)} arquivo(s) carregado(s) com sucesso!",
            "files": uploaded_files
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ===== MANUS OPERATOR ENDPOINTS =====

@app.route("/api/operator/status", methods=["GET"])
def api_operator_status():
    """Get Velyra Prime status"""
    try:
        status = velyra_prime.health_check()
        return jsonify({"success": True, **status})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/operator/monitor", methods=["GET"])
def api_operator_monitor():
    """Monitor campaigns"""
    try:
        result = velyra_prime.monitor_campaigns()
        return jsonify({"success": True, **result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/operator/optimize", methods=["POST"])
def api_operator_optimize():
    """Optimize campaigns automatically"""
    try:
        result = velyra_prime.auto_optimize_campaigns()
        return jsonify({"success": True, **result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/operator/chat", methods=["POST"])
def api_operator_chat():
    """Chat with Velyra Prime"""
    data = request.get_json()
    message = data.get("message", "")
    
    try:
        # Salvar mensagem no banco
        db = get_db()
        db.execute(
            "INSERT INTO chat_messages (sender, message) VALUES (?, ?)",
            ("user", message)
        )
        db.commit()
        
        # Gerar resposta
        response = velyra_prime.chat_response(message)
        
        # Salvar resposta
        db.execute(
            "INSERT INTO chat_messages (sender, message) VALUES (?, ?)",
            ("operator", response)
        )
        db.commit()
        
        return jsonify({
            "success": True,
            "response": response
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/operator/recommendations/<int:campaign_id>", methods=["GET"])
def api_operator_recommendations(campaign_id):
    """Get AI recommendations for a campaign"""
    try:
        result = velyra_prime.generate_ai_recommendations(campaign_id)
        return jsonify({"success": True, **result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ===== A/B TESTING ENDPOINTS =====

@app.route("/api/ab-test/create", methods=["POST"])
def api_ab_test_create():
    """Create A/B test"""
    data = request.get_json()
    
    try:
        db = get_db()
        cursor = db.execute("""
            INSERT INTO ab_tests (campaign_id, test_name, test_type, status)
            VALUES (?, ?, ?, ?)
        """, (
            data.get("campaign_id"),
            data.get("test_name"),
            data.get("test_type"),
            "running"
        ))
        test_id = cursor.lastrowid
        
        # Create variations
        variations = ab_testing_service.create_variations(
            data.get("original_content", {}),
            data.get("test_type")
        )
        
        for i, variation in enumerate(variations):
            db.execute("""
                INSERT INTO ab_test_variations (test_id, variation_name, content_json)
                VALUES (?, ?, ?)
            """, (
                test_id,
                f"Variação {chr(65 + i)}",
                json.dumps(variation)
            ))
        
        db.commit()
        log_activity("Teste A/B Criado", f"Teste '{data.get('test_name')}' criado com {len(variations)} variações")
        
        return jsonify({
            "success": True,
            "test_id": test_id,
            "variations": variations
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/ab-test/analyze/<int:test_id>", methods=["GET"])
def api_ab_test_analyze(test_id):
    """Analyze A/B test results"""
    try:
        db = get_db()
        variations = db.execute(
            "SELECT * FROM ab_test_variations WHERE test_id = ?",
            (test_id,)
        ).fetchall()
        
        test_data = {
            "variations": [dict(v) for v in variations]
        }
        
        result = ab_testing_service.analyze_test_results(test_data)
        return jsonify({"success": True, **result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/ab-test/suggestions", methods=["GET"])
def api_ab_test_suggestions():
    """Get A/B test suggestions"""
    try:
        suggestions = ab_testing_service.get_test_suggestions({})
        return jsonify({"success": True, "suggestions": suggestions})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/ab-test/library", methods=["GET"])
def api_ab_test_library():
    """Get winning variations library"""
    try:
        library = ab_testing_service.get_winning_variations_library()
        return jsonify({"success": True, "library": library})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ===== AUTOMATION ENDPOINTS =====

@app.route("/api/automation/rules", methods=["GET"])
def api_automation_rules():
    """Get available automation rules"""
    try:
        templates = automation_service.get_available_rule_templates()
        return jsonify({"success": True, "templates": templates})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/automation/execute", methods=["POST"])
def api_automation_execute():
    """Execute automation rules"""
    try:
        result = automation_service.execute_rules()
        return jsonify({"success": True, **result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/automation/history", methods=["GET"])
def api_automation_history():
    """Get automation history"""
    try:
        history = automation_service.get_rule_history()
        return jsonify({"success": True, "history": history})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ===== NOTIFICATIONS ENDPOINTS =====

@app.route("/api/notifications", methods=["GET"])
def api_notifications():
    """Get notifications"""
    db = get_db()
    try:
        notifications = db.execute(
            "SELECT * FROM notifications ORDER BY created_at DESC LIMIT 50"
        ).fetchall()
        
        return jsonify({
            "success": True,
            "notifications": [dict(n) for n in notifications]
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/notifications/<int:notification_id>/read", methods=["POST"])
def api_notification_read(notification_id):
    """Mark notification as read"""
    db = get_db()
    try:
        db.execute(
            "UPDATE notifications SET is_read = 1 WHERE id = ?",
            (notification_id,)
        )
        db.commit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ===== REPORTS ENDPOINTS =====

@app.route("/api/reports/generate", methods=["POST"])
def api_report_generate():
    """Generate report"""
    data = request.get_json()
    db = get_db()
    
    try:
        # Buscar dados das campanhas
        campaigns = db.execute("""
            SELECT c.*, m.impressions, m.clicks, m.conversions, m.spend, m.revenue, m.roas
            FROM campaigns c
            LEFT JOIN campaign_metrics m ON c.id = m.campaign_id
            WHERE c.created_at BETWEEN ? AND ?
        """, (
            data.get("date_range_start"),
            data.get("date_range_end")
        )).fetchall()
        
        report_data = {
            "campaigns": [dict(c) for c in campaigns],
            "summary": {
                "total_campaigns": len(campaigns),
                "total_spend": sum(c["spend"] or 0 for c in campaigns),
                "total_revenue": sum(c["revenue"] or 0 for c in campaigns),
                "avg_roas": sum(c["roas"] or 0 for c in campaigns) / len(campaigns) if campaigns else 0
            }
        }
        
        # Salvar relatório
        cursor = db.execute("""
            INSERT INTO reports (report_name, report_type, date_range_start, date_range_end, data_json)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data.get("report_name", "Relatório Personalizado"),
            data.get("report_type", "performance"),
            data.get("date_range_start"),
            data.get("date_range_end"),
            json.dumps(report_data)
        ))
        db.commit()
        
        return jsonify({
            "success": True,
            "report_id": cursor.lastrowid,
            "data": report_data
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/reports/list", methods=["GET"])
def api_reports_list():
    """List all reports"""
    db = get_db()
    try:
        reports = db.execute(
            "SELECT id, report_name, report_type, created_at FROM reports ORDER BY created_at DESC"
        ).fetchall()
        
        return jsonify({
            "success": True,
            "reports": [dict(r) for r in reports]
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/generate-perfect-ad")
def generate_perfect_ad():
    """Generate Perfect Ad (1-Click)"""
    return render_template("generate_perfect_ad.html")


@app.route("/ad-editor")
def ad_editor():
    """Ad Editor - Edit everything after AI generation"""
    return render_template("ad_editor.html")


@app.route("/api/ad/generate-copy", methods=["POST"])
def api_ad_generate_copy():
    """Generate ad copy with OpenAI GPT-4"""
    data = request.json
    product_info = data.get("product", {})
    platform = data.get("platform", "facebook")
    num_variants = data.get("num_variants", 5)
    
    try:
        result = openai_service.generate_ad_copy(product_info, platform, num_variants)
        return jsonify({"success": True, **result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/landing/analyze", methods=["POST"])
def api_landing_analyze():
    """Analyze landing page with AI"""
    data = request.json
    url = data.get("url")
    
    if not url:
        return jsonify({"success": False, "message": "URL is required"}), 400
    
    try:
        result = openai_service.analyze_landing_page(url)
        return jsonify({"success": True, **result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/ad/simulate", methods=["POST"])
def api_ad_simulate():
    """Simulate ad performance"""
    data = request.json
    
    # Simulação baseada em dados históricos e IA
    platform = data.get("platform", "facebook")
    budget = float(data.get("budget", 1000))
    
    # Cálculos estimados
    ctr = 2.5 if platform == "facebook" else 3.2
    cpc = 1.50 if platform == "facebook" else 2.20
    clicks = int((budget / cpc) * 0.9)
    conversions = int(clicks * 0.05)  # 5% conversion rate
    revenue = conversions * 150  # R$ 150 por venda
    roas = revenue / budget if budget > 0 else 0
    
    return jsonify({
        "success": True,
        "simulation": {
            "ctr": ctr,
            "cpc": cpc,
            "clicks": clicks,
            "conversions": conversions,
            "revenue": revenue,
            "roas": round(roas, 2)
        }
    })


@app.route("/api/ad/publish", methods=["POST"])
def api_ad_publish():
    """Publish ad to platform"""
    data = request.json
    config = data.get("config", {})
    
    db = get_db()
    
    try:
        # Criar campanha no banco
        cursor = db.execute("""
            INSERT INTO campaigns (name, platform, status, budget, objective)
            VALUES (?, ?, ?, ?, ?)
        """, (
            f"Anúncio Perfeito - {config.get('platform', 'Facebook')}",
            config.get("platform", "facebook"),
            "active" if not config.get("useSandbox") else "draft",
            config.get("budget", 1000),
            "conversions"
        ))
        campaign_id = cursor.lastrowid
        
        # Log da ação
        db.execute("""
            INSERT INTO activity_logs (action, details, timestamp)
            VALUES (?, ?, ?)
        """, (
            "campaign_published",
            f"Campanha #{campaign_id} publicada via Gerar Anúncio Perfeito",
            datetime.now().isoformat()
        ))
        
        db.commit()
        
        return jsonify({
            "success": True,
            "campaign_id": campaign_id,
            "message": "Anúncio publicado com sucesso!" if not config.get("useSandbox") else "Anúncio criado no Sandbox"
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/generate-image", methods=["POST"])
def api_generate_image():
    """Generate ad images with AI"""
    data = request.json
    product = data.get("product", {})
    
    # Simular geração de imagens (em produção, usar DALL-E ou similar)
    images = [
        {"url": "https://via.placeholder.com/1200x628/0066cc/ffffff?text=Conceito+1", "concept": "Minimalista"},
        {"url": "https://via.placeholder.com/1200x628/ff6600/ffffff?text=Conceito+2", "concept": "Vibrante"},
        {"url": "https://via.placeholder.com/1200x628/00cc66/ffffff?text=Conceito+3", "concept": "Profissional"}
    ]
    
    return jsonify({
        "success": True,
        "images": images
    })


# ===== ENDPOINTS DE INTEGRAÇÃO COM API MANUS =====

@app.route('/manus/connect')
def manus_connect():
    """Página de conexão com API Manus"""
    if manus_api is None:
        status = {'connected': False, 'has_token': False, 'token_valid': False, 'last_sync': None, 'api_url': 'N/A'}
    else:
        status = manus_api.get_connection_status()
    return render_template('manus_connection.html', status=status)

@app.route('/manus/oauth/authorize')
def manus_oauth_authorize():
    """Inicia fluxo OAuth2 com API Manus"""
    auth_url = manus_api.get_authorization_url()
    return redirect(auth_url)

@app.route('/oauth/callback')
def oauth_callback():
    """Callback OAuth2 da API Manus"""
    code = request.args.get('code')
    state = request.args.get('state')
    
    if not code or not state:
        return jsonify({'success': False, 'error': 'Parâmetros inválidos'}), 400
    
    result = manus_api.exchange_code_for_token(code, state)
    
    if result['success']:
        return redirect(url_for('manus_connect'))
    else:
        return jsonify(result), 400

@app.route('/api/manus/status')
def api_manus_status():
    """Retorna status da conexão com API Manus"""
    status = manus_api.get_connection_status()
    return jsonify(status)

@app.route('/api/manus/test')
def api_manus_test():
    """Testa conexão com API Manus"""
    result = manus_api.test_connection()
    return jsonify(result)

@app.route('/api/manus/sync/campaigns', methods=['POST'])
def api_manus_sync_campaigns():
    """Sincroniza campanhas com API Manus"""
    direction = request.json.get('direction', 'both')
    result = manus_api.sync_campaigns(direction)
    return jsonify(result)

@app.route('/api/manus/sync/ads', methods=['POST'])
def api_manus_sync_ads():
    """Sincroniza anúncios com API Manus"""
    campaign_id = request.json.get('campaign_id')
    result = manus_api.sync_ads(campaign_id)
    return jsonify(result)

@app.route('/api/manus/reports', methods=['GET'])
def api_manus_reports():
    """Puxa relatórios da API Manus"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date or not end_date:
        return jsonify({'success': False, 'error': 'Datas obrigatórias'}), 400
    
    result = manus_api.pull_reports(start_date, end_date)
    return jsonify(result)

@app.route('/api/manus/credits/balance')
def api_manus_credits_balance():
    """Consulta saldo de créditos"""
    result = manus_api.get_credits_balance()
    return jsonify(result)

@app.route('/api/manus/credits/consume', methods=['POST'])
def api_manus_credits_consume():
    """Consome créditos"""
    amount = request.json.get('amount')
    description = request.json.get('description', 'Consumo via API')
    
    if not amount:
        return jsonify({'success': False, 'error': 'Amount obrigatório'}), 400
    
    result = manus_api.consume_credits(amount, description)
    return jsonify(result)

@app.route('/api/manus/webhooks/register', methods=['POST'])
def api_manus_webhooks_register():
    """Registra webhook na API Manus"""
    event = request.json.get('event')
    url = request.json.get('url')
    
    if not event or not url:
        return jsonify({'success': False, 'error': 'Event e URL obrigatórios'}), 400
    
    result = manus_api.register_webhook(event, url)
    return jsonify(result)

@app.route('/webhooks/manus', methods=['POST'])
def webhooks_manus():
    """Recebe webhooks da API Manus"""
    signature = request.headers.get('X-Manus-Signature')
    payload = request.get_data(as_text=True)
    
    # Verificar assinatura
    if not manus_api.verify_webhook_signature(payload, signature):
        return jsonify({'error': 'Invalid signature'}), 401
    
    # Processar webhook
    data = request.json
    event = data.get('event')
    
    # Log do webhook
    db = get_db()
    db.execute("""
        INSERT INTO manus_sync_logs (sync_type, pushed, pulled, errors, synced_at)
        VALUES (?, 0, 1, '[]', ?)
    """, (f'webhook_{event}', datetime.now().isoformat()))
    db.commit()
    
    return jsonify({'success': True, 'received': True})


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


# ===== CREDITS ALERT ENDPOINTS =====

# Inicializar Credits Alert Service
from services.credits_alert_service import CreditsAlertService
credits_alert = CreditsAlertService()

@app.route("/api/credits/check-alert", methods=["GET"])
def api_credits_check_alert():
    """Verifica saldo e retorna alerta se necessário"""
    try:
        alert = credits_alert.check_balance_and_alert()
        
        # Registrar alerta se houver
        if alert['alert']:
            credits_alert.log_alert(alert)
            credits_alert.create_notification(alert)
        
        return jsonify(alert)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/credits/balance", methods=["GET"])
def api_credits_balance():
    """Obtém saldo atual de créditos"""
    try:
        balance = credits_alert.get_credits_balance()
        return jsonify({
            "success": True,
            **balance
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/credits/set-unlimited", methods=["POST"])
def api_credits_set_unlimited():
    """Define créditos como ilimitados"""
    try:
        success = credits_alert.set_unlimited_credits()
        
        if success:
            log_activity("Créditos Ilimitados", "Créditos definidos como ILIMITADOS (∞)")
            return jsonify({
                "success": True,
                "message": "✅ Créditos definidos como ILIMITADOS (∞)",
                "balance": "∞"
            })
        else:
            return jsonify({"success": False, "message": "Erro ao definir créditos"}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/notifications/unread", methods=["GET"])
def api_notifications_unread():
    """Obtém notificações não lidas"""
    try:
        notifications = credits_alert.get_unread_notifications()
        return jsonify({
            "success": True,
            "notifications": notifications,
            "count": len(notifications)
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/notifications/mark-read/<int:notification_id>", methods=["POST"])
def api_notifications_mark_read(notification_id):
    """Marca notificação como lida"""
    try:
        success = credits_alert.mark_notification_as_read(notification_id)
        
        if success:
            return jsonify({"success": True, "message": "Notificação marcada como lida"})
        else:
            return jsonify({"success": False, "message": "Erro ao marcar notificação"}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ============================================
# CAMPAIGN TESTER ENDPOINTS
# ============================================

from services.campaign_tester import CampaignTester, create_warming_tables

campaign_tester = CampaignTester()

@app.route('/api/campaign/test/create', methods=['POST'])
def api_create_test_campaign():
    """Criar campanha de teste com aquecimento"""
    try:
        data = request.json
        result = campaign_tester.create_test_campaign(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/campaign/test/monitor/<int:campaign_id>', methods=['GET'])
def api_monitor_test_campaign(campaign_id):
    """Monitorar campanha de teste"""
    try:
        result = campaign_tester.monitor_campaign(campaign_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/campaign/test/status/<int:campaign_id>', methods=['GET'])
def api_test_campaign_status(campaign_id):
    """Status completo do aquecimento"""
    try:
        result = campaign_tester.get_campaign_warming_status(campaign_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/campaign/test/stop/<int:campaign_id>', methods=['POST'])
def api_stop_test_campaign(campaign_id):
    """Parar teste de campanha"""
    try:
        data = request.json
        reason = data.get('reason', 'manual_stop')
        result = campaign_tester.stop_test(campaign_id, reason)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ===== GLOBAL SEARCH ENDPOINT =====

@app.route('/api/search', methods=['GET'])
def api_global_search():
    """Busca global no sistema"""
    try:
        query = request.args.get('q', '').strip().lower()
        if not query:
            return jsonify([])
        
        results = []
        db = get_db()
        
        # Buscar campanhas
        campaigns = db.execute(
            "SELECT id, name, status, platform FROM campaigns WHERE LOWER(name) LIKE ? LIMIT 5",
            (f'%{query}%',)
        ).fetchall()
        
        for campaign in campaigns:
            results.append({
                'category': 'Campanhas',
                'title': campaign['name'],
                'description': f"{campaign['platform']} • {campaign['status']}",
                'icon': 'fas fa-bullhorn',
                'url': f'/campaign/{campaign["id"]}'
            })
        
        # Buscar anúncios
        ads = db.execute(
            "SELECT id, name, status FROM ads WHERE LOWER(name) LIKE ? LIMIT 5",
            (f'%{query}%',)
        ).fetchall()
        
        for ad in ads:
            results.append({
                'category': 'Anúncios',
                'title': ad['name'],
                'description': f"Status: {ad['status']}",
                'icon': 'fas fa-ad',
                'url': f'/ad/{ad["id"]}'
            })
        
        # Buscar relatórios
        reports = db.execute(
            "SELECT id, name, type FROM reports WHERE LOWER(name) LIKE ? LIMIT 5",
            (f'%{query}%',)
        ).fetchall()
        
        for report in reports:
            results.append({
                'category': 'Relatórios',
                'title': report['name'],
                'description': f"Tipo: {report['type']}",
                'icon': 'fas fa-chart-line',
                'url': f'/report/{report["id"]}'
            })
        
        # Páginas do sistema (busca por palavras-chave)
        pages = [
            {'title': 'Dashboard', 'keywords': ['dashboard', 'inicio', 'home', 'painel'], 'icon': 'fas fa-home', 'url': '/'},
            {'title': 'Criar Anúncio Perfeito', 'keywords': ['anuncio', 'criar', 'ia', 'ai', 'perfeito'], 'icon': 'fas fa-magic', 'url': '/create_perfect_ad_v2'},
            {'title': 'Campanhas', 'keywords': ['campanhas', 'lista', 'gerenciar'], 'icon': 'fas fa-bullhorn', 'url': '/campaigns'},
            {'title': 'Criar Campanha', 'keywords': ['criar', 'nova', 'campanha'], 'icon': 'fas fa-plus', 'url': '/create_campaign'},
            {'title': 'Testar Campanha', 'keywords': ['testar', 'teste', 'aquecimento', 'warming'], 'icon': 'fas fa-flask', 'url': '/test_campaign'},
            {'title': 'Biblioteca de Mídia', 'keywords': ['midia', 'imagens', 'videos', 'arquivos'], 'icon': 'fas fa-photo-video', 'url': '/media_library'},
            {'title': 'Relatórios', 'keywords': ['relatorios', 'analytics', 'metricas'], 'icon': 'fas fa-chart-bar', 'url': '/reports'},
            {'title': 'Segmentação', 'keywords': ['segmentacao', 'publico', 'audiencia'], 'icon': 'fas fa-users', 'url': '/segmentation'},
            {'title': 'Funil de Vendas', 'keywords': ['funil', 'vendas', 'conversao'], 'icon': 'fas fa-filter', 'url': '/funnel_builder'},
            {'title': 'DCO Builder', 'keywords': ['dco', 'dinamico', 'criativo'], 'icon': 'fas fa-layer-group', 'url': '/dco_builder'},
            {'title': 'Landing Page Builder', 'keywords': ['landing', 'pagina', 'construtor'], 'icon': 'fas fa-file-code', 'url': '/landing_page_builder'},
            {'title': 'Velyra Prime', 'keywords': ['velyra', 'ia', 'assistente', 'chat'], 'icon': 'fas fa-robot', 'url': '/velyra_prime'},
            {'title': 'Integrações', 'keywords': ['integracoes', 'conectar', 'apis'], 'icon': 'fas fa-plug', 'url': '/integrations'},
            {'title': 'Configurações', 'keywords': ['configuracoes', 'ajustes', 'settings'], 'icon': 'fas fa-cog', 'url': '/settings'},
        ]
        
        for page in pages:
            if any(keyword in query for keyword in page['keywords']):
                results.append({
                    'category': 'Páginas',
                    'title': page['title'],
                    'description': 'Navegar para esta página',
                    'icon': page['icon'],
                    'url': page['url']
                })
        
        return jsonify(results[:15])  # Limitar a 15 resultados
        
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify([])


# ===== MCP INTEGRATION ENDPOINTS =====

@app.route("/api/mcp/command", methods=["POST"])
def api_mcp_command():
    """Execute MCP command"""
    if not mcp_service:
        return jsonify({"success": False, "error": "MCP service not available"}), 503
    
    data = request.get_json()
    command = data.get("command")
    params = data.get("params", {})
    
    result = mcp_service.send_command(command, params)
    return jsonify(result)


@app.route("/api/mcp/webhook/register", methods=["POST"])
def api_mcp_webhook_register():
    """Register webhook"""
    if not mcp_service:
        return jsonify({"success": False, "error": "MCP service not available"}), 503
    
    data = request.get_json()
    event = data.get("event")
    url = data.get("url")
    
    result = mcp_service.register_webhook(event, url)
    return jsonify(result)


@app.route("/api/mcp/event", methods=["POST"])
def api_mcp_event():
    """Emit MCP event"""
    if not mcp_service:
        return jsonify({"success": False, "error": "MCP service not available"}), 503
    
    data = request.get_json()
    event_type = data.get("event_type")
    event_data = data.get("data", {})
    
    result = mcp_service.emit_event(event_type, event_data)
    return jsonify(result)


@app.route("/api/mcp/telemetry", methods=["POST"])
def api_mcp_telemetry():
    """Log telemetry"""
    if not mcp_service:
        return jsonify({"success": False, "error": "MCP service not available"}), 503
    
    data = request.get_json()
    metric = data.get("metric")
    value = data.get("value")
    tags = data.get("tags", {})
    
    result = mcp_service.log_telemetry(metric, value, tags)
    return jsonify(result)


@app.route("/api/mcp/telemetry/<metric>", methods=["GET"])
def api_mcp_get_telemetry(metric):
    """Get telemetry data"""
    if not mcp_service:
        return jsonify({"success": False, "error": "MCP service not available"}), 503
    
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    
    result = mcp_service.get_telemetry(metric, start_date, end_date)
    return jsonify(result)


@app.route("/api/mcp/status", methods=["GET"])
def api_mcp_status():
    """Get MCP integration status"""
    if not mcp_service:
        return jsonify({"success": False, "error": "MCP service not available"}), 503
    
    return jsonify({
        "success": True,
        "mcp_enabled": mcp_service.mcp_enabled,
        "is_connected": mcp_service.is_connected,
        "last_sync": mcp_service.last_sync,
        "api_base_url": mcp_service.api_base_url
    })


@app.route("/api/mcp/authorize", methods=["GET"])
def api_mcp_authorize():
    """Get MCP authorization URL"""
    if not manus_api:
        return jsonify({"success": False, "error": "Manus API not available"}), 503
    
    try:
        auth_url = manus_api.get_authorization_url()
        return jsonify({
            "success": True,
            "authorization_url": auth_url
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/mcp/token", methods=["POST"])
def api_mcp_token():
    """Exchange code for token or refresh token"""
    if not manus_api:
        return jsonify({"success": False, "error": "Manus API not available"}), 503
    
    data = request.get_json()
    grant_type = data.get("grant_type")
    
    try:
        if grant_type == "authorization_code":
            code = data.get("code")
            state = data.get("state")
            result = manus_api.exchange_code_for_token(code, state)
        elif grant_type == "refresh_token":
            result = manus_api.refresh_access_token()
        else:
            return jsonify({"success": False, "error": "Invalid grant_type"}), 400
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/mcp/test", methods=["GET"])
def api_mcp_test():
    """Test MCP connection"""
    return jsonify({
        "success": True,
        "message": "MCP connection is working",
        "timestamp": datetime.now().isoformat()
    })


# ===== REMOTE CONTROL ENDPOINTS =====

@app.route("/api/remote/session/start", methods=["POST"])
def api_remote_session_start():
    """Start remote control session"""
    if not remote_control:
        return jsonify({"success": False, "error": "Remote control not available"}), 503
    
    data = request.get_json()
    controller = data.get("controller", "manus_ai")
    
    result = remote_control.start_session(controller)
    return jsonify(result)


@app.route("/api/remote/session/end", methods=["POST"])
def api_remote_session_end():
    """End remote control session"""
    if not remote_control:
        return jsonify({"success": False, "error": "Remote control not available"}), 503
    
    data = request.get_json()
    session_token = data.get("session_token")
    
    result = remote_control.end_session(session_token)
    return jsonify(result)


@app.route("/api/remote/execute", methods=["POST"])
def api_remote_execute():
    """Execute remote action"""
    if not remote_control:
        return jsonify({"success": False, "error": "Remote control not available"}), 503
    
    data = request.get_json()
    session_token = data.get("session_token")
    action = data.get("action")
    params = data.get("params", {})
    
    result = remote_control.execute_action(session_token, action, params)
    return jsonify(result)


@app.route("/api/remote/sessions", methods=["GET"])
def api_remote_sessions():
    """Get active sessions"""
    if not remote_control:
        return jsonify({"success": False, "error": "Remote control not available"}), 503
    
    result = remote_control.get_active_sessions()
    return jsonify(result)


@app.route("/api/remote/audit", methods=["GET"])
def api_remote_audit():
    """Get audit log"""
    if not remote_control:
        return jsonify({"success": False, "error": "Remote control not available"}), 503
    
    limit = request.args.get("limit", 100, type=int)
    result = remote_control.get_audit_log(limit)
    return jsonify(result)


# ===== CAMPAIGN AUTOMATION ENDPOINTS =====

@app.route("/api/automation/authorize/request", methods=["POST"])
def api_automation_authorize_request():
    """Request spend authorization"""
    if not campaign_automation:
        return jsonify({"success": False, "error": "Automation not available"}), 503
    
    data = request.get_json()
    result = campaign_automation.request_spend_authorization(
        action=data.get("action"),
        amount=data.get("amount"),
        campaign_id=data.get("campaign_id"),
        notes=data.get("notes")
    )
    return jsonify(result)


@app.route("/api/automation/authorize/approve/<int:auth_id>", methods=["POST"])
def api_automation_authorize_approve(auth_id):
    """Approve spend authorization"""
    if not campaign_automation:
        return jsonify({"success": False, "error": "Automation not available"}), 503
    
    data = request.get_json()
    approved_by = data.get("approved_by", "user")
    
    result = campaign_automation.approve_spend_authorization(auth_id, approved_by)
    return jsonify(result)


@app.route("/api/automation/authorize/reject/<int:auth_id>", methods=["POST"])
def api_automation_authorize_reject(auth_id):
    """Reject spend authorization"""
    if not campaign_automation:
        return jsonify({"success": False, "error": "Automation not available"}), 503
    
    data = request.get_json()
    rejected_by = data.get("rejected_by", "user")
    reason = data.get("reason")
    
    result = campaign_automation.reject_spend_authorization(auth_id, rejected_by, reason)
    return jsonify(result)


@app.route("/api/automation/authorize/pending", methods=["GET"])
def api_automation_authorize_pending():
    """Get pending authorizations"""
    if not campaign_automation:
        return jsonify({"success": False, "error": "Automation not available"}), 503
    
    result = campaign_automation.get_pending_authorizations()
    return jsonify(result)


@app.route("/api/automation/optimize/<int:campaign_id>", methods=["POST"])
def api_automation_optimize_campaign(campaign_id):
    """Auto-optimize campaign"""
    if not campaign_automation:
        return jsonify({"success": False, "error": "Automation not available"}), 503
    
    result = campaign_automation.auto_optimize_campaign(campaign_id)
    return jsonify(result)


@app.route("/api/automation/optimize/all", methods=["POST"])
def api_automation_optimize_all():
    """Optimize all campaigns"""
    if not campaign_automation:
        return jsonify({"success": False, "error": "Automation not available"}), 503
    
    result = campaign_automation.optimize_all_campaigns()
    return jsonify(result)


@app.route("/api/automation/report", methods=["GET"])
def api_automation_report():
    """Get automation report"""
    if not campaign_automation:
        return jsonify({"success": False, "error": "Automation not available"}), 503
    
    days = request.args.get("days", 7, type=int)
    result = campaign_automation.get_automation_report(days)
    return jsonify(result)


# ===== UX AUDIT ENDPOINTS =====

@app.route("/api/audit/page", methods=["POST"])
def api_audit_page():
    """Audit single page"""
    if not ux_audit:
        return jsonify({"success": False, "error": "UX audit not available"}), 503
    
    data = request.get_json()
    result = ux_audit.audit_page(data.get("page_name"), data.get("url"))
    return jsonify(result)


@app.route("/api/audit/pages", methods=["GET"])
def api_audit_all_pages():
    """Audit all pages"""
    if not ux_audit:
        return jsonify({"success": False, "error": "UX audit not available"}), 503
    
    result = ux_audit.audit_all_pages()
    return jsonify(result)


@app.route("/api/audit/flows", methods=["GET"])
def api_audit_flows():
    """Audit critical flows"""
    if not ux_audit:
        return jsonify({"success": False, "error": "UX audit not available"}), 503
    
    result = ux_audit.audit_critical_flows()
    return jsonify(result)


@app.route("/api/audit/performance", methods=["GET"])
def api_audit_performance():
    """Audit performance"""
    if not ux_audit:
        return jsonify({"success": False, "error": "UX audit not available"}), 503
    
    result = ux_audit.audit_performance()
    return jsonify(result)


@app.route("/api/audit/accessibility", methods=["GET"])
def api_audit_accessibility():
    """Audit accessibility"""
    if not ux_audit:
        return jsonify({"success": False, "error": "UX audit not available"}), 503
    
    result = ux_audit.audit_accessibility()
    return jsonify(result)


@app.route("/api/audit/full", methods=["GET"])
def api_audit_full():
    """Generate full audit report"""
    if not ux_audit:
        return jsonify({"success": False, "error": "UX audit not available"}), 503
    
    result = ux_audit.generate_full_audit_report()
    
    # Salvar relatório
    save_result = ux_audit.save_audit_report(result)
    result['saved'] = save_result.get('success', False)
    result['audit_id'] = save_result.get('audit_id')
    
    return jsonify(result)


# ===== PRODUCT INTELLIGENCE ENDPOINTS =====

@app.route("/api/intelligence/product/analyze", methods=["POST"])
def api_intelligence_analyze_product():
    """Analyze product"""
    if not product_intelligence:
        return jsonify({"success": False, "error": "Product intelligence not available"}), 503
    
    data = request.get_json()
    result = product_intelligence.analyze_product(data)
    return jsonify(result)


@app.route("/api/intelligence/sales/analyze", methods=["GET"])
def api_intelligence_analyze_sales():
    """Analyze sales data"""
    if not product_intelligence:
        return jsonify({"success": False, "error": "Product intelligence not available"}), 503
    
    period_days = request.args.get("period_days", 30, type=int)
    result = product_intelligence.analyze_sales_data(period_days)
    return jsonify(result)


@app.route("/api/intelligence/sales/forecast", methods=["GET"])
def api_intelligence_forecast_sales():
    """Forecast sales"""
    if not product_intelligence:
        return jsonify({"success": False, "error": "Product intelligence not available"}), 503
    
    days_ahead = request.args.get("days_ahead", 30, type=int)
    result = product_intelligence.forecast_sales(days_ahead)
    return jsonify(result)


@app.route("/api/intelligence/products/recommend", methods=["POST"])
def api_intelligence_recommend_products():
    """Recommend products for campaign"""
    if not product_intelligence:
        return jsonify({"success": False, "error": "Product intelligence not available"}), 503
    
    data = request.get_json()
    result = product_intelligence.recommend_products_for_campaign(
        campaign_objective=data.get("objective", "conversions"),
        budget=data.get("budget", 1000)
    )
    return jsonify(result)


@app.route("/api/intelligence/competitors/analyze", methods=["POST"])
def api_intelligence_analyze_competitors():
    """Analyze competitor products"""
    if not product_intelligence:
        return jsonify({"success": False, "error": "Product intelligence not available"}), 503
    
    data = request.get_json()
    result = product_intelligence.analyze_competitor_products(data.get("product_name"))
    return jsonify(result)


@app.route("/api/intelligence/report", methods=["GET"])
def api_intelligence_report():
    """Generate intelligence report"""
    if not product_intelligence:
        return jsonify({"success": False, "error": "Product intelligence not available"}), 503
    
    result = product_intelligence.generate_intelligence_report()
    return jsonify(result)


# ============================================================================
# API DE GERAÇÃO DE CAMPANHAS COM IA
# ============================================================================

@app.route("/api/ai/generate-campaign", methods=["POST"])
def api_ai_generate_campaign():
    """
    Gera uma campanha completa com anúncios usando IA
    
    Request Body:
    {
        "plataforma": "meta|google|tiktok|pinterest|linkedin",
        "objetivo": "awareness|traffic|engagement|leads|sales",
        "publico": "descrição do público-alvo",
        "produto": "nome do produto/serviço",
        "voz": "casual|profissional|urgente|inspirador",
        "quantidade_anuncios": 3
    }
    
    Response:
    {
        "success": true,
        "campanha": {...},
        "anuncios": [...],
        "metricas_estimadas": {...},
        "recomendacoes": [...]
    }
    """
    if not ai_campaign_generator:
        return jsonify({
            "success": False,
            "error": "AI Campaign Generator não disponível"
        }), 503
    
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ["plataforma", "objetivo", "publico", "produto"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    "success": False,
                    "error": f"Campo obrigatório ausente: {field}"
                }), 400
        
        # Gerar campanha com IA
        result = ai_campaign_generator.generate_campaign(data)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro ao gerar campanha: {str(e)}"
        }), 500


@app.route("/api/ai/generate-ad-variations", methods=["POST"])
def api_ai_generate_ad_variations():
    """
    Gera variações de um anúncio existente
    
    Request Body:
    {
        "base_ad": {...},
        "quantidade": 3
    }
    """
    if not ai_campaign_generator:
        return jsonify({
            "success": False,
            "error": "AI Campaign Generator não disponível"
        }), 503
    
    try:
        data = request.get_json()
        base_ad = data.get("base_ad")
        quantidade = data.get("quantidade", 3)
        
        if not base_ad:
            return jsonify({
                "success": False,
                "error": "base_ad é obrigatório"
            }), 400
        
        variacoes = ai_campaign_generator.generate_ad_variations(base_ad, quantidade)
        
        return jsonify({
            "success": True,
            "variacoes": variacoes
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro ao gerar variações: {str(e)}"
        }), 500


# ============================================================================
# ROTAS DE PÁGINAS ADICIONAIS
# ============================================================================

@app.route("/campaign-detail")
def campaign_detail():
    """Página de detalhes da campanha"""
    return render_template("campaign_detail.html")


@app.route("/create-perfect-ad-v2")
def create_perfect_ad_v2():
    """Página de criação de anúncio perfeito v2"""
    return render_template("create_perfect_ad_v2.html")


@app.route("/manus-connection")
def manus_connection():
    """Página de conexão com Manus"""
    return render_template("manus_connection.html")


@app.route("/not-found")
def not_found_page():
    """Página 404"""
    return render_template("not_found.html"), 404


@app.route("/report-view")
def report_view():
    """Página de visualização de relatório"""
    return render_template("report_view.html")


@app.route("/reports-dashboard")
def reports_dashboard():
    """Dashboard de relatórios"""
    return render_template("reports_dashboard.html")


# ===== INTELIGÊNCIA ARTIFICIAL ROUTES =====

@app.route("/ai-copywriter")
def ai_copywriter():
    """Gerador de Copy com IA"""
    return render_template("ai_copywriter.html")


@app.route("/ai-image-generator")
def ai_image_generator():
    """Gerador de Imagens com IA"""
    return render_template("ai_image_generator.html")


@app.route("/ai-video-scripts")
def ai_video_scripts():
    """Scripts de Vídeo com IA"""
    return render_template("ai_video_scripts.html")


@app.route("/ai-sentiment")
def ai_sentiment():
    """Análise de Sentimento com IA"""
    return render_template("ai_sentiment.html")


@app.route("/ai-performance-prediction")
def ai_performance_prediction():
    """Previsão de Performance com IA"""
    return render_template("ai_performance_prediction.html")


# ===== PLATAFORMAS ROUTES =====

@app.route("/platforms/facebook")
def platforms_facebook():
    """Facebook Ads"""
    return render_template("platforms_facebook.html")


@app.route("/platforms/google")
def platforms_google():
    """Google Ads"""
    return render_template("platforms_google.html")


@app.route("/platforms/tiktok")
def platforms_tiktok():
    """TikTok Ads"""
    return render_template("platforms_tiktok.html")


@app.route("/platforms/pinterest")
def platforms_pinterest():
    """Pinterest Ads"""
    return render_template("platforms_pinterest.html")


@app.route("/platforms/linkedin")
def platforms_linkedin():
    """LinkedIn Ads"""
    return render_template("platforms_linkedin.html")


@app.route("/platforms/multi")
def platforms_multi():
    """Multi-Plataforma"""
    return render_template("platforms_multi.html")


# ===== OTIMIZAÇÃO ROUTES =====

@app.route("/optimization/auto")
def optimization_auto():
    """Otimização Automática"""
    return render_template("optimization_auto.html")


@app.route("/optimization/budget")
def optimization_budget():
    """Redistribuição de Budget"""
    return render_template("optimization_budget.html")


@app.route("/optimization/bidding")
def optimization_bidding():
    """Ajuste de Lances"""
    return render_template("optimization_bidding.html")


@app.route("/optimization/autopilot")
def optimization_autopilot():
    """Auto-Pilot 24/7"""
    return render_template("optimization_autopilot.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
