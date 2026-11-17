from flask import Flask, jsonify
from health_stats_func import (
    create_daily_health_stats,
    calculate_bmi,
    calculate_km_walked,
    calculate_goal_progress_percent,
    is_goal_achieved
)

app = Flask(__name__)

@app.route("/health")
def health():

    stats = create_daily_health_stats(
        height_m=1.80,
        weight_kg=82.5,
        steps=5000,
        calories_burned=1500,
        avg_heart_rate=72
    )

    return jsonify({
        "BMI": calculate_bmi(stats),
        "Distance": calculate_km_walked(stats),
        "Goal Progress": calculate_goal_progress_percent(stats),
        "Goal Achieved": is_goal_achieved(stats)
    })
@app.route("/")
def home():
    return "Health Stats API"

if __name__ == "__main__":
    app.run(debug=True)