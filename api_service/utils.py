def get_paginated_query(query, page, per_page):
    offset = (page - 1) * per_page
    paginated_query = query.limit(per_page).offset(offset)
    count = query.count()
    return paginated_query, count
