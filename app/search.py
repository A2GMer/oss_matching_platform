from app.models import Project

def search_projects(keyword=None, language=None, min_stars=None):
    query = Project.query
    if keyword:
        query = query.filter(Project.name.contains(keyword) | Project.description.contains(keyword))
    if language:
        query = query.filter(Project.language == language)
    if min_stars:
        query = query.filter(Project.stars >= min_stars)
    return query.all()
