from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Literal

import networkx as nx

Difficulty = Literal["beginner", "intermediate", "advanced"]


@dataclass(frozen=True)
class Skill:
    id: str
    name: str
    description: str
    prerequisites: List[str]
    estimated_days: int
    difficulty: Difficulty
    common_pitfalls: List[str] = field(default_factory=list)
    real_world_applications: List[str] = field(default_factory=list)


def _define_skills() -> Dict[str, Skill]:
    """
    Define the skill catalog.

    Note: The original spec mentioned 20 skills, but we model each requested
    topic as its own skill for better granularity (24 total).
    """
    skills: Dict[str, Skill] = {}

    def add(skill: Skill) -> None:
        skills[skill.id] = skill

    # Foundations
    add(
        Skill(
            id="html",
            name="HTML Fundamentals",
            description="Structure web pages using semantic HTML elements.",
            prerequisites=[],
            estimated_days=3,
            difficulty="beginner",
            common_pitfalls=[
                "Overusing non-semantic tags like <div> instead of proper semantics",
                "Incorrect nesting of elements",
                "Forgetting accessibility attributes such as alt text",
            ],
            real_world_applications=[
                "Building static marketing pages",
                "Creating accessible document layouts",
                "Email templates and CMS content",
            ],
        )
    )
    add(
        Skill(
            id="css",
            name="CSS Fundamentals",
            description="Style and lay out web pages using core CSS features.",
            prerequisites=["html"],
            estimated_days=4,
            difficulty="beginner",
            common_pitfalls=[
                "Overly specific selectors that are hard to override",
                "Relying too much on !important",
                "Not understanding the cascade and inheritance",
            ],
            real_world_applications=[
                "Brand-consistent marketing sites",
                "Styling complex UI components",
                "Design systems and component libraries",
            ],
        )
    )
    add(
        Skill(
            id="javascript",
            name="JavaScript Basics",
            description="Write basic JavaScript to add interactivity to web pages.",
            prerequisites=["html", "css"],
            estimated_days=5,
            difficulty="beginner",
            common_pitfalls=[
                "Confusing == and ===",
                "Mutating global state unintentionally",
                "Poor error handling around asynchronous code",
            ],
            real_world_applications=[
                "Interactive forms and validation",
                "Basic UI widgets such as modals and tabs",
                "Client-side input sanitization",
            ],
        )
    )
    add(
        Skill(
            id="git",
            name="Git & Version Control",
            description="Track changes and collaborate using Git and remote repositories.",
            prerequisites=[],
            estimated_days=3,
            difficulty="beginner",
            common_pitfalls=[
                "Committing large unrelated changes together",
                "Accidentally committing secrets",
                "Struggling with merges and rebases due to unclear history",
            ],
            real_world_applications=[
                "Team collaboration on web apps",
                "Code review workflows",
                "Continuous integration and deployment pipelines",
            ],
        )
    )

    # JavaScript concepts
    add(
        Skill(
            id="variables",
            name="JavaScript Variables & Types",
            description="Understand let, const, var, and JavaScript data types.",
            prerequisites=["javascript"],
            estimated_days=2,
            difficulty="beginner",
            common_pitfalls=[
                "Using var instead of let/const and running into hoisting issues",
                "Mutating objects and arrays accidentally",
                "Misunderstanding truthy and falsy values",
            ],
            real_world_applications=[
                "Managing UI state in vanilla JS",
                "Configuring application-level settings",
                "Working with API responses and data models",
            ],
        )
    )
    add(
        Skill(
            id="functions",
            name="JavaScript Functions",
            description="Declare and use functions, including arrow functions.",
            prerequisites=["variables"],
            estimated_days=3,
            difficulty="beginner",
            common_pitfalls=[
                "Confusing function declarations and expressions",
                "Incorrectly binding this in callbacks",
                "Creating unnecessary closures that capture stale state",
            ],
            real_world_applications=[
                "Event handlers and callbacks",
                "Utility libraries for data transformation",
                "Modularizing complex UI logic",
            ],
        )
    )
    add(
        Skill(
            id="arrays",
            name="JavaScript Arrays",
            description="Manipulate ordered collections with built-in array methods.",
            prerequisites=["variables"],
            estimated_days=2,
            difficulty="beginner",
            common_pitfalls=[
                "Mutating arrays instead of using immutable patterns",
                "Using for-loops where higher-order methods are clearer",
                "Not handling empty arrays or out-of-bounds indexes",
            ],
            real_world_applications=[
                "Rendering lists of items in UIs",
                "Transforming API response data",
                "Implementing search, filter, and sort features",
            ],
        )
    )
    add(
        Skill(
            id="objects",
            name="JavaScript Objects",
            description="Model data using objects and understand prototypes.",
            prerequisites=["variables"],
            estimated_days=3,
            difficulty="beginner",
            common_pitfalls=[
                "Accidentally sharing object references",
                "Misunderstanding prototype inheritance",
                "Shadowing properties in object hierarchies",
            ],
            real_world_applications=[
                "Representing application domain models",
                "Configuration objects for libraries and frameworks",
                "State containers and stores",
            ],
        )
    )
    add(
        Skill(
            id="dom",
            name="DOM Manipulation",
            description="Interact with and update the browser DOM programmatically.",
            prerequisites=["javascript", "html"],
            estimated_days=3,
            difficulty="intermediate",
            common_pitfalls=[
                "Causing layout thrashing with inefficient DOM reads/writes",
                "Not cleaning up event listeners leading to memory leaks",
                "Directly manipulating DOM in frameworks that manage it virtually",
            ],
            real_world_applications=[
                "Dynamic form builders",
                "In-page content editors",
                "Legacy apps without modern frameworks",
            ],
        )
    )
    add(
        Skill(
            id="events",
            name="DOM Events",
            description="Handle user and system events with the DOM event model.",
            prerequisites=["dom"],
            estimated_days=2,
            difficulty="intermediate",
            common_pitfalls=[
                "Not understanding event propagation and delegation",
                "Attaching too many individual listeners",
                "Forgetting to prevent default browser behavior when necessary",
            ],
            real_world_applications=[
                "Interactive drag-and-drop experiences",
                "Keyboard-accessible interfaces",
                "Custom context menus and gestures",
            ],
        )
    )
    add(
        Skill(
            id="closures",
            name="Closures",
            description="Use closures to capture lexical scope and build abstractions.",
            prerequisites=["functions"],
            estimated_days=3,
            difficulty="intermediate",
            common_pitfalls=[
                "Accidentally retaining large objects leading to memory issues",
                "Capturing stale variables inside loops or async callbacks",
                "Overcomplicating code with unnecessary closure layers",
            ],
            real_world_applications=[
                "Encapsulating module state",
                "Implementing currying and partial application",
                "Creating factory functions for UI components",
            ],
        )
    )
    add(
        Skill(
            id="promises",
            name="Promises",
            description="Model asynchronous workflows using promises.",
            prerequisites=["functions"],
            estimated_days=3,
            difficulty="intermediate",
            common_pitfalls=[
                "Forgetting to return promises in chains",
                "Mixing callbacks and promises inconsistently",
                "Swallowing errors without proper catch handlers",
            ],
            real_world_applications=[
                "Fetching data from REST APIs",
                "Sequencing dependent async operations",
                "Parallelizing network requests efficiently",
            ],
        )
    )
    add(
        Skill(
            id="async_await",
            name="Async/Await",
            description="Write asynchronous code with async/await syntax on top of promises.",
            prerequisites=["promises"],
            estimated_days=2,
            difficulty="intermediate",
            common_pitfalls=[
                "Blocking concurrency by awaiting in loops",
                "Forgetting try/except style error handling with async functions",
                "Not handling rejection paths for awaited promises",
            ],
            real_world_applications=[
                "Readable API integration layers",
                "Server-side rendering logic in modern frameworks",
                "Complex workflows with multiple async steps",
            ],
        )
    )
    add(
        Skill(
            id="this_keyword",
            name="The this Keyword",
            description="Understand how this is bound in different JavaScript contexts.",
            prerequisites=["functions", "objects"],
            estimated_days=2,
            difficulty="intermediate",
            common_pitfalls=[
                "Losing this binding when passing methods as callbacks",
                "Using arrow functions where dynamic this is required",
                "Relying on implicit global this in sloppy mode",
            ],
            real_world_applications=[
                "Class-based components in older React codebases",
                "Event handler methods on objects",
                "Custom library and framework implementations",
            ],
        )
    )

    # Frontend (React ecosystem)
    add(
        Skill(
            id="jsx",
            name="JSX Syntax",
            description="Write JSX to describe UI trees within JavaScript.",
            prerequisites=["javascript", "dom"],
            estimated_days=3,
            difficulty="intermediate",
            common_pitfalls=[
                "Confusing expressions and statements inside JSX",
                "Overusing inline functions in render paths",
                "Not understanding how JSX compiles to function calls",
            ],
            real_world_applications=[
                "React component development",
                "Static site generation with tools like Next.js",
                "Design system documentation sites",
            ],
        )
    )
    add(
        Skill(
            id="react",
            name="React Fundamentals",
            description="Build component-based UIs using React.",
            prerequisites=["jsx"],
            estimated_days=7,
            difficulty="intermediate",
            common_pitfalls=[
                "Mutating state directly instead of using setters",
                "Deeply nested prop drilling instead of composition",
                "Not understanding reconciliation and key usage for lists",
            ],
            real_world_applications=[
                "Single-page applications",
                "Admin dashboards",
                "Cross-platform UI via React Native",
            ],
        )
    )
    add(
        Skill(
            id="components",
            name="Component Design",
            description="Design reusable, composable UI components.",
            prerequisites=["react"],
            estimated_days=4,
            difficulty="intermediate",
            common_pitfalls=[
                "Creating overly generic 'god' components",
                "Leaking implementation details through props",
                "Tightly coupling components to specific data sources",
            ],
            real_world_applications=[
                "Design systems and UI libraries",
                "White-label product theming",
                "Highly reusable internal dashboards",
            ],
        )
    )
    add(
        Skill(
            id="props",
            name="Props & Composition",
            description="Pass data and behavior between components using props.",
            prerequisites=["components"],
            estimated_days=2,
            difficulty="intermediate",
            common_pitfalls=[
                "Prop drilling instead of using context or better composition",
                "Passing unstable callback references causing re-renders",
                "Using props for things that should be internal state",
            ],
            real_world_applications=[
                "Configurable widgets and charts",
                "Composable layout systems",
                "Highly customizable component APIs",
            ],
        )
    )
    add(
        Skill(
            id="state",
            name="State Management",
            description="Manage local and shared UI state effectively.",
            prerequisites=["react", "props"],
            estimated_days=4,
            difficulty="advanced",
            common_pitfalls=[
                "Keeping too much global state",
                "Re-render storms due to poor state granularity",
                "Not normalizing complex nested data",
            ],
            real_world_applications=[
                "Real-time dashboards",
                "Collaborative editing tools",
                "Offline-capable progressive web apps",
            ],
        )
    )
    add(
        Skill(
            id="hooks",
            name="React Hooks",
            description="Reuse stateful logic and side effects via hooks.",
            prerequisites=["state"],
            estimated_days=4,
            difficulty="advanced",
            common_pitfalls=[
                "Breaking the rules of hooks (calling conditionally or in loops)",
                "Using useEffect as a catch-all for any side-effect",
                "Dependency array mistakes leading to stale or runaway effects",
            ],
            real_world_applications=[
                "Custom hooks for data fetching",
                "Shared behavior across complex components",
                "Abstracting cross-cutting concerns like analytics",
            ],
        )
    )

    # Styling
    add(
        Skill(
            id="flexbox",
            name="CSS Flexbox",
            description="Lay out one-dimensional UI structures using flexbox.",
            prerequisites=["css"],
            estimated_days=2,
            difficulty="intermediate",
            common_pitfalls=[
                "Over-nesting flex containers",
                "Misunderstanding flex-basis vs width",
                "Relying on magic numbers for spacing",
            ],
            real_world_applications=[
                "Navigation bars and toolbars",
                "Horizontal and vertical alignment",
                "Responsive card layouts",
            ],
        )
    )
    add(
        Skill(
            id="grid",
            name="CSS Grid",
            description="Create two-dimensional layouts using CSS Grid.",
            prerequisites=["flexbox"],
            estimated_days=3,
            difficulty="intermediate",
            common_pitfalls=[
                "Mixing grid and flexbox without clear responsibilities",
                "Hard-coding pixel-based tracks instead of using fractions",
                "Not considering content overflow behavior",
            ],
            real_world_applications=[
                "Complex dashboard layouts",
                "Magazine-style editorial designs",
                "Responsive image galleries",
            ],
        )
    )
    add(
        Skill(
            id="responsive",
            name="Responsive Design",
            description="Build layouts that adapt across devices and screen sizes.",
            prerequisites=["flexbox", "grid"],
            estimated_days=4,
            difficulty="intermediate",
            common_pitfalls=[
                "Designing only mobile or only desktop first",
                "Using too many discrete breakpoints",
                "Ignoring accessibility when rearranging content",
            ],
            real_world_applications=[
                "Mobile-first web applications",
                "Multi-device marketing sites",
                "Embedded web UIs in native shells",
            ],
        )
    )
    add(
        Skill(
            id="tailwind",
            name="Tailwind CSS",
            description="Use Tailwind utility classes to rapidly style components.",
            prerequisites=["css", "responsive"],
            estimated_days=3,
            difficulty="intermediate",
            common_pitfalls=[
                "Creating unreadable class soups on elements",
                "Not extracting reusable components from duplicated utilities",
                "Overriding Tailwind defaults without a clear design system",
            ],
            real_world_applications=[
                "Rapid prototyping of product ideas",
                "Design-consistent internal tools",
                "Theming SaaS dashboards with minimal custom CSS",
            ],
        )
    )

    return skills


def build_skill_graph() -> nx.DiGraph:
    """
    Build and return a directed skill dependency graph.

    Nodes are skill IDs with rich metadata as node attributes.
    Edges are directed from prerequisite -> dependent skill.
    """
    skills = _define_skills()
    graph = nx.DiGraph()

    for skill in skills.values():
        graph.add_node(
            skill.id,
            id=skill.id,
            name=skill.name,
            description=skill.description,
            prerequisites=list(skill.prerequisites),
            estimated_days=skill.estimated_days,
            difficulty=skill.difficulty,
            common_pitfalls=list(skill.common_pitfalls),
            real_world_applications=list(skill.real_world_applications),
        )

    for skill in skills.values():
        for prereq in skill.prerequisites:
            if prereq not in skills:
                raise ValueError(f"Unknown prerequisite '{prereq}' for skill '{skill.id}'")
            graph.add_edge(prereq, skill.id)

    if not nx.is_directed_acyclic_graph(graph):
        raise ValueError("Skill graph must be acyclic; a cycle was detected.")

    return graph


def get_learning_path(graph: nx.DiGraph, target_skill_id: str) -> List[str]:
    """
    Compute an ordered learning path (list of skill IDs) leading to the target.

    The path includes all transitive prerequisites and the target skill,
    ordered so that each skill appears after its prerequisites.
    """
    if target_skill_id not in graph:
        raise KeyError(f"Skill '{target_skill_id}' is not present in the graph.")

    ancestors = nx.ancestors(graph, target_skill_id)
    subgraph_nodes = list(ancestors) + [target_skill_id]
    subgraph = graph.subgraph(subgraph_nodes)

    ordered = list(nx.topological_sort(subgraph))
    return ordered


def describe_skill(graph: nx.DiGraph, skill_id: str) -> Dict[str, object]:
    """
    Return a human-friendly description payload for a given skill.
    """
    if skill_id not in graph:
        raise KeyError(f"Skill '{skill_id}' is not present in the graph.")

    data = graph.nodes[skill_id]
    successors = list(graph.successors(skill_id))
    predecessors = list(graph.predecessors(skill_id))

    return {
        "id": data["id"],
        "name": data["name"],
        "description": data["description"],
        "difficulty": data["difficulty"],
        "estimated_days": data["estimated_days"],
        "prerequisites": predecessors,
        "unlocks": successors,
        "common_pitfalls": data["common_pitfalls"],
        "real_world_applications": data["real_world_applications"],
    }


__all__ = [
    "Skill",
    "Difficulty",
    "build_skill_graph",
    "get_learning_path",
    "describe_skill",
]

