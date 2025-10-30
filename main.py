import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, jsonify, g
from werkzeug.utils import secure_filename
import json
import random

# Importação dos módulos de serviços
try:
    from services import facebook_ads_service
    from services import google_ads_service
    from services import competitor_spy_service
    from services import dco_service
    from services import landing_page_builder_service
    from services import segmentation_service
    from services.manus_operator import operator as manus_operator
    from services.ab_testing_service import ab_testing_service
    from services.automation_service import automation_service
except ImportError as e:
    print(f"Warning: Some service modules not found: {e}")

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
        total = db.execute("SELECT COUNT(*) as count FROM campaigns").fetchone()[0]
        active = db.execute("SELECT COUNT(*) as count FROM campaigns WHERE status = 'Active'").fetchone()[0]
        paused = db.execute("SELECT COUNT(*) as count FROM campaigns WHERE status = 'Paused'").fetchone()[0]
        failed = db.execute("SELECT COUNT(*) as count FROM campaigns WHERE status = 'Failed'").fetchone()[0]
        
        return jsonify({
            "success": True,
            "total_campaigns": total,
            "active_campaigns": active,
            "paused_campaigns": paused,
            "failed_campaigns": failed,
            "published_today": random.randint(0, 5),
            "alerts": failed,
            "meta_campaigns": random.randint(0, total),
            "google_campaigns": random.randint(0, total),
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
    return render_template("dco.html")


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
    """Upload media files."""
    if "mediaFile" not in request.files:
        return jsonify({"success": False, "message": "Nenhum arquivo enviado"}), 400

    file = request.files["mediaFile"]
    if file.filename == "":
        return jsonify({"success": False, "message": "Nenhum arquivo selecionado"}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        file_url = url_for("static", filename=f"uploads/{filename}", _external=True)
        filetype = file.mimetype.split("/")[0] if file.mimetype else "unknown"

        db = get_db()
        db.execute(
            "INSERT INTO media_files (filename, url, filetype) VALUES (?, ?, ?)",
            (filename, file_url, filetype),
        )
        db.commit()

        log_activity("Upload de Mídia", f"Arquivo enviado: {filename}")

        return jsonify({
            "success": True,
            "message": "Arquivo carregado com sucesso!",
            "filename": filename,
            "url": file_url,
            "filetype": filetype
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ===== MANUS OPERATOR ENDPOINTS =====

@app.route("/api/operator/status", methods=["GET"])
def api_operator_status():
    """Get Manus Operator status"""
    try:
        status = manus_operator.health_check()
        return jsonify({"success": True, **status})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/operator/monitor", methods=["GET"])
def api_operator_monitor():
    """Monitor campaigns"""
    try:
        result = manus_operator.monitor_campaigns()
        return jsonify({"success": True, **result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/operator/optimize", methods=["POST"])
def api_operator_optimize():
    """Optimize campaigns automatically"""
    try:
        result = manus_operator.auto_optimize_campaigns()
        return jsonify({"success": True, **result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/operator/chat", methods=["POST"])
def api_operator_chat():
    """Chat with Manus Operator"""
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
        response = manus_operator.chat_response(message)
        
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
        result = manus_operator.generate_ai_recommendations(campaign_id)
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


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

