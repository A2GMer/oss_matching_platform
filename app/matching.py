from app.models import Project, User

def recommend_projects(user):
    user_skills = set(user.skills.split(','))
    projects = Project.query.all()
    recommendations = []
    for project in projects:
        project_skills = set(project.skills.split(','))
        match_score = len(user_skills & project_skills)
        if match_score > 0:
            recommendations.append((project, match_score))
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return [rec[0] for rec in recommendations]
