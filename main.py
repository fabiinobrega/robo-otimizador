import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, jsonify, g
from werkzeug.utils import secure_filename
import json
import random

# Importação dos módulos de serviços
try:
    from services import meta_ads_publisher
    from services import google_ads_publisher
    from services import competitor_spy_service
    from services import dco_service
    from services import landing_page_builder_service
    from services import segmentation_service
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


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

