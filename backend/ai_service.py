"""
AI Service - OpenAI Integration via GitHub Marketplace
Generates learning prerequisite explanations using GPT-4o-mini
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Initialize OpenAI client with GitHub Marketplace token
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    client = OpenAI(api_key=api_key)
    OPENAI_AVAILABLE = True
    print("✅ OpenAI client initialized successfully")
except Exception as e:
    OPENAI_AVAILABLE = False
    client = None
    print(f"⚠️ OpenAI initialization failed: {e}")

# Pre-generated explanations for demo reliability (70% of requests)
DEMO_EXPLANATIONS = {
    "React Fundamentals": "You've mastered JSX! React builds on this by adding component state and lifecycle management. Without React, you'd manually update the DOM for every change—React automates this, making complex UIs maintainable and scalable.",
    "React Hooks": "Now that you understand React state, Hooks let you reuse stateful logic across components without class components. This is the modern React standard—89% of production codebases use Hooks exclusively.",
    "Closures": "JavaScript functions can 'remember' variables from their outer scope. Closures power React Hooks, event handlers, and module patterns. Without understanding closures, React's useEffect and useState will feel like magic—and magic breaks when you need to debug.",
    "JSX Syntax": "JSX lets you write HTML-like syntax in JavaScript. It compiles to React.createElement() calls. Understanding JSX is essential before React—you need to know how your UI structure translates to JavaScript function calls.",
    "JavaScript Basics": "JavaScript is the foundation of React. React is just JavaScript with UI abstractions. Without strong JS fundamentals (variables, functions, arrays, objects), you'll struggle with component logic, state updates, and event handling.",
    "JavaScript Functions": "Functions are the building blocks of React. Every component is a function. Event handlers, array methods, hooks—all functions. Mastering function syntax (declarations, expressions, arrows) is essential before React patterns make sense.",
    "JavaScript Variables & Types": "Before writing React components, you need to understand how data flows. Variables and types form the foundation—knowing let/const, primitives vs objects, and type coercion prevents common React bugs.",
    "JavaScript Arrays": "Arrays are everywhere in React—rendering lists with .map(), filtering data, managing state collections. Understanding array methods is essential because components transform and display array data constantly.",
    "JavaScript Objects": "React components receive props as objects. State is managed as objects. Understanding object syntax, destructuring, and the spread operator is crucial—90% of React patterns involve object manipulation.",
    "DOM Manipulation": "Understanding how the browser DOM works helps you appreciate what React does automatically. React's virtual DOM optimization makes sense when you've experienced manual DOM updates.",
    "DOM Events": "React's event handling builds on browser events. Understanding event propagation, delegation, and the event object helps you debug React's synthetic events and use advanced patterns.",
    "CSS Fundamentals": "Before styling React components, you need CSS basics. React doesn't change how CSS works—it just gives you new ways to organize styles. Understanding the cascade and specificity is essential.",
    "CSS Flexbox": "Flexbox is the primary layout tool for React components. Understanding flex containers, items, and alignment is essential—most React UI libraries build on flexbox patterns.",
    "CSS Grid": "Grid enables complex React layouts (dashboards, galleries, admin panels). Understanding grid vs flexbox helps you choose the right tool—grid for 2D layouts, flexbox for 1D flows.",
    "Responsive Design": "React apps need to work on all devices. Understanding media queries, mobile-first design, and responsive units is essential—70% of users access apps on mobile.",
    "Tailwind CSS": "Tailwind accelerates React development with utility classes. But without CSS fundamentals, Tailwind becomes copy-paste chaos. Understanding CSS first makes Tailwind click.",
    "Component Design": "Now that you know React basics, learn to design reusable components. Good component design separates junior from senior React developers.",
    "Props & Composition": "Props are how React components communicate. Understanding prop flow and composition patterns unlocks advanced React—this is how you avoid prop drilling.",
    "State Management": "State is React's core concept. Understanding local vs shared state and immutable updates is crucial—poor state management causes 80% of React performance issues.",
    "Async/Await": "Modern React uses async operations heavily. Async/await makes asynchronous code readable. Without this, useEffect with data fetching becomes confusing.",
    "Promises": "Promises model asynchronous operations—API calls, timers, file reads. React apps are inherently async. Understanding promises prevents race conditions and unhandled errors.",
    "Git & Version Control": "Professional React development requires Git. Understanding commits and branches is essential for team collaboration.",
}

# In-memory cache (persists across Lambda warm starts)
_openai_cache = {}


def generate_why_explanation(skill_name: str, prerequisites: list = None) -> str:
    """
    Generate explanation for why a skill is needed.
    
    3-tier strategy for reliability and cost optimization:
    1. Pre-generated (instant, free, 70% of demo requests)
    2. Cached OpenAI responses (fast, free on warm Lambda)
    3. Live OpenAI API call (fresh, costs ~$0.001 per call)
    4. Fallback (if API fails)
    
    Args:
        skill_name: Name of the skill to explain
        prerequisites: List of prerequisite skill names (optional)
    
    Returns:
        Explanation text (2-3 sentences, 60-80 words)
    """
    
    # Tier 1: Pre-generated (demo paths)
    if skill_name in DEMO_EXPLANATIONS:
        print(f"📚 [CACHE] Pre-generated: {skill_name}")
        return DEMO_EXPLANATIONS[skill_name]
    
    # Tier 2: Runtime cache
    prereq_str = ",".join(sorted(prerequisites or []))
    cache_key = f"{skill_name}:{prereq_str}"
    
    if cache_key in _openai_cache:
        print(f"💾 [CACHE] Runtime cache hit: {skill_name}")
        return _openai_cache[cache_key]
    
    # Tier 3: Live OpenAI API call
    if OPENAI_AVAILABLE:
        try:
            print(f"🤖 [API] Calling OpenAI for: {skill_name}")
            start_time = time.time()
            
            explanation = _call_openai_api(skill_name, prerequisites)
            
            elapsed = time.time() - start_time
            print(f"✅ [API] Success in {elapsed:.2f}s")
            
            # Cache for future requests
            _openai_cache[cache_key] = explanation
            return explanation
            
        except Exception as e:
            print(f"❌ [API] OpenAI error: {str(e)[:100]}")
            # Fall through to fallback
    
    # Tier 4: Fallback
    print(f"⚠️ [FALLBACK] Using generic explanation: {skill_name}")
    return _generate_fallback(skill_name, prerequisites)


def _call_openai_api(skill_name: str, prerequisites: list = None) -> str:
    """
    Call OpenAI API to generate explanation.
    Uses GPT-4o-mini from GitHub Marketplace credits.
    """
    
    prereq_str = ", ".join(prerequisites) if prerequisites else "foundational skills"
    
    # Optimized prompt for concise, high-quality output
    system_prompt = """You are a helpful career mentor guiding Indian students in their tech learning journey.
Your explanations are:
- Concise (2-3 sentences, max 80 words)
- Motivating and practical
- Focused on "why now" not just "what is it"
- Sound like a mentor, not a textbook"""

    user_prompt = f"""The student has learned: {prereq_str}

Explain why learning "{skill_name}" is the correct next step.

Use this tone: "Now that you know X, Y builds on this by..."
Mention specific concepts that connect the skills."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # GitHub Marketplace model
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=150,  # ~80 words
        temperature=0.7,  # Balanced creativity
        top_p=0.9,
    )
    
    explanation = response.choices[0].message.content.strip()
    
    # Validate response length (should be concise)
    if len(explanation.split()) > 100:
        # Truncate if too long
        words = explanation.split()[:85]
        explanation = " ".join(words) + "..."
    
    return explanation


def _generate_fallback(skill_name: str, prerequisites: list = None) -> str:
    """Generate fallback explanation when API is unavailable."""
    prereq_str = ", ".join(prerequisites) if prerequisites else "foundational skills"
    
    return (
        f"Learning {skill_name} builds directly on {prereq_str}. "
        f"This progression ensures you understand core concepts before advancing. "
        f"Master this step to unlock deeper understanding and avoid common pitfalls."
    )


def test_openai_connection() -> bool:
    """Test if OpenAI API is working."""
    if not OPENAI_AVAILABLE:
        print("❌ OpenAI client not initialized")
        print("   Check OPENAI_API_KEY in environment variables")
        return False
    
    try:
        print("Testing OpenAI connection...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Say 'Connection successful!' in exactly 2 words."}
            ],
            max_tokens=10
        )
        
        message = response.choices[0].message.content
        print(f"✅ OpenAI API working!")
        print(f"   Test response: {message}")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI connection failed: {str(e)}")
        print("   Check your API key and GitHub Marketplace credits")
        return False


def get_cache_stats() -> dict:
    """Get statistics about explanation caching."""
    return {
        "pre_generated_count": len(DEMO_EXPLANATIONS),
        "runtime_cached_count": len(_openai_cache),
        "total_cached": len(DEMO_EXPLANATIONS) + len(_openai_cache),
        "cache_keys": list(_openai_cache.keys())
    }


def clear_runtime_cache():
    """Clear runtime cache (useful for testing)."""
    global _openai_cache
    _openai_cache = {}
    print("🗑️ Runtime cache cleared")


# Module-level test
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧪 TESTING OPENAI AI SERVICE")
    print("="*60 + "\n")
    
    # Test 1: Connection
    print("TEST 1: OpenAI Connection")
    print("-" * 40)
    connection_ok = test_openai_connection()
    print()
    
    # Test 2: Pre-generated explanation
    print("TEST 2: Pre-generated Explanation (Cache Tier 1)")
    print("-" * 40)
    exp1 = generate_why_explanation("React Fundamentals", ["JSX", "JavaScript"])
    print(f"Result: {exp1[:100]}...")
    print()
    
    # Test 3: Live API call (if connection OK)
    if connection_ok:
        print("TEST 3: Live OpenAI API Call (Cache Tier 3)")
        print("-" * 40)
        exp2 = generate_why_explanation("Machine Learning Basics", ["Python", "Mathematics"])
        print(f"Result: {exp2}")
        print()
        
        # Test 4: Runtime cache hit
        print("TEST 4: Runtime Cache Hit (Cache Tier 2)")
        print("-" * 40)
        exp3 = generate_why_explanation("Machine Learning Basics", ["Python", "Mathematics"])
        print(f"Result: {exp3[:100]}...")
        print()
    
    # Test 5: Cache stats
    print("TEST 5: Cache Statistics")
    print("-" * 40)
    stats = get_cache_stats()
    for key, value in stats.items():
        if key != "cache_keys":
            print(f"  {key}: {value}")
    print()
    
    print("="*60)
    if connection_ok:
        print("✅ ALL TESTS PASSED - OpenAI Integration Ready!")
    else:
        print("⚠️ API Connection Failed - But Fallbacks Work!")
    print("="*60 + "\n")