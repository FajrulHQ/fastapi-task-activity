from fastapi import Query

def page_size_pagination(
  query: Query,
  page: int, 
  size: int,
):
  response          = dict(page=page, size=size)
  offset            = (page - 1) * size
  response['total'] = query.count()
  response['data']  = query.limit(size).offset(offset).all()
  
  return response