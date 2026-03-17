from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from ai_service import generate_why_explanation
import os
from pydantic import BaseModel
from typing import List

from graph_engine import build_skill_graph, get_learning_path, describe_skill

load_dotenv()

app = FastAPI(
    title="SkillScout API",
    description="AI-powered learning path generator with prerequisite gap detection",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: ["https://skillscout.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Build graph once at startup
skill_graph = build_skill_graph()

# Pydantic Models
class PathRequest(BaseModel):
    target_skill_id: str
    current_skills: List[str] = []

class TimelineRequest(BaseModel):
    target_skill_id: str
    proposed_weeks: int

# Hardcoded community data (for demo)
COMMUNITY_INSIGHTS = {
    "closures": {
        "struggle_percentage": 87,
        "average_days_to_master": 3.2,
        "common_confusion": "Understanding scope and variable access in nested functions",
        "tip": "Practice writing custom React hooks - they force you to understand closures deeply",
        "testimonial": "मैंने बिना closures समझे React सीखा था। 2 महीने struggle किया। - Rahul, Mumbai"
    },
    "react": {
        "struggle_percentage": 73,
        "average_days_to_master": 8.5,
        "common_confusion": "When to use state vs props, component lifecycle",
        "tip": "Build 3 small projects before one big one - muscle memory matters",
        "testimonial": "State management confusion गया after I built a todo app. - Priya, Bangalore"
    },
    "hooks": {
        "struggle_percentage": 82,
        "average_days_to_master": 4.8,
        "common_confusion": "useEffect dependency arrays, stale closures",
        "tip": "Read React docs on hooks 3 times. It clicks on third read.",
        "testimonial": "useEffect dependencies समझने में 1 week लगा। Worth it. - Anjali, Pune"
    },
    "javascript": {
        "struggle_percentage": 65,
        "average_days_to_master": 5.0,
        "common_confusion": "this keyword, prototype inheritance, type coercion",
        "tip": "Master fundamentals before frameworks. Future you will thank present you.",
        "testimonial": "Fundamentals strong होना चाहिए। Shortcuts don't work. - Rohan, Delhi"
    },
    "async_await": {
        "struggle_percentage": 75,
        "average_days_to_master": 2.5,
        "common_confusion": "Error handling with try/catch, promise chaining",
        "tip": "Practice with fetch API - seeing real async helps",
        "testimonial": "API calls के साथ practice करने से समझ आया। - Karthik, Chennai"
    },
    "jsx": {
        "struggle_percentage": 58,
        "average_days_to_master": 3.0,
        "common_confusion": "JavaScript expressions vs statements in JSX",
        "tip": "Remember: JSX compiles to React.createElement() calls",
        "testimonial": "JSX is just JavaScript. Ek baar समझ गया तो easy. - Neha, Hyderabad"
    },
    "dom": {
        "struggle_percentage": 62,
        "average_days_to_master": 3.0,
        "common_confusion": "Event delegation, DOM traversal methods",
        "tip": "Learn vanilla JS DOM before jQuery or frameworks",
        "testimonial": "Manual DOM manipulation सीखने से React appreciate करने लगा। - Amit, Kolkata"
    },
    "state": {
        "struggle_percentage": 78,
        "average_days_to_master": 4.0,
        "common_confusion": "When to lift state up, immutable updates",
        "tip": "Start with local state, lift only when needed",
        "testimonial": "State management pattern समझने में time लगा but worth it. - Divya, Jaipur"
    }
}

# Root & Health Endpoints
@app.get("/")
def root():
    return {
        "service": "SkillScout API",
        "version": "1.0.0",
        "status": "healthy",
        "skills_loaded": len(skill_graph.nodes),
        "endpoints": [
            "GET /health",
            "GET /skills",
            "GET /skill/{id}",
            "POST /generate-path",
            "POST /validate-timeline",
            "GET /community-insights/{id}"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "ok", "skills": len(skill_graph.nodes)}

# Main Feature Endpoints
@app.post("/generate-path")
def generate_path(request: PathRequest):
    """
    Generate personalized learning path with AI gap detection.
    
    This is the CORE feature - detects prerequisite gaps and explains why they matter.
    """
    try:
        full_path = get_learning_path(skill_graph, request.target_skill_id)

        filtered_path = [
            skill for skill in full_path
            if skill not in request.current_skills
        ]
        next_gap = filtered_path[0] if filtered_path else None

        detailed_path = []
        for idx, skill_id in enumerate(filtered_path):
            skill_data = describe_skill(skill_graph, skill_id)
            
            # Generate AI explanation
            explanation = generate_why_explanation(
                skill_data["name"],
                request.current_skills
            )
            skill_data["why_now"] = explanation
            skill_data["is_critical_gap"] = (skill_id == next_gap)
            skill_data["order"] = idx + 1
            
            # Add community insights if available
            if skill_id in COMMUNITY_INSIGHTS:
                skill_data["community"] = {
                    "struggle_rate": COMMUNITY_INSIGHTS[skill_id]["struggle_percentage"],
                    "helpful_tip": COMMUNITY_INSIGHTS[skill_id]["tip"]
                }
            
            detailed_path.append(skill_data)
        
        total_days = sum(s["estimated_days"] for s in detailed_path)
        total_weeks = round(total_days / 7, 1)

        return {
            "success": True,
            "target_skill": request.target_skill_id,
            "target_skill_name": skill_graph.nodes[request.target_skill_id]["name"],
            "current_skills": request.current_skills,
            "has_gap": len(filtered_path) > 0,
            "next_critical_gap": next_gap,
            "learning_path": detailed_path,
            "total_days": total_days,
            "total_weeks": total_weeks,
            "timeline_message": f"Realistic timeline: {total_weeks} weeks with focused study"
        }

    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Skill not found: {str(e)}")

@app.post("/validate-timeline")
def validate_timeline(request: TimelineRequest):
    """
    Check if user's proposed timeline is realistic.
    
    KEY DIFFERENTIATOR - prevents unrealistic goals like "ML engineer in 1 week"
    """
    try:
        path = get_learning_path(skill_graph, request.target_skill_id)
        
        total_days = sum(
            skill_graph.nodes[skill]["estimated_days"] 
            for skill in path
        )
        realistic_weeks = round(total_days / 7, 1)
        
        is_realistic = request.proposed_weeks >= realistic_weeks * 0.8
        
        return {
            "success": True,
            "is_realistic": is_realistic,
            "proposed_weeks": request.proposed_weeks,
            "realistic_weeks": realistic_weeks,
            "total_days": total_days,
            "message": (
                f"✅ {request.proposed_weeks} weeks is achievable with focused study!" 
                if is_realistic 
                else f"⚠️ This typically takes {realistic_weeks} weeks. Consider adjusting your timeline for sustainable learning."
            ),
            "adjustment_factor": round(realistic_weeks / request.proposed_weeks, 1) if request.proposed_weeks > 0 else 0
        }
    
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Skill not found: {str(e)}")

@app.get("/community-insights/{skill_id}")
def get_community_insights(skill_id: str):
    """
    Get community learning patterns for a skill.
    
    Shows struggle rates, helpful tips, and Hinglish testimonials.
    """
    if skill_id not in skill_graph:
        raise HTTPException(status_code=404, detail="Skill not found")

    insights = COMMUNITY_INSIGHTS.get(
        skill_id,
        {
            "struggle_percentage": 65,
            "average_days_to_master": skill_graph.nodes[skill_id]["estimated_days"],
            "common_confusion": "Various conceptual challenges",
            "tip": "Practice with real projects",
            "testimonial": None
        }
    )

    return {
        "success": True,
        "skill_id": skill_id,
        "skill_name": skill_graph.nodes[skill_id]["name"],
        **insights
    }

@app.get("/skills")
def list_skills():
    """List all available skills for dropdowns/autocomplete"""
    skills = []
    for node_id in skill_graph.nodes:
        node_data = skill_graph.nodes[node_id]
        skills.append({
            "id": node_id,
            "name": node_data["name"],
            "difficulty": node_data["difficulty"],
            "estimated_days": node_data["estimated_days"],
            "prerequisites_count": len(node_data["prerequisites"])
        })
    
    # Sort by difficulty then name
    difficulty_order = {"beginner": 0, "intermediate": 1, "advanced": 2}
    skills.sort(key=lambda x: (difficulty_order[x["difficulty"]], x["name"]))
    
    return {"success": True, "skills": skills, "total": len(skills)}

@app.get("/skill/{skill_id}")
def skill_details(skill_id: str):
    """Get detailed information about a specific skill"""
    try:
        details = describe_skill(skill_graph, skill_id)
        return {"success": True, **details}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Skill not found: {str(e)}")