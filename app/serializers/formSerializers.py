
def getuserformEntity(post) -> dict:
    return {
        "_id": str(post["_id"]),
        "modulename": post["modulename"],
        "recuriter": post['recuriter'],
        "moduleelements": post["moduleelements"],
        "singleColumnForms": post.get("singleColumnForms") if post.get("singleColumnForms") is not None else None
    }

def getalluserformEntity(post) -> dict:
    return {
        "_id": str(post["_id"]),
        "modulename": post["modulename"],
        "recuriter": post['recuriter'],
        "moduleelements": post["moduleelements"],
        "singleColumnForms": post.get("singleColumnForms") if post.get("singleColumnForms") is not None else None
    }

def getmoduletabledata(post) -> dict:
    return {
      "_id": str(post["_id"]),
      "moduleId": post['moduleId'],
      "recuriter": post['recuriter'], 
      "tableData": post["tableData"]
    }

def gettabledata(post) -> dict:
    return {
      "_id": str(post["_id"]),
      "tableData": post["tableData"]
    }

def getchecktabledata(post) -> dict:
    return {
      "tableData": post["tableData"]
    }


def getuserLogo(post) -> dict:
    return {
        "id": str(post["_id"]),
        "profile": post["profile"],
        "title": post["title"]
    }

def getcurrentuserLogo(post) -> dict:
    return {
        "id": str(post["_id"]),
        "profile": post["profile"],
        "title": post["title"]
    }

def getmodulename(post) -> dict:
    return {
        "_id": str(post["_id"]),
        "created_at": post["created_at"],
        "modulename": post["modulename"],
    }

def getsametabledata(post) -> dict:
    return {
      "tableData": post["tableData"]
    }

def getsametabledatalist(post) -> list:
    emptyarray = []
    for val in post:
        emptyarray.append((val))
    return emptyarray
      
    

    

